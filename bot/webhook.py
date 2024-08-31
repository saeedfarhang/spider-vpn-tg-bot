import os
from flask import Flask

app = Flask(__name__)


def run_webserver():
    host = os.environ.get("WEBHOOK_HOST", "localhost")
    port = str(os.environ.get("WEBHOOK_PORT", 5000))
    app.run(host=host, port=port)
