######
# app.py
#
# Entry point for onnx-graphsurgeon GUI web app.
##

from bottle import route, run, static_file
import pathlib

@route('/<filename:path>')
def get_file(filename):
    return static_file(filename, root=pathlib.Path(__file__).parent.resolve())

@route('/')
def hello():
    return get_file('index.html')



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
