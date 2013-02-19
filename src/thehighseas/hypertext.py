import os
import inspect

from bottle import Bottle, request, response, abort
from mako.lookup import TemplateLookup

from rootapp import app
import rootapp
from constants import redis_connection, announce_url
from values import Swarm

_template_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["templates/"])
_css_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["css/"])

_templates_ = TemplateLookup(
    directories=[_template_dir_],
    module_directory='/tmp/thehighseas-templates')

@app.get("/")
def index():
    return _templates_.get_template("index.mako").render(swarms=Swarm.all())

@app.get("/upload")
def upload_form():
    return _templates_.get_template("upload.mako").render(announce_url=announce_url)

@app.get("/css/bootstrap.min.css")
def index():
    response.set_header("Content-Type", "text/css")
    return open(_css_dir_ + "bootstrap.min.css")

@app.get("/css/style.css")
def index():
    response.set_header("Content-Type", "text/css")
    return open(_css_dir_ + "style.css")

@app.get("/torrent/:hex_hash")
def torrent(hex_hash):
    swarm = Swarm.from_hex_hash(hex_hash)
    response.set_header("Content-Type", "application/x-bittorrent")
    response.set_header("Content-Disposition",
                        "filename={name}.torrent".format(name=swarm.name()))
    return swarm.to_metainfo()

@app.post("/upload")
def upload():
    metainfo_file = request.files.get("metainfo-file")
    swarm = Swarm.from_metainfo_file(metainfo_file.file, metainfo_file.filename)
    response.set_header("Content-Type", "application/x-bittorrent")
    response.set_header("Content-Disposition",
                        "filename={name}.torrent".format(name=swarm.name()))
    return swarm.to_metainfo()
