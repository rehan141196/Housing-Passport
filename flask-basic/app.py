from flask import Flask
from flask_cors import CORS, cross_origin
from api.base import base_api
from api.aggregate import aggregate_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(base_api, url_prefix='/api')
app.register_blueprint(aggregate_api, url_prefix='/api/aggregate')

@app.route("/")
def index():
    """
    Landing page for API
    """
    return "Welcome to the Housing Passport API"