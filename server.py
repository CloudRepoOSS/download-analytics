import flask
import logging
import sys

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

common_methods = [
    "GET",
    "POST",
    "HEAD"
]

# homepage
@app.route("/", methods=common_methods)
def homepage():
    return flask.Response(
        "Welcome to this CloudRepo download counting server!",
        mimetype="text/plain"
    )


# if file is being run directly instead of being imported, run this:
if __name__ == "__main__":
    app.run("127.0.0.1")
