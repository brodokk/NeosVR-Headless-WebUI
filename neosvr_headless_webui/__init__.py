from flask import Flask, redirect, render_template, session, url_for

from os import path
from base64 import b64encode

import logging

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    if app.config["LOG_FILE"]:
        rl = logging.getLogger()
        rl.setLevel("INFO")
        hdlr = logging.FileHandler(app.config["LOG_FILE"])
        fmt = logging.Formatter(
            fmt="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        hdlr.setFormatter(fmt)
        hdlr.addFilter(logging.Filter("neosvr_headless_webui"))
        rl.addHandler(hdlr)

    logo_path = path.join(app.instance_path, app.config["APP_LOGO"])
    if path.exists(logo_path):
        with open(logo_path, "rb") as logo_fp:
            logo_data = b64encode(logo_fp.read()).decode("ascii")
            app.config["APP_LOGO_DATA"] = logo_data

    @app.route("/")
    def index():
        if "user" in session:
            return redirect(url_for("dashboard.dashboard"))
        return render_template("index.html")

    from . import db
    db.init_app(app)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import account
    app.register_blueprint(account.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)

    from . import client
    app.register_blueprint(client.bp)

    return app
