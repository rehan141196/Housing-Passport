from flask import Blueprint, jsonify, request
import boto3
import requests
from boto3.dynamodb.conditions import Key
from authentication import requires_auth, AuthError
import subprocess
import json

base_api = Blueprint("api", __name__)

@base_api.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Error handling for incorrect authentication
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@base_api.route("/")
def hello():
    """
    Landing page for API
    """
    return jsonify({"response": "Welcome to the Housing Passport API"})

@base_api.route("/getrecord")
@requires_auth
def getrecord():
    """
    Retrieve record from DB by username
    Must have username as a query parameter
    """
    args = request.args.to_dict() # query should have username

    if 'username' not in args:
        return jsonify({"response": "No username provided", "args": args})

    user = args['username']

    # Dynamo DB query to return results with a particular username
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        KeyConditionExpression=Key('username').eq(user)
    )

    if not response['Items']:
        return jsonify({"response": "No data found for this user"})

    # convert results to string
    result = response['Items'][0]
    for item in result:
        result[item] = str(result[item])

    return jsonify({"response": "Data found for user", "data": result})

@base_api.route("/addrecord", methods=['POST'])
@requires_auth
def addrecord():
    """
    Add record to DB using a POST request and compare with EPC API
    """
    data = request.form.to_dict()

    # if EPC cert key is present use that to query EPC API, else use address
    EPC_data = {}
    if 'EPC_cert_key' in data and data['EPC_cert_key'] != None:
        EPC_data = search_EPC_by_key(data['EPC_cert_key'])
    else:
        EPC_data = search_EPC_by_address(data['address'], data['postcode'])

    # add record to DB (might move this to end)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.put_item(Item=data)

    # record does not exist in EPC API
    if not EPC_data:
        return jsonify({"response": "Added entry to DB, did not find matching record in EPC API", "args": data})

    # check for mismatches between user entered data and data from EPC API
    flags = {
        "Property_Type_Mismatch": False,
        "Age_Mismatch": False,
        "Rooms_Mismatch": False,
        "Roof_Mismatch": False,
        "Roof_Insulation_Mismatch": False,
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
    if data['age'].lower() not in EPC_data['construction-age-band'].lower():
        flags['Age_Mismatch'] = True
    if str(data['bedrooms']) not in EPC_data['number-habitable-rooms']:
        flags['Rooms_Mismatch'] = True
    if data['roof_type'].lower() not in EPC_data['roof-description'].lower():
        flags['Roof_Mismatch'] = True

    # Check for roof insulation
    if data['roof_insulation'] == 'True' and ('no insulation' in EPC_data['roof-description'].lower() or 'limited' in EPC_data['roof-description'].lower()):
        flags['Roof_Insulation_Mismatch'] = True
    elif data['roof_insulation'] == 'Limited' and 'limited' not in EPC_data['roof-description'].lower():
        flags['Roof_Insulation_Mismatch'] = True
    elif data['roof_insulation'] == 'False' and 'no insulation' not in EPC_data['roof-description'].lower() and 'another' not in EPC_data['roof-description'].lower():
        flags['Roof_Insulation_Mismatch'] = True

    if data['wall_type'].lower() not in EPC_data['walls-description'].lower():
        flags['Wall_Type_Mismatch'] = True

    # Check for wall insulation
    if data['wall_insulation'] == 'True' and ('no insulation' in EPC_data['walls-description'].lower() or 'partial' in EPC_data['walls-description'].lower()):
        flags['Wall_Insulation_Mismatch'] = True
    elif data['wall_insulation'] == 'Partial' and 'partial' not in EPC_data['walls-description'].lower():
        flags['Wall_Insulation_Mismatch'] = True
    elif data['wall_insulation'] == 'False' and 'no insulation' not in EPC_data['walls-description'].lower():
        flags['Wall_Insulation_Mismatch'] = True


    if data['hotwater_type'].lower() not in EPC_data['hotwater-description'].lower():
        flags['Hotwater_Mismatch'] = True
    if data['floor_type'].lower() not in EPC_data['floor-description'].lower():
        flags['Floor_Type_Mismatch'] = True

    # Check for floor insulation
    if data['floor_insulation'] == 'True' and ('no insulation' in EPC_data['floor-description'].lower() or 'limited' in EPC_data['floor-description'].lower()):
        flags['Floor_Insulation_Mismatch'] = True
    elif data['floor_insulation'] == 'Limited' and 'limited' not in EPC_data['floor-description'].lower():
        flags['Floor_Insulation_Mismatch'] = True
    elif data['floor_insulation'] == 'False' and 'no insulation' not in EPC_data['floor-description'].lower() and 'another' not in EPC_data['floor-description'].lower():
        flags['Floor_Insulation_Mismatch'] = True

    if data['glaze_type'].lower() not in EPC_data['glazed-type'].lower() and data['glaze_type'].lower() not in EPC_data['windows-description'].lower():
        flags['Glaze_Type_Mismatch'] = True
    if (data['gas_connection'] == 'True' and EPC_data['mains-gas-flag'] != 'Y') or (data['gas_connection'] == 'False' and EPC_data['mains-gas-flag'] == 'Y'):
        flags['Gas_Connection_Mismatch'] = True
    if data['heating_type'].lower() not in EPC_data['mainheat-description'].lower():
        flags['Heating_Type_Mismatch'] = True

    # Check for heating fuel 
    if data['heating_fuel'].lower() not in EPC_data['main-fuel'].lower():
        flags['Heating_Fuel_Mismatch'] = True

    # Check for thermostat
    if data['thermostat'] == 'True' and 'thermostat' not in EPC_data['mainheatcont-description']:
        flags['Thermostat_Mismatch'] = True
    elif data['thermostat'] == 'True' and 'no' in EPC_data['mainheatcont-description'] and 'thermostat' in EPC_data['mainheatcont-description']:
        flags['Thermostat_Mismatch'] = True
    elif data['thermostat'] == 'False' and ('no' not in EPC_data['mainheatcont-description'] or 'thermostat' not in EPC_data['mainheatcont-description']):
        flags['Thermostat_Mismatch'] = True
    elif data['thermostat'] == 'Other' and 'thermostat' in EPC_data['mainheatcont-description']:
        flags['Thermostat_Mismatch'] = True
    
    if (data['solar_water_heating'] == 'True' and EPC_data['solar-water-heating-flag'] != 'Y') or (data['solar_water_heating'] == 'False' and EPC_data['solar-water-heating-flag'] == 'Y'):
        flags['Solar_Water_Heating_Mismatch'] = True
    if str(data['low_energy_light_pct']) != EPC_data['low-energy-lighting']:
        flags['Low_Energy_Light_Mismatch'] = True

    return jsonify({"response": "Added entry to DB", "args": data, "mismatch-flags": flags})

def search_EPC_by_address(address, postcode):
    """
    Utility function to search EPC API by address
    """
    url = "https://epc.opendatacommunities.org/api/v1/domestic/search"
    parameters = {'address': address,
                  'postcode': postcode}
    head = {'Authorization': 'Basic cmtzMjBAaWMuYWMudWs6MjE0NzM0YjFkYzY5ZjI2Nzc1ZDFmZDZlYzY4ODY0ZGIxYzY1MmNhYQ==',
            'Accept': 'application/json'}

    r = requests.get(url=url, params=parameters, headers=head)

    # EPC API gives empty response if address is not found
    if not r.text:
        return {}

    data = r.json()

    return data['rows'][0]

def search_EPC_by_key(cert_key):
    """
    Utility function to search EPC API by LMK key
    """
    url = "https://epc.opendatacommunities.org/api/v1/domestic/certificate/" + str(cert_key)
    head = {'Authorization': 'Basic cmtzMjBAaWMuYWMudWs6MjE0NzM0YjFkYzY5ZjI2Nzc1ZDFmZDZlYzY4ODY0ZGIxYzY1MmNhYQ==',
            'Accept': 'application/json'}

    r = requests.get(url=url, headers=head)

    # EPC API gives 404 error if LMK key does not exist
    if r.status_code != requests.codes.ok:
        return {}

    data = r.json()

    return data['rows'][0]

@base_api.route("/deleterecord", methods=['POST'])
@requires_auth
def deleterecord():
    """
    Delete record from DB
    Requires username and address
    """
    args = request.form.to_dict()

    if 'username' not in args or 'address' not in args:
        return jsonify({"response": "No username/address provided", "args": args})

    user = args['username']
    address = args['address']

    # find record in DB
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        KeyConditionExpression = Key('username').eq(user) & Key('address').eq(address)
    )

    if not response['Items']:
        return jsonify({"response": "Record not found"})

    # delete record
    response = table.delete_item(
        Key={
            'username': user,
            'address': address
        }
    )

    return jsonify({"response": "Deleted entry in DB"})

