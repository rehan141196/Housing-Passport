from flask import Blueprint, jsonify, request
import boto3
import requests
from boto3.dynamodb.conditions import Key

from authentication import requires_auth, AuthError

aggregate_api = Blueprint("api/aggregate", __name__)

@aggregate_api.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Error handling for incorrect authentication
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@aggregate_api.route("/")
def hello():
    """
    Landing page for Aggregation API
    """
    return jsonify({"response": "Welcome to the Housing Passport API for aggregation"})

@aggregate_api.route("/by_field")
@requires_auth
def aggregate_by_field():
    """
    Aggregate data by specified field
    Must have post_town and field as query parameters
    """
    args = request.args.to_dict() # query should have post town

    if 'post_town' not in args or 'field' not in args:
        return jsonify({"response": "No post town or field provided", "args": args})

    post_town = args['post_town']
    field = args['field']

    # scan Dynamo DB table for all homes in post town
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')

    # type is a reserved keyword so we need to add an expression attribute
    scan_kwargs = {
        'FilterExpression': Key('post_town').eq(post_town),
        'ProjectionExpression': "address, #t",
        'ExpressionAttributeNames': {'#t': field}
    }

    # include pagination if result size exceeds 1 MB
    done = False
    start_key = None
    total_count = 0
    aggregate = {}
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        results = response.get('Items', [])
        for result in results:
            if result[field].lower() not in aggregate:
                aggregate[result[field].lower()] = 1
            else:
                aggregate[result[field].lower()] += 1
        total_count = total_count + response['Count']
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    aggregate["Homes in Post Town"] = total_count
        
    return jsonify({"response": "Successfully scanned DB", "results": aggregate})
