######
# app.py
#
# Entry point for onnx-graphsurgeon GUI web app.
##

from bottle import route, get, post, request, run, static_file
import pathlib

from graphsurgeon_http import Model

# TODO: how to not use global variable?
model = None

@route('/')
def hello():
    # Default landing page.
    return get_file('index.html')

@route('/<filename:path>')
def get_file(filename):
    # Necessary for the website to load static files like CSS, JS, images, etc.
    response = static_file(filename, root=pathlib.Path(__file__).parent.resolve())
    response.set_header("Cache-Control", "max-age=0") # no cached files TODO: doesn't work.
    return response

@get('/python_version')
def has_python():
    # Client can query this to see if it is connected to our bottle server.
    import platform
    return platform.python_version()

@post('/model/open')
def open_model():
    # Load a user-uploaded ONNX model into graphsurgeon.
    global model
    onnx_file = request.files['file']
    model = Model.from_bytes(onnx_file.file.read())

@post('/model/assign_node_ids')
def assign_node_ids():
    # I would like to delete this.
    global model
    model.assign_node_ids(request.json)

@post('/model/edit')
def edit_model():
    # This should be called when the user makes an edit to the model using the web GUI.
    # The edit is given as a json dict which we use to make the exact same edit
    # to the onnx-graphsurgeon model.
    global model
    try:
        model.edit(request.json)
    except KeyError as e:
        print("KeyError when editing model: ", e)

@post('/model/save')
def save_model():
    # Serve the saved graphsurgeon graph as a file which the client can download.
    global model
    tmp_filename = '/tmp/modified.onnx'
    model.save_to_file(tmp_filename)
    return static_file(tmp_filename, root='/')

@post('/model/cleanup')
def cleanup_model():
    # TODO
    global model
    model.cleanup()
    return save_model()

run(host='localhost', port=8080, debug=True)
