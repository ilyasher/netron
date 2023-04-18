// Sends graph edits to the server.
client.Client = class {

    constructor() {
        this.connected = false;
        this.connect();
    }

    connect() {
        fetch('/python_version', {method: "GET"})
            .then(() => { this.connected = true; })
            .catch(() => {
                this.connected = false;
                console.log("[client.js] Warning: Unable to connect to python server");
            });
    }

    open(file) {
        // Send ONNX file to server.
        const form = new FormData();
        form.append('file', file);
        fetch('/model/open', {
            method: 'POST',
            body: form
        })
        .catch((e) => { this._log_fail(funcName(), e); });
    }

    download(host) {
        fetch('/model/save', { method: 'POST' })
            .then((status) => {
                status.blob().then((blob) => {
                    const bigBlob = new Blob([ blob ]);
                    host.export('modified.onnx', bigBlob);
                });
            })
            .catch((e) => { this._log_fail(funcName(), e); });
    }

    cleanup() {
        // TODO: implement
    }

    add_attr(node_id, attr_name, attr_value, attr_type) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'attr_name': attr_name,
            'attr_value': attr_value,
            'attr_type': attr_type,
        });
    }

    remove_attr(node_id, attr_name) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'attr_name': attr_name,
        });
    }

    change_attr_name(node_id, attr_name, new_name) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'attr_name': attr_name,
            'new_name': new_name,
        });
    }

    change_attr_value(node_id, attr_name, new_value) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'attr_name': attr_name,
            'new_value': new_value,
        });
    }

    change_attr_type(node_id, attr_name, new_value) {
        // TODO: implement
    }

    add_node(node_id, node_name, node_op) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'node_name': node_name,
            'node_op': node_op,
        });
    }

    remove_node(node_id) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
        });
    }

    change_node_name(node_id, new_name) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'new_name': new_name,
        });
    }

    change_node_op(node_id, new_op) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'new_op': new_op,
        });
    }

    change_node_op(node_id, new_op) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'new_op': new_op,
        });
    }

    change_node_description(node_id, new_description) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'new_description': new_description,
        });
    }

    add_node_input_output(node_id, io_name, input_or_output) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'io_name': io_name,
            'input_or_output': input_or_output,
        });
    }

    remove_node_input_output(node_id, io_name, input_or_output) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'io_name': io_name,
            'input_or_output': input_or_output,
        });
    }

    change_node_input_output(node_id, old_name, new_name, input_or_output) {
        this._do_model_edit(funcName(), {
            'node_id': node_id,
            'old_name': old_name,
            'new_name': new_name,
            'input_or_output': input_or_output,
        });
    }

    change_model_opset(opset) {
        this._do_model_edit(funcName(), {
            'opset': opset,
        });
    }

    change_model_producer(producer) {
        this._do_model_edit(funcName(), {
            'producer': producer,
        });
    }

    change_model_description(description) {
        this._do_model_edit(funcName(), {
            'description': description,
        });
    }

    add_model_input_output(io_name, input_or_output) {
        this._do_model_edit(funcName(), {
            'io_name': io_name,
            'input_or_output': input_or_output,
        });
    }

    remove_model_input_output(io_name, input_or_output) {
        this._do_model_edit(funcName(), {
            'io_name': io_name,
            'input_or_output': input_or_output,
        });
    }

    // Helper function which returns the caller function's name.
    funcName() {
        return funcName.caller.name;
    }

    // Helper function to send a model edit to the server.
    // If server is not connected, this function does nothing.
    _do_model_edit(action_name, params) {
        if (!this.connected) return;

        params['action'] = action_name;

        fetch('/model/edit', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(params)
        })
        .catch((e) => { this._log_fail(action_name, e); });
    }

    _log_fail(action_name, e) {
        console.log("[client.js] Error performing " + action_name + ": " + e);
    }
}

if (typeof module !== 'undefined' && typeof module.exports === 'object') {
    module.exports.Client = client.Client;
}

