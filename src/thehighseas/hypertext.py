import os
import inspect

from bottle import Bottle, request, response, abort
from mako.lookup import TemplateLookup

from rootapp import app
import rootapp

_template_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["templates/"])

_templates_ = TemplateLookup(
    directories=[_template_dir_],
    module_directory='/tmp/thehighseas-templates')

@app.get("/")
def index():
    return _templates_.get_template("index.mako").render()