@base_api.route("/getrecordbyaddress")
@requires_auth
def getrecordbyaddress():
    """
    Retrieve record from DB by address
    Must have address as a query parameter
    """
    args = request.args.to_dict() # query should have address

    if 'address' not in args:
        return jsonify({"response": "No address provided", "args": args})

    address = args['address']

    # Dynamo DB query to return results with a particular address
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Residences')
    response = table.query(
        IndexName='By_Address',
        KeyConditionExpression=Key('address').eq(address)
    )

    if not response['Items']:
        return jsonify({"response": "No data found for this address"})


    # convert results to string
    result = response['Items'][0]
    for item in result:
        result[item] = str(result[item])

    return jsonify({"response": "Data found for address", "data": result})

city_codes = {'HARTLEPOOL': 'E06000001', 'MIDDLESBROUGH': 'E06000002', 'REDCAR AND CLEVELAND': 'E06000003', 'STOCKTON ON TEES': 'E06000004', 'DARLINGTON': 'E06000005', 'HALTON': 'E06000006', 'WARRINGTON': 'E06000007', 'BLACKBURN WITH DARWEN': 'E06000008', 'BLACKPOOL': 'E06000009', 'KINGSTON UPON HULL CITY OF': 'E06000010', 'EAST RIDING OF YORKSHIRE': 'E06000011', 'NORTH EAST LINCOLNSHIRE': 'E06000012', 'NORTH LINCOLNSHIRE': 'E06000013', 'YORK': 'E06000014', 'DERBY': 'E06000015', 'LEICESTER': 'E06000016', 'RUTLAND': 'E06000017', 'NOTTINGHAM': 'E06000018', 'HEREFORDSHIRE COUNTY OF': 'E06000019', 'TELFORD AND WREKIN': 'E06000020', 'STOKE ON TRENT': 'E06000021', 'BATH AND NORTH EAST SOMERSET': 'E06000022', 'BRISTOL CITY OF': 'E06000023', 'NORTH SOMERSET': 'E06000024', 'SOUTH GLOUCESTERSHIRE': 'E06000025', 'PLYMOUTH': 'E06000026', 'TORBAY': 'E06000027', 'SWINDON': 'E06000030', 'PETERBOROUGH': 'E06000031', 'LUTON': 'E06000032', 'SOUTHEND ON SEA': 'E06000033', 'THURROCK': 'E06000034', 'MEDWAY': 'E06000035', 'BRACKNELL FOREST': 'E06000036', 'WEST BERKSHIRE': 'E06000037', 'READING': 'E06000038', 'SLOUGH': 'E06000039', 'WINDSOR AND MAIDENHEAD': 'E06000040', 'WOKINGHAM': 'E06000041', 'MILTON KEYNES': 'E06000042', 'BRIGHTON AND HOVE': 'E06000043', 'PORTSMOUTH': 'E06000044', 'SOUTHAMPTON': 'E06000045', 'ISLE OF WIGHT': 'E06000046', 'COUNTY DURHAM': 'E06000047', 'CHESHIRE EAST': 'E06000049', 'CHESHIRE WEST AND CHESTER': 'E06000050', 'SHROPSHIRE': 'E06000051', 'CORNWALL': 'E06000052', 'ISLES OF SCILLY': 'E06000053', 'WILTSHIRE': 'E06000054', 'BEDFORD': 'E06000055', 'CENTRAL BEDFORDSHIRE': 'E06000056', 'NORTHUMBERLAND': 'E06000057', 'BOURNEMOUTH CHRISTCHURCH AND POOLE': 'E06000058', 'DORSET': 'E06000059', 'AYLESBURY VALE': 'E07000004', 'CHILTERN': 'E07000005', 'SOUTH BUCKS': 'E07000006', 'WYCOMBE': 'E07000007', 'CAMBRIDGE': 'E07000008', 'EAST CAMBRIDGESHIRE': 'E07000009', 'FENLAND': 'E07000010', 'HUNTINGDONSHIRE': 'E07000011', 'SOUTH CAMBRIDGESHIRE': 'E07000012', 'ALLERDALE': 'E07000026', 'BARROW IN FURNESS': 'E07000027', 'CARLISLE': 'E07000028', 'COPELAND': 'E07000029', 'EDEN': 'E07000030', 'SOUTH LAKELAND': 'E07000031', 'AMBER VALLEY': 'E07000032', 'BOLSOVER': 'E07000033', 'CHESTERFIELD': 'E07000034', 'DERBYSHIRE DALES': 'E07000035', 'EREWASH': 'E07000036', 'HIGH PEAK': 'E07000037', 'NORTH EAST DERBYSHIRE': 'E07000038', 'SOUTH DERBYSHIRE': 'E07000039', 'EAST DEVON': 'E07000040', 'EXETER': 'E07000041', 'MID DEVON': 'E07000042', 'NORTH DEVON': 'E07000043', 'SOUTH HAMS': 'E07000044', 'TEIGNBRIDGE': 'E07000045', 'TORRIDGE': 'E07000046', 'WEST DEVON': 'E07000047', 'EASTBOURNE': 'E07000061', 'HASTINGS': 'E07000062', 'LEWES': 'E07000063', 'ROTHER': 'E07000064', 'WEALDEN': 'E07000065', 'BASILDON': 'E07000066', 'BRAINTREE': 'E07000067', 'BRENTWOOD': 'E07000068', 'CASTLE POINT': 'E07000069', 'CHELMSFORD': 'E07000070', 'COLCHESTER': 'E07000071', 'EPPING FOREST': 'E07000072', 'HARLOW': 'E07000073', 'MALDON': 'E07000074', 'ROCHFORD': 'E07000075', 'TENDRING': 'E07000076', 'UTTLESFORD': 'E07000077', 'CHELTENHAM': 'E07000078', 'COTSWOLD': 'E07000079', 'FOREST OF DEAN': 'E07000080', 'GLOUCESTER': 'E07000081', 'STROUD': 'E07000082', 'TEWKESBURY': 'E07000083', 'BASINGSTOKE AND DEANE': 'E07000084', 'EAST HAMPSHIRE': 'E07000085', 'EASTLEIGH': 'E07000086', 'FAREHAM': 'E07000087', 'GOSPORT': 'E07000088', 'HART': 'E07000089', 'HAVANT': 'E07000090', 'NEW FOREST': 'E07000091', 'RUSHMOOR': 'E07000092', 'TEST VALLEY': 'E07000093', 'WINCHESTER': 'E07000094', 'BROXBOURNE': 'E07000095', 'DACORUM': 'E07000096', 'HERTSMERE': 'E07000098', 'NORTH HERTFORDSHIRE': 'E07000099', 'THREE RIVERS': 'E07000102', 'WATFORD': 'E07000103', 'ASHFORD': 'E07000105', 'CANTERBURY': 'E07000106', 'DARTFORD': 'E07000107', 'DOVER': 'E07000108', 'GRAVESHAM': 'E07000109', 'MAIDSTONE': 'E07000110', 'SEVENOAKS': 'E07000111', 'FOLKESTONE AND HYTHE': 'E07000112', 'SWALE': 'E07000113', 'THANET': 'E07000114', 'TONBRIDGE AND MALLING': 'E07000115', 'TUNBRIDGE WELLS': 'E07000116', 'BURNLEY': 'E07000117', 'CHORLEY': 'E07000118', 'FYLDE': 'E07000119', 'HYNDBURN': 'E07000120', 'LANCASTER': 'E07000121', 'PENDLE': 'E07000122', 'PRESTON': 'E07000123', 'RIBBLE VALLEY': 'E07000124', 'ROSSENDALE': 'E07000125', 'SOUTH RIBBLE': 'E07000126', 'WEST LANCASHIRE': 'E07000127', 'WYRE': 'E07000128', 'BLABY': 'E07000129', 'CHARNWOOD': 'E07000130', 'HARBOROUGH': 'E07000131', 'HINCKLEY AND BOSWORTH': 'E07000132', 'MELTON': 'E07000133', 'NORTH WEST LEICESTERSHIRE': 'E07000134', 'OADBY AND WIGSTON': 'E07000135', 'BOSTON': 'E07000136', 'EAST LINDSEY': 'E07000137', 'LINCOLN': 'E07000138', 'NORTH KESTEVEN': 'E07000139', 'SOUTH HOLLAND': 'E07000140', 'SOUTH KESTEVEN': 'E07000141', 'WEST LINDSEY': 'E07000142', 'BRECKLAND': 'E07000143', 'BROADLAND': 'E07000144', 'GREAT YARMOUTH': 'E07000145', 'KING S LYNN AND WEST NORFOLK': 'E07000146', 'NORTH NORFOLK': 'E07000147', 'NORWICH': 'E07000148', 'SOUTH NORFOLK': 'E07000149', 'CORBY': 'E07000150', 'DAVENTRY': 'E07000151', 'EAST NORTHAMPTONSHIRE': 'E07000152', 'KETTERING': 'E07000153', 'NORTHAMPTON': 'E07000154', 'SOUTH NORTHAMPTONSHIRE': 'E07000155', 'WELLINGBOROUGH': 'E07000156', 'CRAVEN': 'E07000163', 'HAMBLETON': 'E07000164', 'HARROGATE': 'E07000165', 'RICHMONDSHIRE': 'E07000166', 'RYEDALE': 'E07000167', 'SCARBOROUGH': 'E07000168', 'SELBY': 'E07000169', 'ASHFIELD': 'E07000170', 'BASSETLAW': 'E07000171', 'BROXTOWE': 'E07000172', 'GEDLING': 'E07000173', 'MANSFIELD': 'E07000174', 'NEWARK AND SHERWOOD': 'E07000175', 'RUSHCLIFFE': 'E07000176', 'CHERWELL': 'E07000177', 'OXFORD': 'E07000178', 'SOUTH OXFORDSHIRE': 'E07000179', 'VALE OF WHITE HORSE': 'E07000180', 'WEST OXFORDSHIRE': 'E07000181', 'MENDIP': 'E07000187', 'SEDGEMOOR': 'E07000188', 'SOUTH SOMERSET': 'E07000189', 'CANNOCK CHASE': 'E07000192', 'EAST STAFFORDSHIRE': 'E07000193', 'LICHFIELD': 'E07000194', 'NEWCASTLE UNDER LYME': 'E07000195', 'SOUTH STAFFORDSHIRE': 'E07000196', 'STAFFORD': 'E07000197', 'STAFFORDSHIRE MOORLANDS': 'E07000198', 'TAMWORTH': 'E07000199', 'BABERGH': 'E07000200', 'IPSWICH': 'E07000202', 'MID SUFFOLK': 'E07000203', 'ELMBRIDGE': 'E07000207', 'EPSOM AND EWELL': 'E07000208', 'GUILDFORD': 'E07000209', 'MOLE VALLEY': 'E07000210', 'REIGATE AND BANSTEAD': 'E07000211', 'RUNNYMEDE': 'E07000212', 'SPELTHORNE': 'E07000213', 'SURREY HEATH': 'E07000214', 'TANDRIDGE': 'E07000215', 'WAVERLEY': 'E07000216', 'WOKING': 'E07000217', 'NORTH WARWICKSHIRE': 'E07000218', 'NUNEATON AND BEDWORTH': 'E07000219', 'RUGBY': 'E07000220', 'STRATFORD ON AVON': 'E07000221', 'WARWICK': 'E07000222', 'ADUR': 'E07000223', 'ARUN': 'E07000224', 'CHICHESTER': 'E07000225', 'CRAWLEY': 'E07000226', 'HORSHAM': 'E07000227', 'MID SUSSEX': 'E07000228', 'WORTHING': 'E07000229', 'BROMSGROVE': 'E07000234', 'MALVERN HILLS': 'E07000235', 'REDDITCH': 'E07000236', 'WORCESTER': 'E07000237', 'WYCHAVON': 'E07000238', 'WYRE FOREST': 'E07000239', 'ST ALBANS': 'E07000240', 'WELWYN HATFIELD': 'E07000241', 'EAST HERTFORDSHIRE': 'E07000242', 'STEVENAGE': 'E07000243', 'EAST SUFFOLK': 'E07000244', 'WEST SUFFOLK': 'E07000245', 'SOMERSET WEST AND TAUNTON': 'E07000246', 'BOLTON': 'E08000001', 'BURY': 'E08000002', 'MANCHESTER': 'E08000003', 'OLDHAM': 'E08000004', 'ROCHDALE': 'E08000005', 'SALFORD': 'E08000006', 'STOCKPORT': 'E08000007', 'TAMESIDE': 'E08000008', 'TRAFFORD': 'E08000009', 'WIGAN': 'E08000010', 'KNOWSLEY': 'E08000011', 'LIVERPOOL': 'E08000012', 'ST HELENS': 'E08000013', 'SEFTON': 'E08000014', 'WIRRAL': 'E08000015', 'BARNSLEY': 'E08000016', 'DONCASTER': 'E08000017', 'ROTHERHAM': 'E08000018', 'SHEFFIELD': 'E08000019', 'NEWCASTLE UPON TYNE': 'E08000021', 'NORTH TYNESIDE': 'E08000022', 'SOUTH TYNESIDE': 'E08000023', 'SUNDERLAND': 'E08000024', 'BIRMINGHAM': 'E08000025', 'COVENTRY': 'E08000026', 'DUDLEY': 'E08000027', 'SANDWELL': 'E08000028', 'SOLIHULL': 'E08000029', 'WALSALL': 'E08000030', 'WOLVERHAMPTON': 'E08000031', 'BRADFORD': 'E08000032', 'CALDERDALE': 'E08000033', 'KIRKLEES': 'E08000034', 'LEEDS': 'E08000035', 'WAKEFIELD': 'E08000036', 'GATESHEAD': 'E08000037', 'CITY OF LONDON': 'E09000001', 'BARKING AND DAGENHAM': 'E09000002', 'BARNET': 'E09000003', 'BEXLEY': 'E09000004', 'BRENT': 'E09000005', 'BROMLEY': 'E09000006', 'CAMDEN': 'E09000007', 'CROYDON': 'E09000008', 'EALING': 'E09000009', 'ENFIELD': 'E09000010', 'GREENWICH': 'E09000011', 'HACKNEY': 'E09000012', 'HAMMERSMITH AND FULHAM': 'E09000013', 'HARINGEY': 'E09000014', 'HARROW': 'E09000015', 'HAVERING': 'E09000016', 'HILLINGDON': 'E09000017', 'HOUNSLOW': 'E09000018', 'ISLINGTON': 'E09000019', 'KENSINGTON AND CHELSEA': 'E09000020', 'KINGSTON UPON THAMES': 'E09000021', 'LAMBETH': 'E09000022', 'LEWISHAM': 'E09000023', 'MERTON': 'E09000024', 'NEWHAM': 'E09000025', 'REDBRIDGE': 'E09000026', 'RICHMOND UPON THAMES': 'E09000027', 'SOUTHWARK': 'E09000028', 'SUTTON': 'E09000029', 'TOWER HAMLETS': 'E09000030', 'WALTHAM FOREST': 'E09000031', 'WANDSWORTH': 'E09000032', 'WESTMINSTER': 'E09000033', 'ISLE OF ANGLESEY': 'W06000001', 'GWYNEDD': 'W06000002', 'CONWY': 'W06000003', 'DENBIGHSHIRE': 'W06000004', 'FLINTSHIRE': 'W06000005', 'WREXHAM': 'W06000006', 'CEREDIGION': 'W06000008', 'PEMBROKESHIRE': 'W06000009', 'CARMARTHENSHIRE': 'W06000010', 'SWANSEA': 'W06000011', 'NEATH PORT TALBOT': 'W06000012', 'BRIDGEND': 'W06000013', 'VALE OF GLAMORGAN': 'W06000014', 'CARDIFF': 'W06000015', 'RHONDDA CYNON TAF': 'W06000016', 'CAERPHILLY': 'W06000018', 'BLAENAU GWENT': 'W06000019', 'TORFAEN': 'W06000020', 'MONMOUTHSHIRE': 'W06000021', 'NEWPORT': 'W06000022', 'POWYS': 'W06000023', 'MERTHYR TYDFIL': 'W06000024'}

