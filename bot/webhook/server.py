import os

from flask import Flask
from .controllers import construct_blueprint
from telegram.ext import Application

app = Flask(__name__)


def run_webserver(application: Application):
    host = os.environ.get("WEBHOOK_HOST", "localhost")
    port = str(os.environ.get("WEBHOOK_PORT", 5000))
    bp = construct_blueprint(application)
    app.register_blueprint(
        bp,
        url_prefix="/api/v1",
    )
    app.run(host=host, port=port)
