<h1 align="center">
  <img src="https://cloudrepo.io/assets/img/logo/square/CloudRepo-Square-Brand-Blue.png" alt="CloudRepo Logo">
</h1>

## Download Analytics :chart_with_upwards_trend:

Download analytics is a simple system to track artifact download counts, built on [Flask](https://palletsprojects.com/p/flask/) and [Annie](https://github.com/annieapp/annie) technologies.

## Setup :wrench:

### Server Setup :hammer:

To set this up, you will first need to host the server. If you know how to do this, go right ahead.  Otherwise, use a hosting provider ([PythonAnywhere :link:](https://pythonanywhere.com) is great for this) to set it up simply.

If you do end up using PythonAnywhere (its free), you can easily create a web app (select `Flask` and the [*newest* version of Python](https://www.python.org/downloads/) when prompted), and than you can simply delete the hello world template and paste in the `server.py` in this repository, and reload your app. You should be good).

### CloudRepo Setup :pick:

After completing the server setup, you will need to head on over to CloudRepo and create a webhook.  You will want to follow [this guide](https://www.cloudrepo.io/docs/webhooks.html#creating-a-cloudrepo-webhook).

**Use these settings** :gear::

* Type: *JSON*
* Trigger On:
  * *Download*: Yes
  * *Upload*: No
  * *Delete*: No
* URL: This will be dynamic based on the URL of your instance, but will follow the basic pattern of `https://{SERVER_URL}/callback`

-------

*This guide will be completed soon*
