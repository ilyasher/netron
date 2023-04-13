######
# graphsurgeon_http.py
#
# Wrapper around onnx-graphsurgeon which enables
# using onnx-graphsurgeon via a JSON API.
##

from typing import Dict, Any

import onnx
import onnx_graphsurgeon as gs

class Model:

    def __init__(self, model: gs.Graph):
        self.model: gs.Graph = model
        self.nodes: Dict[int, gs.Node] = {id: node for id, node in enumerate(model.nodes)}

        # TODO: do we need a lock?

    ################ Constructors
    @classmethod
    def from_file(cls, filepath: str) -> "Model":
        return Model(gs.import_onnx(onnx.load(filepath)))
    
    @classmethod
    def from_bytes(cls, bytes: bytes) -> "Model":
        return Model(gs.import_onnx(onnx.load_model_from_string(bytes)))

    ################# I'm not sure if we really need this API.
    def assign_node_ids(self, node_ids: bytes):
        # FIXME no assert
        assert len(node_ids) == len(self.model.nodes)
        self.nodes = {id: node for id, node in zip(node_ids, self.model.nodes)}

    ################ Serialization & Saving
    def to_bytes(self) -> bytes:
        return gs.export_onnx(self.model).SerializeToString()
    
    def save_to_file(self, filepath):
        onnx.save(gs.export_onnx(self.model), filepath)

    ################ Advanced Graphsurgeon Edits.
    def cleanup(self):
        self.model.cleanup()

    ############### Basic Graphsurgeon Edits.
    def edit(self, edit_json: Dict[str, Any]):
        '''
        General edit methods which dispatches to helper methods.

        Throws KeyError if edit_json['action'] does not exist or is not valid.
        '''
        action_handlers = {
            # Attributes.
            'add_attr': self._add_attr,
            'remove_attr': self._remove_attr,
            'change_attr_name': self._change_attr_name,
            'change_attr_value': self._change_attr_value,
            'change_attr_type': self._change_attr_type,

            # Node properties.
            'add_node': self._add_node,
            'remove_node': self._remove_node,
            'change_node_name': self._change_node_name,
            'change_node_op': self._change_node_op,
            'change_node_description': self._change_node_description,

            # Node inputs & outputs.
            'add_node_input_output': self._add_node_input_output,
            'remove_node_input_output': self._remove_node_input_output,
            'change_node_input_output': self._change_node_input_output,

            # Model properties.
            'change_model_opset': self._change_model_opset,
            'change_model_producer': self._change_model_producer,
            'change_model_description': self._change_model_description,

            # Model inputs & outputs.
            'add_model_input_output': self._add_model_input_output,
            'remove_model_input_output': self._remove_model_input_output,
        }
        action_name = edit_json['action']
        return action_handlers[action_name](edit_json)
    
    def _get_node_by_id(self, node_id):
        return self.nodes[node_id]

    def _change_attr_name(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        attr_name = edit_json['attr_name']
        new_name = edit_json['new_name']

        node = self._get_node_by_id(node_id)
        node.attrs[new_name] = node.attrs.pop(attr_name)

    def _change_attr_value(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        attr_name = edit_json['attr_name']
        new_value = edit_json['new_value']

        node = self._get_node_by_id(node_id)
        node.attrs[attr_name] = new_value

    def _change_attr_type(self, edit_json: Dict[str, Any]):
        # TODO
        pass

    def _add_attr(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        attr_name = edit_json['attr_name']
        attr_value = edit_json['attr_value']
        attr_type = edit_json['attr_type'] # FIXME unused

        node = self._get_node_by_id(node_id)
        node.attrs[attr_name] = attr_value

    def _remove_attr(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        attr_name = edit_json['attr_name']

        node = self._get_node_by_id(node_id)
        del node.attrs[attr_name]

    def _add_node(self, edit_json: Dict[str, Any]):
        node_id   = edit_json['node_id']
        node_name = edit_json['node_name']
        node_op   = edit_json['node_op']

        node = gs.Node(node_op, node_name)
        self.model.nodes.append(node)
        self.nodes[node_id] = node

    def _remove_node(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        node = self.nodes.pop(node_id)
        self.model.nodes.remove(node)

    def _change_node_name(self, edit_json: Dict[str, Any]):
        node_id  = edit_json['node_id']
        new_name = edit_json['new_name']

        node = self.nodes[node_id]
        node.name = new_name

    def _change_node_op(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_id']
        new_op  = edit_json['new_op']

        node = self.nodes[node_id]
        node.op = new_op

    def _change_node_description(self, edit_json: Dict[str, Any]):
        # onnx-graphsurgeon doesn't have node descriptions.
        pass

    def _add_node_input_output(self, edit_json: Dict[str, Any]):
        node_id  = edit_json['node_id']
        io_name  = edit_json['io_name']
        is_input = edit_json['input_or_output'] == 'input'

        node = self.nodes[node_id]
        io_list = node.inputs if is_input else node.outputs
        io_list.append(io_name)

    def _remove_node_input_output(self, edit_json: Dict[str, Any]):
        node_id  = edit_json['node_id']
        io_name  = edit_json['io_name']
        is_input = edit_json['input_or_output'] == 'input'

        node = self.nodes[node_id]
        io_list = node.inputs if is_input else node.outputs
        io_list.remove(io_name)

    def _change_node_input_output(self, edit_json: Dict[str, Any]):
        node_id  = edit_json['node_id']
        old_name = edit_json['old_input_name']
        new_name = edit_json['new_input_name']
        is_input = edit_json['input_or_output'] == 'input'

        node = self.nodes[node_id]
        io_list = node.inputs if is_input else node.outputs
        io_list[io_list.index(old_name)] = new_name

    def _change_model_opset(self, edit_json: Dict[str, Any]):
        opset = edit_json['opset']
        try:
            self.model.opset = int(opset)
        except ValueError as e:
            print("Failed to cast opset to int: ", e)

    def _change_model_producer(self, edit_json: Dict[str, Any]):
        # Producer is not supported by onnx-graphsurgeon
        pass

    def _change_model_description(self, edit_json: Dict[str, Any]):
        self.model.doc_string = edit_json['description']

    def _add_model_input_output(self, edit_json: Dict[str, Any]):
        io_name  = edit_json['io_name']
        is_input = edit_json['input_or_output'] == 'input'

        io_list = self.model.inputs if is_input else self.model.outputs
        io_list.append(io_name)

    def _remove_model_input_output(self, edit_json: Dict[str, Any]):
        io_name  = edit_json['io_name']
        is_input = edit_json['input_or_output'] == 'input'

        io_list = self.model.inputs if is_input else self.model.outputs
        io_list.remove(io_name)
