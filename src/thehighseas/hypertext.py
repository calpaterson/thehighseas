import os
import inspect

from bottle import Bottle, request, response, abort
from mako.lookup import TemplateLookup

from rootapp import app
import rootapp
from constants import redis_connection, announce_url
from domain import Swarm

_template_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["templates/"])
_css_dir_ = "/".join(inspect.getfile(rootapp).split("/")[:-1] + ["css/"])

_templates_ = TemplateLookup(
    directories=[_template_dir_],
    module_directory='/tmp/thehighseas-templates')

@app.get("/")
def index():
    return _templates_.get_template("index.mako").render(swarms=Swarm.nonsecret())

@app.get("/upload")
def upload_form():
    return _templates_.get_template("upload.mako").render(announce_url=announce_url)

@app.get("/css/bootstrap.min.css")
def bootstrap():
    response.set_header("Content-Type", "text/css")
    return open(_css_dir_ + "bootstrap.min.css")

@app.get("/css/style.css")
def style():
    response.set_header("Content-Type", "text/css")
    return open(_css_dir_ + "style.css")

@app.get("/swarm/:hex_hash/download")
def download_metainfo(hex_hash):
    swarm = Swarm.from_hex_hash(hex_hash)
    response.set_header("Content-Type", "application/x-bittorrent")
    response.set_header("Content-Disposition",
                        "filename={name}.torrent".format(name=swarm.name()))
    return swarm.to_metainfo()

@app.get("/swarm/:hex_hash/details")
def details(hex_hash):
    swarm = Swarm.from_hex_hash(hex_hash)
    return _templates_.get_template("details.mako").render(swarm=swarm)

@app.post("/upload")
def upload():
    metainfo_file = request.files.get("metainfo-file")
    swarm = Swarm.from_metainfo_file(metainfo_file.file, metainfo_file.filename)
    response.set_header("Content-Type", "application/x-bittorrent")
    response.set_header("Content-Disposition",
                        "filename={name}.torrent".format(name=swarm.name()))
    return swarm.to_metainfo()
