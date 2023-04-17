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

}

if (typeof module !== 'undefined' && typeof module.exports === 'object') {
    module.exports.Client = client.Client;
}

