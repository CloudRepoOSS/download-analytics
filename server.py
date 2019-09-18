import flask
import logging
import sys
import os
import json
from filehandlers import AbstractFile, FileManipulator
from io import TextIOWrapper

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

globaljson: AbstractFile = AbstractFile("save.json")
jsonmanip: FileManipulator(globaljson)

# save file init stuff

if os.path.exists("save.json"):
    app.logger.debug("Found save file - should have loaded via constructor")
else:
    globaljson.touch()
    jsonmanip.write_to_file(
        json.dumps({
            "all": 0
        })
    )

# list annotation makes this look nice
common_methods: list = [
    "GET",
    "POST",
    "HEAD"
]


# not exactly thread safe but whatever
def saveJson():
    jsonmanip.write_to_file(json.dumps(ourjson))
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
    cachetmp: list = jsonmanip.cache()
    cachetmp["all"] = cachetmp["all"] + 1
    saveJson()
    return flask.Response(
        json.dumps({
            "success": True
        }),
        mimetype="text/plain"
    )


# if file is being run directly, lets get this show on the road:
if __name__ == "__main__":
    app.run("127.0.0.1")
