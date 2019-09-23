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
    "types": {
        "jarfile": 0,
        "pom": 0,
        "crypto": 0,
        "other": 0
    },
    "users": {
        # format: "username": "password"
        "admin": "admin123"
        # please change this in your save file, this is super insecure !!
    },
    "display": {
        "by-file-name": True,
        "by-repo-name": True,
        "by-file-type": True
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
    "POST"
]


def update_save_file(arraydict: dict):
    # we have arraydict in memory by now, so this is safe
    open("save.json", "w").write(json.dumps(arraydict))


@auth.error_handler
def auth_error():
    """
    View to be displayed when the user inputs invalid credentials.

    :return: the view
    :rtype: str
    """
    app.logger.warning(
        "User has triggered access denied - potential unauthorized login detected"
    )
    return "Access Denied!"


@auth.verify_password
def verify_password(username, password):
    """
    Verify the user-inputted credentials.

    :param username: the username inputted
    :param password: the password inputted
    :return: if the credentials are correct
    :rtype: bool
    """
    eg = translate_file_input()
    if username in eg["users"]:
        return eg["users"][username] == password

    # username is wrong
    return False


# homepage
@app.route("/", methods=common_methods)
def homepage() -> flask.Response:
    """
    Homepage/greeting view

    :return: the homepage text
    :rtype: flask.Response
    """
    return flask.Response(
        "Welcome to this CloudRepo download counting server!",
        mimetype="text/plain"
    )


# webhooks should ping this url if set up correctly
@app.route("/callback", methods=["POST"])
def webhook_callback() -> flask.Response:
    """
    Webhook callback endpoint

    :return: the Response object
    :rtype: flask.Response
    """
    reqdata: dict = translate(flask.request.data)
    # json parsing/manipulating
    cachetmp: dict = translate_file_input()
    cachetmp["all"] = cachetmp["all"] + 1
    # in theory with these try/except statements, a KeyError *could*
    # be thrown within the except blocks resulting in data loss, but
    # I don't think the complex logic is worth it.
    try:
        cachetmp["downloads"][reqdata["file-name"]] += 1
    except KeyError:
        cachetmp["downloads"][reqdata["file-name"]] = 1
    try:
        cachetmp["repos"][reqdata["repository-id"]] += 1
    except KeyError:
        cachetmp["repos"][reqdata["repository-id"]] = 1
    # have this logic first to prevent stuff like .jar.sha256
    if "sha" in reqdata["filename"] or "md5":
        cachetmp["types"]["crypto"] += 1
        # abort early
        update_save_file(cachetmp)
        return flask.Response(
            json.dumps({
                "success": True
            }),
            mimetype="application/json"
        )
    if ".xml" in reqdata["filename"]:
        cachetmp["types"]["pom"] += 1
    elif ".jar" in reqdata["filename"]:
        cachetmp["types"]["pom"] += 1
    else:
        cachetmp["other"] += 1
    update_save_file(cachetmp)
    return flask.Response(
        json.dumps({
            "success": True
        }),
        mimetype="application/json"
    )


# we only want bytes in because strings are much easier to work with
def translate(stream: bytes) -> dict:
    return json.loads(stream)


def translate_file_input() -> dict:
    """
    Loads the raw bytes of the save file, and translates them to a dict.

    :return: the dict
    :rtype: dict
    """
    return translate(FileManipulator(AbstractFile('save.json')).get_cache()[0])


@app.route("/stats", methods=common_methods)
@auth.login_required
def stats():
    # login is required for this endpoint for security
    t = translate_file_input()  # static context
    return flask.render_template(
        "stats.html",
        chartcorelink=flask.url_for('static', filename='chartcore.min.js'),
        piechartextlink=flask.url_for('static', filename='piechart.min.js'),
        stylesheetlink=flask.url_for('static', filename='dash.css'),
        data=t,
        overallcount=t["all"],
        show_byfilename=t["display"]["by-file-name"],
        show_byreponame=t["display"]["by-repo-name"],
        show_byfiletype=t["display"]["by-file-type"]
    )


# if file is being run directly, let's get this show on the road:
if __name__ == "__main__":
    app.run("127.0.0.1")
