import flask
import logging
import sys
import os
import json
from flask_httpauth import HTTPBasicAuth
from filehandlers import AbstractFile, FileManipulator, OpenModes
from textwrap import dedent

# init app
app = flask.Flask(__name__)
auth = HTTPBasicAuth()

app.logger.info("""
--------      CloudRepo Download Analytics Server v2.0.0     --------

                    Under the Apache v2.0 license.
            https://github.com/CloudRepoOSS/download-analytics

---------------------------------------------------------------------
""")

json_template = {
    "all": 0,
    "downloads": {},
    "repos": {},
    "types": {
        "jar": 0,
        "pom": 0,
        "crypto": 0,
        "other": 0
    },
    "users": {
        # format: "username": "password"
        "admin": "admin123"
        # please change this in your save file, this is super insecure !!
    }
}

# Save file creation
if not os.path.exists("save.json"):
    globaljson = AbstractFile("save.json")
    globaljson.touch()
    jsonmanip = FileManipulator(globaljson)
    jsonmanip.write_to_file(
        json.dumps(json_template)
    )

common_methods: list = [
    "GET",
    "POST"
]


def update_save_file(arraydict: dict):
    """Writes the passed dictionary to the save file."""

    open("save.json", mode=OpenModes.WRITE.value).write(json.dumps(arraydict))


@auth.error_handler
def auth_error():
    """View to be displayed when the user inputs invalid credentials."""

    app.logger.warning(
        "A user has triggered access denied - potential unauthorized login detected"
    )
    return "Access Denied!", 401


@auth.verify_password
def verify_password(username, password):
    """
    Verify the user-inputted credentials.

    :param username: the username inputted
    :param password: the password inputted
    :return: if the credentials are correct
    :rtype: bool
    """

    conf = translate_file_input()
    if username in conf["users"]:
        # username is in the config, check if password is right
        return conf["users"][username] == password

    # username is not in the config
    return False


# homepage
@app.route("/", methods=common_methods)
def homepage() -> flask.Response:
    """Homepage/greeting view."""

    return flask.Response(
        dedent("""\
        Welcome to this CloudRepo download analytics server.
        If you are an administrator, you can visit /stats to see the analytics.
        """),
        mimetype="text/plain"
    )


@app.route("/callback", methods=["POST"])
def webhook_callback() -> flask.Response:
    """Webhook callback endpoint."""

    reqdata: dict = translate(flask.request.data)

    conf = translate_file_input()
    conf["all"] = conf["all"] + 1

    try:
        conf["downloads"][reqdata["file-name"]] += 1
    except KeyError:
        conf["downloads"][reqdata["file-name"]] = 1
    try:
        conf["repos"][reqdata["repository-id"]] += 1
    except KeyError:
        conf["repos"][reqdata["repository-id"]] = 1

    # have this logic first to prevent file names like .jar.sha256
    if "sha" in reqdata["filename"] or "md5" in reqdata["filename"]:
        conf["types"]["crypto"] += 1
        # exit early, since we have saved all needed data by now
        update_save_file(conf)
        return flask.Response(
            json.dumps({
                "success": True
            }),
            mimetype="application/json"
        )

    if "pom" in reqdata["filename"]:
        conf["types"]["pom"] += 1
    elif ".jar" in reqdata["filename"]:
        conf["types"]["jar"] += 1
    else:
        conf["other"] += 1

    update_save_file(conf)

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
    """Loads the raw bytes of the save file, and translates them to a dict."""
    return translate(FileManipulator(AbstractFile('save.json')).get_cache()[0])


@app.route("/stats", methods=common_methods)
@auth.login_required
def stats():
    # login is required for this endpoint for security
    return flask.render_template(
        "stats.html",
        data=translate_file_input()
    )


# if file is being run directly, let's get this show on the road:
if __name__ == "__main__":
    app.run("127.0.0.1")
