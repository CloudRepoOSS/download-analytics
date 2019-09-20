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

You should have the server set up properly if you followed these steps correctly.

### Configuration :woman_mechanic:

> **Note: when you start the server for the first time, wait for it to boot and start listening, and shut it down after this. It needs to be configured as described in this section!**

After running the server, if all went well, a `save.json` file should have been created in the server's working directory. You will want to open it up with a text editor.

In the text editor, you can tweak these settings:

* :warning: Warning: ***Do not*** modify the `all`, `repos`, or `downloads` fields. They are critical to the analytics and can cause errors. Please leave them alone.
* `users` field - you can change this to add or remove users that are authorized to view the analytics. You will need at least one user to log in (duh!), and you can add more using the simple format of `"username": password`. To make the JSON valid, you will need to put a comma at the end of the line if there is another user below that one.

Once you are done, you can save the file and reboot the server.
You can modify the file at any time by re-doing the steps above.

## Issues :rotating_light:

Found a bug? Want a feature added? [Open an issue!](https://github.com/CloudRepoOSS/download-analytics/issues)

## Code of Conduct :page_with_curl:

Please follow the [code of conduct](https://cloudrepooss.github.io/download-analytics/CODE_OF_CONDUCT) when contributing to make the contributing experience for everyone.

## Contributing :computer:

Want to contribute? Please do! We love contributions.

You can take a look at our open [issues](https://github.com/CloudRepoOSS/download-analytics/issues) or [projects](https://github.com/CloudRepoOSS/download-analytics/projects) for things that need to get done.
