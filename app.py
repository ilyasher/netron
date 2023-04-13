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

from graphsurgeon_http import Model
model = None

@post('/model/open')
def open_model():
    global model
    onnx_file = request.files['file']
    model = Model.from_bytes(onnx_file.file.read())

@post('/model/edit')
def edit_model():
    global model
    try:
        model.edit(request.json)
    except KeyError as e:
        print("KeyError when editing model: ", e)

@post('/model/save')
def save_model():
    global model
    tmp_filename = '/tmp/modified.onnx'
    model.save_to_file(tmp_filename)
    return static_file(tmp_filename, root='/')

@post('/model/cleanup')
def cleanup_model():
    global model
    model.cleanup()
    return save_model()


### end Graphsurgeon stuff

run(host='localhost', port=8080, debug=True)