@base_api.route("/predictefficiency", methods=['POST'])
def predict_efficiency():
    """
    Predict energy efficiency score for a house
    """
    data = request.form.to_dict()

    path = "./Pickle Models/" + city_codes[data["post_town"]] + ".pickle"

    new_row = {'PROPERTY_TYPE': data['type'], 'MAINS_GAS_FLAG': data['gas_connection'], 'GLAZED_TYPE': data['glaze_type'], 'NUMBER_HABITABLE_ROOMS': int(data['bedrooms']), 'LOW_ENERGY_LIGHTING': int(data['low_energy_light_pct']), 'HOTWATER_DESCRIPTION': data['hotwater_type'], 'FLOOR_DESCRIPTION': data['floor_type'], 'WALLS_DESCRIPTION': data['wall_insulation'], 'ROOF_DESCRIPTION': data['roof_type'], 'MAINHEAT_DESCRIPTION': data['heating_type'], 'MAINHEATCONT_DESCRIPTION': data['thermostat'], 'MAIN_FUEL': data['heating_fuel'], 'SOLAR_WATER_HEATING_FLAG': data['solar_water_heating'], 'CONSTRUCTION_AGE_BAND': data['age']}

    arg = json.dumps(new_row)

    x = subprocess.check_output(['python3', 'model_try.py', path, arg])

    efficiency = x.decode("utf-8")
    efficiency = efficiency.strip()

    return jsonify({"response": "Successfully predicted efficiency score", "efficiency_score": efficiency})