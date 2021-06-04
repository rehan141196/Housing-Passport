from flask import Blueprint, jsonify, request
import boto3
import requests
from boto3.dynamodb.conditions import Key

aggregate_api = Blueprint("api/aggregate", __name__)

@aggregate_api.route("/")
def hello():
    return jsonify({"response": "Welcome to the Housing Passport API for aggregation"})

@aggregate_api.route("/by_wall_insulation")
def aggregate_by_wall_insulation():
    args = request.args.to_dict() # query should have post town

    if 'post_town' not in args:
        return jsonify({"response": "No post town provided", "args": args})

    post_town = args['post_town']

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')

    scan_kwargs = {
        'FilterExpression': Key('post_town').eq(post_town),
        'ProjectionExpression': "address, wall_insulation"
    }

    done = False
    start_key = None
    total_count = 0
    insulated_count = 0
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        results = response.get('Items', [])
        for result in results:
        	if result['wall_insulation'] == 'True':
        		insulated_count = insulated_count + 1
        total_count = total_count + response['Count']
        print("Homes in Post Town Count = ", total_count)
        print("Insulated Count = ", insulated_count)
        print("Scanned Count = ", response['ScannedCount'])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    return jsonify({"response": "Successfully scanned DB", "Homes in Post Town": total_count, "Insulated Homes": insulated_count, "Non-insulated homes": total_count-insulated_count})