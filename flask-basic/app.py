from flask import Flask
from api.base import base_api

app = Flask(__name__)

app.register_blueprint(base_api, url_prefix='/api')

@app.route("/")
def index():
    return "Welcome to the Housing Passport API"