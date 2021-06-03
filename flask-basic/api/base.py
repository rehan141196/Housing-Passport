from flask import Blueprint, jsonify, request
import boto3
import requests
from boto3.dynamodb.conditions import Key

base_api = Blueprint("api", __name__)

@base_api.route("/")
def hello():
    return jsonify({"response": "Welcome to the Housing Passport API"})

@base_api.route("/getrecord")
def getrecord():
    args = request.args.to_dict() # query should have argument with username being the key

    if 'username' not in args:
        return jsonify({"response": "No username provided", "args": args})

    user = args['username']

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        KeyConditionExpression=Key('username').eq(user)
    )

    if not response['Items']:
    	return jsonify({"response": "No data found for this user"})

    result = response['Items'][0]
    for item in result:
    	result[item] = str(result[item])

    return jsonify({"response": "Data found for user", "data": result})

@base_api.route("/addrecord", methods=['POST'])
def addrecord():
    data = request.form.to_dict()

    # if EPC cert key is present use that to query EPC API
    EPC_data = {}
    if 'EPC_cert_key' in data and data['EPC_cert_key'] != None:
        EPC_data = search_EPC_by_key(data['EPC_cert_key'])
    else:
        EPC_data = search_EPC_by_address(data['address'], data['postcode'])

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.put_item(Item=data)

    flags = {
        "Property_Type_Mismatch": False,
        "Age_Mismatch": False,
        "Rooms_Mismatch": False,
        "Roof_Mismatch": False,
        "Wall_Type_Mismatch": False,
        "Wall_Insulation_Mismatch": False,
        "Hotwater_Mismatch": False,
        "Floor_Type_Mismatch": False,
        "Floor_Insulation_Mismatch": False,
        "Glaze_Type_Mismatch": False,
        "Gas_Connection_Mismatch": False,
        "Heating_Type_Mismatch": False,
        "Heating_Fuel_Mismatch": False,
        "Thermostat_Mismatch": False,
        "Solar_Water_Heating_Mismatch": False,
        "Low_Energy_Light_Mismatch": False
    }

    if data['type'].lower() != EPC_data['property-type'].lower():
        flags['Property Type Mismatch'] = True
    if data['age'] not in EPC_data['construction-age-band']:
        flags['Age_Mismatch'] = True
    if str(data['bedrooms']) != EPC_data['number-habitable-rooms']:
        flags['Rooms_Mismatch'] = True
    if data['roof_type'].lower() != EPC_data['roof-description'].lower():
        flags['Roof_Mismatch'] = True
    if data['wall_type'].lower() not in EPC_data['walls-description'].lower():
        flags['Wall_Type_Mismatch'] = True
    if (data['wall_insulation'] == True and 'insulated' not in EPC_data['walls-description']) or (data['wall_insulation'] == False and 'insulated' in EPC_data['walls-description']):
        flags['Wall_Insulation_Mismatch'] = True
    if data['hotwater_type'].lower() not in EPC_data['hotwater-description'].lower():
        flags['Hotwater_Mismatch'] = True
    if data['floor_type'].lower() not in EPC_data['floor-description'].lower():
        flags['Floor_Type_Mismatch'] = True
    if (data['floor_insulation'] == True and 'insulated' not in EPC_data['floor-description']) or (data['floor_insulation'] == False and 'insulated' in EPC_data['floor-description']):
        flags['Floor_Insulation_Mismatch'] = True
    if data['glaze_type'].lower() not in EPC_data['glazed-type'].lower():
        flags['Glaze_Type_Mismatch'] = True
    if (data['gas_connection'] == True and EPC_data['mains-gas-flag'] != 'Y') or (data['gas_connection'] == False and EPC_data['mains-gas-flag'] == 'Y'):
        flags['Gas_Connection_Mismatch'] = True
    if data['heating_type'].lower() not in EPC_data['mainheat-description'].lower():
        flags['Heating_Type_Mismatch'] = True
    if data['heating_fuel'].lower() not in EPC_data['main-fuel'].lower():
        flags['Heating_Fuel_Mismatch'] = True
    if (data['thermostat'] == True and 'thermostat' not in EPC_data['mainheatcont-description']) or (data['thermostat'] == False and 'thermostat' in EPC_data['mainheatcont-description']):
        flags['Thermostat_Mismatch'] = True
    if (data['solar_water_heating'] == True and EPC_data['solar-water-heating-flag'] != 'Y') or (data['solar_water_heating'] == False and EPC_data['solar-water-heating-flag'] == 'Y'):
        flags['Solar_Water_Heating_Mismatch'] = True
    if str(data['low_energy_light_pct']) != EPC_data['low-energy-lighting']:
        flags['Low_Energy_Light_Mismatch'] = True

    return jsonify({"response": "Added entry to DB", "args": data, "mismatch-flags": flags})

def search_EPC_by_address(address, postcode):
    url = "https://epc.opendatacommunities.org/api/v1/domestic/search"
    parameters = {'address': address,
                  'postcode': postcode}
    head = {'Authorization': 'Basic cmtzMjBAaWMuYWMudWs6MjE0NzM0YjFkYzY5ZjI2Nzc1ZDFmZDZlYzY4ODY0ZGIxYzY1MmNhYQ==',
            'Accept': 'application/json'}

    r = requests.get(url=url, params=parameters, headers=head)
    data = r.json()

    return data['rows'][0]

def search_EPC_by_key(cert_key):
    url = "https://epc.opendatacommunities.org/api/v1/domestic/certificate/" + str(cert_key)
    head = {'Authorization': 'Basic cmtzMjBAaWMuYWMudWs6MjE0NzM0YjFkYzY5ZjI2Nzc1ZDFmZDZlYzY4ODY0ZGIxYzY1MmNhYQ==',
            'Accept': 'application/json'}

    r = requests.get(url=url, headers=head)
    data = r.json()

    return data['rows'][0]

@base_api.route("/deleterecord", methods=['POST'])
def deleterecord():
    args = request.form.to_dict()

    if 'username' not in args or 'address' not in args:
        return jsonify({"response": "No username/address provided", "args": args})

    user = args['username']
    address = args['address']

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        KeyConditionExpression = Key('username').eq(user) & Key('address').eq(address)
    )

    if not response['Items']:
        return jsonify({"response": "Record not found"})

    response = table.delete_item(
        Key={
            'username': user,
            'address': address
        }
    )

    return jsonify({"response": "Deleted entry in DB"})

@base_api.route("/getrecordbyaddress")
def getrecordbyaddress():
    args = request.args.to_dict() # query should have argument with address being the key

    if 'address' not in args:
        return jsonify({"response": "No address provided", "args": args})

    address = args['address']

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        IndexName='By_Address',
        KeyConditionExpression=Key('address').eq(address)
    )

    if not response['Items']:
        return jsonify({"response": "No data found for this address"})
    result = response['Items'][0]
    for item in result:
        result[item] = str(result[item])

    return jsonify({"response": "Data found for address", "data": result})