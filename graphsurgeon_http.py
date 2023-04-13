from typing import Dict, Any

import onnx
import onnx_graphsurgeon as gs

class Model:

    def __init__(self, model: gs.Graph):
        self.model = model

        # TODO: generate node IDS.

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
            'change_attr_name': self._change_attr_name,
        }
        action_name = edit_json['action']
        return action_handlers[action_name](edit_json)
    
    def _change_attr_name(self, edit_json: Dict[str, Any]):
        node_id = edit_json['node_name'] # FIXME use ID
        old_name = edit_json['attr_name']
        new_name = edit_json['new_name']
        
        for node in self.model.nodes:
            if node.name == node_id: # FIXME
                node.attrs[new_name] = node.attrs.pop(old_name)

