import os
import inspect

from bottle import Bottle, request, response, abort
from mako.lookup import TemplateLookup

from rootapp import app
import rootapp
from constants import redis_connection
from values import Swarm

_template_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["templates/"])

_templates_ = TemplateLookup(
    directories=[_template_dir_],
    module_directory='/tmp/thehighseas-templates')      

@app.get("/")
def index():
    return _templates_.get_template("index.mako").render(swarms=Swarm.all())

@app.get("/upload")
def upload_form():
    return _templates_.get_template("upload_form.mako").render()

@app.post("/upload")
def upload():
    metainfo_file = request.files.get("metainfo-file")
    swarm = Swarm.from_metainfo_file(metainfo_file.file, metainfo_file.filename)
    response.set_header("Content-Type", "application/x-bittorrent")
    response.set_header("Content-Disposition",
                        "filename={name}.torrent".format(name=swarm.name()))
    return swarm.to_metainfo()
