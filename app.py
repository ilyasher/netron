######
# app.py
#
# Entry point for onnx-graphsurgeon GUI web app.
##

from bottle import route, get, post, run, static_file
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

def open_model(filepath):
    ...

def modify_model():
    ...

def save_model(filepath):
    ...


### end Graphsurgeon stuff

run(host='localhost', port=8080, debug=True)
