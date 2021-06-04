from flask import Flask
from api.base import base_api
from api.aggregate import aggregate_api

app = Flask(__name__)

app.register_blueprint(base_api, url_prefix='/api')
app.register_blueprint(aggregate_api, url_prefix='/api/aggregate')

@app.route("/")
def index():
    return "Welcome to the Housing Passport API"