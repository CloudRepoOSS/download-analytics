import flask
import logging
import sys
import os
import json
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

# save file init stuff
# todo: use filehandlers (https://filehandlers.rdil.rocks) for easier interfacing
ourjson = None
if os.path.exists("save.json"):
    app.logger.debug("Found save file - attempting to load")
    with open("save.json", mode="r") as filehandler:
        ourjson = json.loads(filehandler.read())
        filehandler.close()
else:
    mkfile: TextIOWrapper = open("save.json", "a")
    mkfile.write(
        json.dumps({
            "all": 0
        })
    )
    ourjson = mkfile.read()
    mkfile.close()

# list annotation makes this look nice
common_methods: list = [
    "GET",
    "POST",
    "HEAD"
]


# not exactly thread safe but whatever
def saveJson():
    e: TextIOWrapper = open("save.json", "w")
    e.write(json.dumps(ourjson))
    e.close()
    ourjson = json.loads(open("save.json", mode="r").read())


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
    ourjson["all"] = ourjson["all"] + 1
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
