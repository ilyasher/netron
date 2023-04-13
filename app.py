######
# app.py
#
# Entry point for onnx-graphsurgeon GUI web app.
##

from bottle import route, get, post, request, run, static_file
import pathlib

@route('/<filename:path>')
def get_file(filename):
    response = static_file(filename, root=pathlib.Path(__file__).parent.resolve())
    response.set_header("Cache-Control", "max-age=0") # no cached files TODO: doesn't work.
    return response

@route('/')
def hello():
    return get_file('index.html')

@get('/python_version')
def has_python():
    # Javascript can query this to see if python is available.
    import platform
    return platform.python_version()


### Graphsurgeon stuff begins here
### TODO: factor out to different file

import onnx
import onnx_graphsurgeon as gs

model = None

@post('/open_model')
def open_model():
    global model
    print("[app.py] importing model")
    onnx_file = request.files['file']
    print(onnx_file)
    model = gs.import_onnx(onnx.load_model_from_string(onnx_file.file.read()))
    print("[app.py] imported model!")

@post('/edit_model')
def edit_model():
    global model
    edit = request.json
    print(edit)
    if edit['action'] == 'change_attr_name':
        for node in model.nodes:
            if node.name == edit['node_name']:
                node.attrs[edit['new_name']] = node.attrs.pop(edit['attr_name'])
    else:
        print("Unknown edit action: ", edit['action'])

@post('/save_model')
def save_model():
    global model
    model_proto = gs.export_onnx(model)
    # as_bytes = model_proto.SerializeToString()

    # FIXME is this necessary?
    tmp_filename = '/tmp/modified.onnx'
    onnx.save(model_proto, tmp_filename)
    return static_file(tmp_filename, root='/', download='modified.onnx')



### end Graphsurgeon stuff

run(host='localhost', port=8080, debug=True)
