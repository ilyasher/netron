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

        # TODO: generate node IDs.
        self.nodes: Dict[str, gs.Node] = ...

        # TODO: do we need a lock?

    ################ Constructors
    @classmethod
    def from_file(cls, filepath: str) -> "Model":
        return Model(gs.import_onnx(onnx.load(filepath)))
    
    @classmethod
    def from_bytes(cls, bytes: bytes) -> "Model":
        return Model(gs.import_onnx(onnx.load_model_from_string(bytes)))

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

            # below this line is TODO

            # Node properties.
            'add_node': None,
            'remove_node': None,
            'change_node_name': None,
            'change_node_op': None,
            'change_node_description': None,

            # Node inputs & outputs.
            'add_node_input': None,
            'remove_node_input': None,
            'change_node_input': None,
            'add_node_output': None,
            'remove_node_output': None,
            'change_node_output': None,

            # Model properties.
            'change_model_opset': None,
            'change_model_producer': None,
            'change_model_description': None,

            # Model inputs & outputs.
            'add_model_input': None,
            'remove_model_input': None,
            'change_model_input': None,
            'add_model_output': None,
            'remove_model_output': None,
            'change_model_output': None,
        }
        action_name = edit_json['action']
        return action_handlers[action_name](edit_json)
    
    def _get_node_by_id(self, node_id):
        for node in self.model.nodes:
            if node.name == node_id: # FIXME
                return node
        raise KeyError(node_id)

    def _change_attr_name(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_name'] # FIXME use ID
        attr_name = edit_json['attr_name']
        new_name = edit_json['new_name']

        node = self._get_node_by_id(node_id)
        node.attrs[new_name] = node.attrs.pop(attr_name)

    def _change_attr_value(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_name'] # FIXME use ID
        attr_name = edit_json['attr_name']
        new_value = edit_json['new_value']

        node = self._get_node_by_id(node_id)
        node.attrs[attr_name] = new_value

    def _change_attr_type(self, edit_json: Dict[str, Any]):
        # TODO
        pass

    def _add_attr(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_name'] # FIXME use ID
        attr_name = edit_json['attr_name']
        attr_value = edit_json['attr_value']
        attr_type = edit_json['attr_type'] # FIXME unused

        node = self._get_node_by_id(node_id)
        node.attrs[attr_name] = attr_value

    def _remove_attr(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_name'] # FIXME use ID
        attr_name = edit_json['attr_name']

        node = self._get_node_by_id(node_id)
        del node.attrs[attr_name]

