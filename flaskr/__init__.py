import flask
import logging
import sys
import os
import json
from flask_httpauth import HTTPBasicAuth
from filehandlers import AbstractFile, FileManipulator

# init app
app = flask.Flask(__name__)
auth = HTTPBasicAuth()

# yeah, we run the bootstrap even if the code is imported
# create log file for first time
AbstractFile("server.log").touch()

# set up logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.addHandler(logging.FileHandler("server.log", mode="w"))
app.logger.setLevel(logging.DEBUG)

# enhanced crypto
app.secret_key = os.urandom(4096)  # many bytes

# basic info for console
app.logger.info("-- CloudRepo Download Analytics Server v1.0.0 --")
app.logger.info("-- This software is under the Apache 2.0 license. --")
app.logger.info("-- Source: https://github.com/CloudRepoOSS/download-analytics --")

json_template = {
    "all": 0,
    "downloads": {},
    "repos": {},
    "users": {
        # format: "username": "password"
        "admin": "admin123"
        # please change this in your save file, this is super insecure !!
    }
}

# save file init stuff
if os.path.exists("save.json"):
    app.logger.debug("Found save file - should have loaded via constructor")
else:
    globaljson: AbstractFile = AbstractFile("save.json")
    globaljson.touch()
    jsonmanip: FileManipulator = FileManipulator(globaljson)
    jsonmanip.write_to_file(
        json.dumps(json_template)
    )

# list annotation makes this look nice
common_methods: list = [
    "GET",
    "POST",
    "HEAD"
]


def saveJson(arraydict: dict):
    # we have arraydict in memory by now, so this is safe
    open("save.json", "w").write(json.dumps(arraydict))


@auth.error_handler
def auth_error():
    app.logger.warning(
        "User has triggered access denied - potential unauthorized login detected"
    )
    return "Access Denied!"


@auth.verify_password
def verify_password(username, password):
    eg = translate_file_input()
    if username in eg["users"]:
        return eg["users"][username] == password
    return False
    
# homepage
@app.route("/", methods=common_methods)
def homepage() -> flask.Response:
    return flask.Response(
        "Welcome to this CloudRepo download counting server!",
        mimetype="text/plain"
    )


# webhooks should ping this url if set up correctly
@app.route("/callback", methods=["POST"])
def webhook_callback() -> flask.Response:
    #app.logger.debug("Got request data: " + translate(flask.request.data))
    reqdata: dict = translate(flask.request.data)
    # json parsing/manipulating
    cachetmp: dict = translate_file_input()
    cachetmp["all"] = cachetmp["all"] + 1
    try:
        cachetmp["downloads"][reqdata["file-name"]] = cachetmp["downloads"][reqdata["file-name"]] + 1
    except KeyError:
        cachetmp["downloads"][reqdata["file-name"]] = 1
    try:
        cachetmp["repos"][reqdata["repository-id"]] = cachetmp["repos"][reqdata["repository-id"]] + 1
    except KeyError:
        cachetmp["repos"][reqdata["repository-id"]] = 1
    saveJson(cachetmp)
    return flask.Response(
        json.dumps({
            "success": True
        }),
        mimetype="text/plain"
    )


# we only want bytes in because strings are much easier to work with
def translate(stream: bytes) -> dict:
    return json.loads(stream)


def translate_file_input() -> dict:
    return translate(FileManipulator(AbstractFile('save.json')).get_cache()[0])


@app.route("/stats", methods=common_methods)
@auth.login_required
def stats():
    # login is required for this endpoint for security
    return flask.render_template(
        "stats.html",
        chartcorelink=flask.url_for('static', filename='chartcore.min.js'),
        piechartextlink=flask.url_for('static', filename='piechart.min.js'),
        stylesheetlink=flask.url_for('static', filename='dash.css'),
        data=json.loads(FileManipulator(AbstractFile("save.json")).get_cache()[0]),
        overallcount=translate_file_input()["all"]  # todo: using translate above breaks stuff
    )


# if file is being run directly, let's get this show on the road:
if __name__ == "__main__":
    app.run("127.0.0.1")
