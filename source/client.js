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

	_log_fail(action_name, e) {
		console.log("[client.js] Error performing " + action_name + ": " + e);
	}

	open(file) {
		if (!this.connected) return;

        // Send ONNX file to server.
        const form = new FormData();
        form.append('file', file);
        fetch('/model/open', {
            method: 'POST',
            body: form
        })
        .catch((e) => { this._log_fail('open', e); });    
	}

	download(host) {
		if (!this.connected) return;
        fetch('/model/save', { method: 'POST' })
        	.then((status) => {
	            status.blob().then((blob) => {
	                const bigBlob = new Blob([ blob ]);
	                host.export('modified.onnx', bigBlob);
	            });
	        })
        	.catch((e) => { this._log_fail("download", e); });
	}

	cleanup() {
		if (!this.connected) return;
		// TODO: implement
	}

	funcName() {
    	return funcName.caller.name;
	}

	_send_json(route, object) {
		return fetch(route, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(object)
        })
	}

	add_attr(node_id, attr_name, attr_value, attr_type) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': 'add_attr',
            'node_id': node_id,
            'attr_name': attr_name,
            'attr_value': attr_value,
            'attr_type': attr_type,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	remove_attr(node_id, attr_name) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'attr_name': attr_name,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_attr_name(node_id, attr_name, new_name) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'attr_name': attr_name,
            'new_name': new_name,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_attr_value(node_id, attr_name, new_value) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'attr_name': attr_name,
            'new_value': new_value,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_attr_type(node_id, attr_name, new_value) {
		if (!this.connected) return;
		// TODO: implement
	}

	add_node(node_id, node_name, node_op) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'node_name': node_name,
            'node_op': node_op,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	remove_node(node_id) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_node_name(node_id, new_name) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'new_name': new_name,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_node_op(node_id, new_op) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'new_op': new_op,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_node_op(node_id, new_op) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'new_op': new_op,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_node_description(node_id, new_description) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'new_description': new_description,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	add_node_input_output(node_id, io_name, input_or_output) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'io_name': io_name,
            'input_or_output': input_or_output,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	remove_node_input_output(node_id, io_name, input_or_output) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'io_name': io_name,
            'input_or_output': input_or_output,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_node_input_output(node_id, old_name, new_name, input_or_output) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'node_id': node_id,
            'old_name': old_name,
            'new_name': new_name,
            'input_or_output': input_or_output,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_model_opset(opset) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'opset': opset,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_model_producer(producer) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'producer': producer,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	change_model_description(description) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'description': description,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	add_model_input_output(io_name, input_or_output) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'io_name': io_name,
            'input_or_output': input_or_output,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

	remove_model_input_output(io_name, input_or_output) {
		if (!this.connected) return;

		const action_name = funcName();
		this._send_json('/model/edit', {
            'action': action_name,
            'io_name': io_name,
            'input_or_output': input_or_output,
        })
        .catch((e) => { this._log_fail(action_name, e); });
	}

}

if (typeof module !== 'undefined' && typeof module.exports === 'object') {
    module.exports.Client = client.Client;
}

