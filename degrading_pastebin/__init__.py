from flask import Flask

app = Flask(__name__)


@app.after_request
def apply_headers(response):
    response.headers["Cache-Control"] = "no-cache"
    return response
