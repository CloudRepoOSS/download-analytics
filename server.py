import flask
import logging
import sys
import os
import json
from filehandlers import AbstractFile, FileManipulator

# init app
app = flask.Flask(__name__)

# set up logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.addHandler(logging.FileHandler("server.log", mode="w"))
app.logger.setLevel(logging.DEBUG)

# basic info for console
app.logger.info("-- CloudRepo Download Analytics Server v1.0.0 --")
app.logger.info("-- This software is under the Apache 2.0 license. --")
app.logger.info("-- Source: https://github.com/CloudRepoOSS/download-analytics --")

json_template = {
    "all": 0,
    "downloads": {},
    "repos": {}
}

# save file init stuff
if os.path.exists("save.json"):
    app.logger.debug("Found save file - should have loaded via constructor")
else:
    globaljson: AbstractFile = AbstractFile("save.json")
    globaljson.touch()
    jsonmanip = FileManipulator(globaljson)
    jsonmanip.write_to_file(
        json.dumps(json_template)
    )

# list annotation makes this look nice
common_methods: list = [
    "GET",
    "POST",
    "HEAD"
]


def saveJson(arraylist: list):
    jsonmanip: FileManipulator(AbstractFile("save.json"))
    jsonmanip.write_to_file(json.dumps(arraylist))
    jsonmanip.refresh()


# homepage
@app.route("/", methods=common_methods)
def homepage() -> flask.Response:
    return flask.Response(
        "Welcome to this CloudRepo download counting server!",
        mimetype="text/plain"
    )


# webhooks should ping this url if set up correctly
@app.route("/callback", methods=common_methods)
def webhook_callback() -> flask.Response:
    logging.getLogger().debug("Got request data: " + flask.request.data)
    jsonmanip = FileManipulator(AbstractFile("save.json"))
    # json parsing/manipulating
    cachetmp: list = jsonmanip.cache()
    cachetmp["all"] = cachetmp["all"] + 1
    try:
        cachetmp["downloads"][flask.request.data["file-name"]] = cachetmp["downloads"][flask.request.data["file-name"]] + 1
    except KeyError:
        cachetmp["downloads"][flask.request.data["file-name"]] = 1
    try:
        cachetmp["repos"][flask.request.data["repository-id"]] = cachetmp["repos"][flask.request.data["repository-id"]] + 1
    except KeyError:
        cachetmp["repos"][flask.request.data["repository-id"]] = 1
    saveJson(cachetmp)
    return flask.Response(
        json.dumps({
            "success": True
        }),
        mimetype="text/plain"
    )


# if file is being run directly, lets get this show on the road:
if __name__ == "__main__":
    app.run("127.0.0.1")
