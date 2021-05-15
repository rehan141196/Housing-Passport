import pandas as pd
from collections import Counter
import csv
import re

global_current_rating = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "INVALID!": 0}
global_potential_rating = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "INVALID!": 0}
values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'INVALID!']

# list_of_files = ["testcerts1.csv", "testcerts2.csv"]

# list_of_files = [
# "domestic-E06000001-Hartlepool/certificates.csv",
# "domestic-E06000002-Middlesbrough/certificates.csv",
# "domestic-E06000003-Redcar-and-Cleveland/certificates.csv"]

list_of_files = [
"domestic-E06000001-Hartlepool/certificates.csv",
"domestic-E06000002-Middlesbrough/certificates.csv",
"domestic-E06000003-Redcar-and-Cleveland/certificates.csv",
"domestic-E06000004-Stockton-on-Tees/certificates.csv",
"domestic-E06000005-Darlington/certificates.csv",
"domestic-E06000006-Halton/certificates.csv",
"domestic-E06000007-Warrington/certificates.csv",
"domestic-E06000008-Blackburn-with-Darwen/certificates.csv",
"domestic-E06000009-Blackpool/certificates.csv",
"domestic-E06000010-Kingston-upon-Hull-City-of/certificates.csv",
"domestic-E06000011-East-Riding-of-Yorkshire/certificates.csv",
"domestic-E06000012-North-East-Lincolnshire/certificates.csv",
"domestic-E06000013-North-Lincolnshire/certificates.csv",
"domestic-E06000014-York/certificates.csv",
"domestic-E06000015-Derby/certificates.csv",
"domestic-E06000016-Leicester/certificates.csv",
"domestic-E06000017-Rutland/certificates.csv",
"domestic-E06000018-Nottingham/certificates.csv",
"domestic-E06000019-Herefordshire-County-of/certificates.csv",
"domestic-E06000020-Telford-and-Wrekin/certificates.csv",
"domestic-E06000021-Stoke-on-Trent/certificates.csv",
"domestic-E06000022-Bath-and-North-East-Somerset/certificates.csv",
"domestic-E06000023-Bristol-City-of/certificates.csv",
"domestic-E06000024-North-Somerset/certificates.csv",
"domestic-E06000025-South-Gloucestershire/certificates.csv",
"domestic-E06000026-Plymouth/certificates.csv",
"domestic-E06000027-Torbay/certificates.csv",
"domestic-E06000030-Swindon/certificates.csv",
"domestic-E06000031-Peterborough/certificates.csv",
"domestic-E06000032-Luton/certificates.csv",
"domestic-E06000033-Southend-on-Sea/certificates.csv",
"domestic-E06000034-Thurrock/certificates.csv",
"domestic-E06000035-Medway/certificates.csv",
"domestic-E06000036-Bracknell-Forest/certificates.csv",
"domestic-E06000037-West-Berkshire/certificates.csv",
"domestic-E06000038-Reading/certificates.csv",
"domestic-E06000039-Slough/certificates.csv",
"domestic-E06000040-Windsor-and-Maidenhead/certificates.csv",
"domestic-E06000041-Wokingham/certificates.csv",
"domestic-E06000042-Milton-Keynes/certificates.csv",
"domestic-E06000043-Brighton-and-Hove/certificates.csv",
"domestic-E06000044-Portsmouth/certificates.csv",
"domestic-E06000045-Southampton/certificates.csv",
"domestic-E06000046-Isle-of-Wight/certificates.csv",
"domestic-E06000047-County-Durham/certificates.csv",
"domestic-E06000049-Cheshire-East/certificates.csv",
"domestic-E06000050-Cheshire-West-and-Chester/certificates.csv",
"domestic-E06000051-Shropshire/certificates.csv",
"domestic-E06000052-Cornwall/certificates.csv",
"domestic-E06000053-Isles-of-Scilly/certificates.csv",
"domestic-E06000054-Wiltshire/certificates.csv",
"domestic-E06000055-Bedford/certificates.csv",
"domestic-E06000056-Central-Bedfordshire/certificates.csv",
"domestic-E06000057-Northumberland/certificates.csv",
"domestic-E06000058-Bournemouth-Christchurch-and-Poole/certificates.csv",
"domestic-E06000059-Dorset/certificates.csv",
"domestic-E07000004-Aylesbury-Vale/certificates.csv",
"domestic-E07000005-Chiltern/certificates.csv",
"domestic-E07000006-South-Bucks/certificates.csv",
"domestic-E07000007-Wycombe/certificates.csv",
"domestic-E07000008-Cambridge/certificates.csv",
"domestic-E07000009-East-Cambridgeshire/certificates.csv",
"domestic-E07000010-Fenland/certificates.csv",
"domestic-E07000011-Huntingdonshire/certificates.csv",
"domestic-E07000012-South-Cambridgeshire/certificates.csv",
"domestic-E07000026-Allerdale/certificates.csv",
"domestic-E07000027-Barrow-in-Furness/certificates.csv",
"domestic-E07000028-Carlisle/certificates.csv",
"domestic-E07000029-Copeland/certificates.csv",
"domestic-E07000030-Eden/certificates.csv",
"domestic-E07000031-South-Lakeland/certificates.csv",
"domestic-E07000032-Amber-Valley/certificates.csv",
"domestic-E07000033-Bolsover/certificates.csv",
"domestic-E07000034-Chesterfield/certificates.csv",
"domestic-E07000035-Derbyshire-Dales/certificates.csv",
"domestic-E07000036-Erewash/certificates.csv",
"domestic-E07000037-High-Peak/certificates.csv",
"domestic-E07000038-North-East-Derbyshire/certificates.csv",
"domestic-E07000039-South-Derbyshire/certificates.csv",
"domestic-E07000040-East-Devon/certificates.csv",
"domestic-E07000041-Exeter/certificates.csv",
"domestic-E07000042-Mid-Devon/certificates.csv",
"domestic-E07000043-North-Devon/certificates.csv",
"domestic-E07000044-South-Hams/certificates.csv",
"domestic-E07000045-Teignbridge/certificates.csv",
"domestic-E07000046-Torridge/certificates.csv",
"domestic-E07000047-West-Devon/certificates.csv",
"domestic-E07000061-Eastbourne/certificates.csv",
"domestic-E07000062-Hastings/certificates.csv",
"domestic-E07000063-Lewes/certificates.csv",
"domestic-E07000064-Rother/certificates.csv",
"domestic-E07000065-Wealden/certificates.csv",
"domestic-E07000066-Basildon/certificates.csv",
"domestic-E07000067-Braintree/certificates.csv",
"domestic-E07000068-Brentwood/certificates.csv",
"domestic-E07000069-Castle-Point/certificates.csv",
"domestic-E07000070-Chelmsford/certificates.csv",
"domestic-E07000071-Colchester/certificates.csv",
"domestic-E07000072-Epping-Forest/certificates.csv",
"domestic-E07000073-Harlow/certificates.csv",
"domestic-E07000074-Maldon/certificates.csv",
"domestic-E07000075-Rochford/certificates.csv",
"domestic-E07000076-Tendring/certificates.csv",
"domestic-E07000077-Uttlesford/certificates.csv",
"domestic-E07000078-Cheltenham/certificates.csv",
"domestic-E07000079-Cotswold/certificates.csv",
"domestic-E07000080-Forest-of-Dean/certificates.csv",
"domestic-E07000081-Gloucester/certificates.csv",
"domestic-E07000082-Stroud/certificates.csv",
"domestic-E07000083-Tewkesbury/certificates.csv",
"domestic-E07000084-Basingstoke-and-Deane/certificates.csv",
"domestic-E07000085-East-Hampshire/certificates.csv",
"domestic-E07000086-Eastleigh/certificates.csv",
"domestic-E07000087-Fareham/certificates.csv",
"domestic-E07000088-Gosport/certificates.csv",
"domestic-E07000089-Hart/certificates.csv",
"domestic-E07000090-Havant/certificates.csv",
"domestic-E07000091-New-Forest/certificates.csv",
"domestic-E07000092-Rushmoor/certificates.csv",
"domestic-E07000093-Test-Valley/certificates.csv",
"domestic-E07000094-Winchester/certificates.csv",
"domestic-E07000095-Broxbourne/certificates.csv",
"domestic-E07000096-Dacorum/certificates.csv",
"domestic-E07000098-Hertsmere/certificates.csv",
"domestic-E07000099-North-Hertfordshire/certificates.csv",
"domestic-E07000102-Three-Rivers/certificates.csv",
"domestic-E07000103-Watford/certificates.csv",
"domestic-E07000105-Ashford/certificates.csv",
"domestic-E07000106-Canterbury/certificates.csv",
"domestic-E07000107-Dartford/certificates.csv",
"domestic-E07000108-Dover/certificates.csv",
"domestic-E07000109-Gravesham/certificates.csv",
"domestic-E07000110-Maidstone/certificates.csv",
"domestic-E07000111-Sevenoaks/certificates.csv",
"domestic-E07000112-Folkestone-and-Hythe/certificates.csv",
"domestic-E07000113-Swale/certificates.csv",
"domestic-E07000114-Thanet/certificates.csv",
"domestic-E07000115-Tonbridge-and-Malling/certificates.csv",
"domestic-E07000116-Tunbridge-Wells/certificates.csv",
"domestic-E07000117-Burnley/certificates.csv",
"domestic-E07000118-Chorley/certificates.csv",
"domestic-E07000119-Fylde/certificates.csv",
"domestic-E07000120-Hyndburn/certificates.csv",
"domestic-E07000121-Lancaster/certificates.csv",
"domestic-E07000122-Pendle/certificates.csv",
"domestic-E07000123-Preston/certificates.csv",
"domestic-E07000124-Ribble-Valley/certificates.csv",
"domestic-E07000125-Rossendale/certificates.csv",
"domestic-E07000126-South-Ribble/certificates.csv",
"domestic-E07000127-West-Lancashire/certificates.csv",
"domestic-E07000128-Wyre/certificates.csv",
"domestic-E07000129-Blaby/certificates.csv",
"domestic-E07000130-Charnwood/certificates.csv",
"domestic-E07000131-Harborough/certificates.csv",
"domestic-E07000132-Hinckley-and-Bosworth/certificates.csv",
"domestic-E07000133-Melton/certificates.csv",
"domestic-E07000134-North-West-Leicestershire/certificates.csv",
"domestic-E07000135-Oadby-and-Wigston/certificates.csv",
"domestic-E07000136-Boston/certificates.csv",
"domestic-E07000137-East-Lindsey/certificates.csv",
"domestic-E07000138-Lincoln/certificates.csv",
"domestic-E07000139-North-Kesteven/certificates.csv",
"domestic-E07000140-South-Holland/certificates.csv",
"domestic-E07000141-South-Kesteven/certificates.csv",
"domestic-E07000142-West-Lindsey/certificates.csv",
"domestic-E07000143-Breckland/certificates.csv",
"domestic-E07000144-Broadland/certificates.csv",
"domestic-E07000145-Great-Yarmouth/certificates.csv",
"domestic-E07000146-King-s-Lynn-and-West-Norfolk/certificates.csv",
"domestic-E07000147-North-Norfolk/certificates.csv",
"domestic-E07000148-Norwich/certificates.csv",
"domestic-E07000149-South-Norfolk/certificates.csv",
"domestic-E07000150-Corby/certificates.csv",
"domestic-E07000151-Daventry/certificates.csv",
"domestic-E07000152-East-Northamptonshire/certificates.csv",
"domestic-E07000153-Kettering/certificates.csv",
"domestic-E07000154-Northampton/certificates.csv",
"domestic-E07000155-South-Northamptonshire/certificates.csv",
"domestic-E07000156-Wellingborough/certificates.csv",
"domestic-E07000163-Craven/certificates.csv",
"domestic-E07000164-Hambleton/certificates.csv",
"domestic-E07000165-Harrogate/certificates.csv",
"domestic-E07000166-Richmondshire/certificates.csv",
"domestic-E07000167-Ryedale/certificates.csv",
"domestic-E07000168-Scarborough/certificates.csv",
"domestic-E07000169-Selby/certificates.csv",
"domestic-E07000170-Ashfield/certificates.csv",
"domestic-E07000171-Bassetlaw/certificates.csv",
"domestic-E07000172-Broxtowe/certificates.csv",
"domestic-E07000173-Gedling/certificates.csv",
"domestic-E07000174-Mansfield/certificates.csv",
"domestic-E07000175-Newark-and-Sherwood/certificates.csv",
"domestic-E07000176-Rushcliffe/certificates.csv",
"domestic-E07000177-Cherwell/certificates.csv",
"domestic-E07000178-Oxford/certificates.csv",
"domestic-E07000179-South-Oxfordshire/certificates.csv",
"domestic-E07000180-Vale-of-White-Horse/certificates.csv",
"domestic-E07000181-West-Oxfordshire/certificates.csv",
"domestic-E07000187-Mendip/certificates.csv",
"domestic-E07000188-Sedgemoor/certificates.csv",
"domestic-E07000189-South-Somerset/certificates.csv",
"domestic-E07000192-Cannock-Chase/certificates.csv",
"domestic-E07000193-East-Staffordshire/certificates.csv",
"domestic-E07000194-Lichfield/certificates.csv",
"domestic-E07000195-Newcastle-under-Lyme/certificates.csv",
"domestic-E07000196-South-Staffordshire/certificates.csv",
"domestic-E07000197-Stafford/certificates.csv",
"domestic-E07000198-Staffordshire-Moorlands/certificates.csv",
"domestic-E07000199-Tamworth/certificates.csv",
"domestic-E07000200-Babergh/certificates.csv",
"domestic-E07000202-Ipswich/certificates.csv",
"domestic-E07000203-Mid-Suffolk/certificates.csv",
"domestic-E07000207-Elmbridge/certificates.csv",
"domestic-E07000208-Epsom-and-Ewell/certificates.csv",
"domestic-E07000209-Guildford/certificates.csv",
"domestic-E07000210-Mole-Valley/certificates.csv",
"domestic-E07000211-Reigate-and-Banstead/certificates.csv",
"domestic-E07000212-Runnymede/certificates.csv",
"domestic-E07000213-Spelthorne/certificates.csv",
"domestic-E07000214-Surrey-Heath/certificates.csv",
"domestic-E07000215-Tandridge/certificates.csv",
"domestic-E07000216-Waverley/certificates.csv",
"domestic-E07000217-Woking/certificates.csv",
"domestic-E07000218-North-Warwickshire/certificates.csv",
"domestic-E07000219-Nuneaton-and-Bedworth/certificates.csv",
"domestic-E07000220-Rugby/certificates.csv",
"domestic-E07000221-Stratford-on-Avon/certificates.csv",
"domestic-E07000222-Warwick/certificates.csv",
"domestic-E07000223-Adur/certificates.csv",
"domestic-E07000224-Arun/certificates.csv",
"domestic-E07000225-Chichester/certificates.csv",
"domestic-E07000226-Crawley/certificates.csv",
"domestic-E07000227-Horsham/certificates.csv",
"domestic-E07000228-Mid-Sussex/certificates.csv",
"domestic-E07000229-Worthing/certificates.csv",
"domestic-E07000234-Bromsgrove/certificates.csv",
"domestic-E07000235-Malvern-Hills/certificates.csv",
"domestic-E07000236-Redditch/certificates.csv",
"domestic-E07000237-Worcester/certificates.csv",
"domestic-E07000238-Wychavon/certificates.csv",
"domestic-E07000239-Wyre-Forest/certificates.csv",
"domestic-E07000240-St-Albans/certificates.csv",
"domestic-E07000241-Welwyn-Hatfield/certificates.csv",
"domestic-E07000242-East-Hertfordshire/certificates.csv",
"domestic-E07000243-Stevenage/certificates.csv",
"domestic-E07000244-East-Suffolk/certificates.csv",
"domestic-E07000245-West-Suffolk/certificates.csv",
"domestic-E07000246-Somerset-West-and-Taunton/certificates.csv",
"domestic-E08000001-Bolton/certificates.csv",
"domestic-E08000002-Bury/certificates.csv",
"domestic-E08000003-Manchester/certificates.csv",
"domestic-E08000004-Oldham/certificates.csv",
"domestic-E08000005-Rochdale/certificates.csv",
"domestic-E08000006-Salford/certificates.csv",
"domestic-E08000007-Stockport/certificates.csv",
"domestic-E08000008-Tameside/certificates.csv",
"domestic-E08000009-Trafford/certificates.csv",
"domestic-E08000010-Wigan/certificates.csv",
"domestic-E08000011-Knowsley/certificates.csv",
"domestic-E08000012-Liverpool/certificates.csv",
"domestic-E08000013-St-Helens/certificates.csv",
"domestic-E08000014-Sefton/certificates.csv",
"domestic-E08000015-Wirral/certificates.csv",
"domestic-E08000016-Barnsley/certificates.csv",
"domestic-E08000017-Doncaster/certificates.csv",
"domestic-E08000018-Rotherham/certificates.csv",
"domestic-E08000019-Sheffield/certificates.csv",
"domestic-E08000021-Newcastle-upon-Tyne/certificates.csv",
"domestic-E08000022-North-Tyneside/certificates.csv",
"domestic-E08000023-South-Tyneside/certificates.csv",
"domestic-E08000024-Sunderland/certificates.csv",
"domestic-E08000025-Birmingham/certificates.csv",
"domestic-E08000026-Coventry/certificates.csv",
"domestic-E08000027-Dudley/certificates.csv",
"domestic-E08000028-Sandwell/certificates.csv",
"domestic-E08000029-Solihull/certificates.csv",
"domestic-E08000030-Walsall/certificates.csv",
"domestic-E08000031-Wolverhampton/certificates.csv",
"domestic-E08000032-Bradford/certificates.csv",
"domestic-E08000033-Calderdale/certificates.csv",
"domestic-E08000034-Kirklees/certificates.csv",
"domestic-E08000035-Leeds/certificates.csv",
"domestic-E08000036-Wakefield/certificates.csv",
"domestic-E08000037-Gateshead/certificates.csv",
"domestic-E09000001-City-of-London/certificates.csv",
"domestic-E09000002-Barking-and-Dagenham/certificates.csv",
"domestic-E09000003-Barnet/certificates.csv",
"domestic-E09000004-Bexley/certificates.csv",
"domestic-E09000005-Brent/certificates.csv",
"domestic-E09000006-Bromley/certificates.csv",
"domestic-E09000007-Camden/certificates.csv",
"domestic-E09000008-Croydon/certificates.csv",
"domestic-E09000009-Ealing/certificates.csv",
"domestic-E09000010-Enfield/certificates.csv",
"domestic-E09000011-Greenwich/certificates.csv",
"domestic-E09000012-Hackney/certificates.csv",
"domestic-E09000013-Hammersmith-and-Fulham/certificates.csv",
"domestic-E09000014-Haringey/certificates.csv",
"domestic-E09000015-Harrow/certificates.csv",
"domestic-E09000016-Havering/certificates.csv",
"domestic-E09000017-Hillingdon/certificates.csv",
"domestic-E09000018-Hounslow/certificates.csv",
"domestic-E09000019-Islington/certificates.csv",
"domestic-E09000020-Kensington-and-Chelsea/certificates.csv",
"domestic-E09000021-Kingston-upon-Thames/certificates.csv",
"domestic-E09000022-Lambeth/certificates.csv",
"domestic-E09000023-Lewisham/certificates.csv",
"domestic-E09000024-Merton/certificates.csv",
"domestic-E09000025-Newham/certificates.csv",
"domestic-E09000026-Redbridge/certificates.csv",
"domestic-E09000027-Richmond-upon-Thames/certificates.csv",
"domestic-E09000028-Southwark/certificates.csv",
"domestic-E09000029-Sutton/certificates.csv",
"domestic-E09000030-Tower-Hamlets/certificates.csv",
"domestic-E09000031-Waltham-Forest/certificates.csv",
"domestic-E09000032-Wandsworth/certificates.csv",
"domestic-E09000033-Westminster/certificates.csv",
"domestic-W06000001-Isle-of-Anglesey/certificates.csv",
"domestic-W06000002-Gwynedd/certificates.csv",
"domestic-W06000003-Conwy/certificates.csv",
"domestic-W06000004-Denbighshire/certificates.csv",
"domestic-W06000005-Flintshire/certificates.csv",
"domestic-W06000006-Wrexham/certificates.csv",
"domestic-W06000008-Ceredigion/certificates.csv",
"domestic-W06000009-Pembrokeshire/certificates.csv",
"domestic-W06000010-Carmarthenshire/certificates.csv",
"domestic-W06000011-Swansea/certificates.csv",
"domestic-W06000012-Neath-Port-Talbot/certificates.csv",
"domestic-W06000013-Bridgend/certificates.csv",
"domestic-W06000014-Vale-of-Glamorgan/certificates.csv",
"domestic-W06000015-Cardiff/certificates.csv",
"domestic-W06000016-Rhondda-Cynon-Taf/certificates.csv",
"domestic-W06000018-Caerphilly/certificates.csv",
"domestic-W06000019-Blaenau-Gwent/certificates.csv",
"domestic-W06000020-Torfaen/certificates.csv",
"domestic-W06000021-Monmouthshire/certificates.csv",
"domestic-W06000022-Newport/certificates.csv",
"domestic-W06000023-Powys/certificates.csv",
"domestic-W06000024-Merthyr-Tydfil/certificates.csv",
"domestic-_unknown_local_authority--Unknown-Local-Authority-/certificates.csv"
]

verbose = False

def aggregate_data(df):
	'''
	Aggregates all the data and gives number of homes in each ratings band
	'''

	verbose and print(df)

	verbose and print("Local values:")
	current_rating = df['CURRENT_ENERGY_RATING'].value_counts().to_dict()
	potential_rating = df['POTENTIAL_ENERGY_RATING'].value_counts().to_dict()
	verbose and print(current_rating)
	verbose and print(potential_rating)

	global global_current_rating
	Cdict_current = Counter(global_current_rating) + Counter(current_rating)
	global_current_rating = dict(Cdict_current)

	global global_potential_rating
	Cdict_potential = Counter(global_potential_rating) + Counter(potential_rating)
	global_potential_rating = dict(Cdict_potential)

def aggregate_data_geographically(df, current_writer, potential_writer, filename):
	'''
	Aggregates data by location and creates CSV files with energy ratings data by location
	'''
	current_rating = df['CURRENT_ENERGY_RATING'].value_counts().to_dict()
	potential_rating = df['POTENTIAL_ENERGY_RATING'].value_counts().to_dict()

	# Extract name of place from filename
	pattern = r'domestic-[E,W].*?-'
	location = re.sub(pattern, '', filename)
	pattern = r'\/.*'
	location = re.sub(pattern, '', location)

	current_row = []
	current_row.append(location)
	for value in values:
		if value not in current_rating:
			current_row.append(0)
		else:
			current_row.append(current_rating[value])
	current_writer.writerow(current_row)

	potential_row = []
	potential_row.append(location)
	for value in values:
		if value not in potential_rating:
			potential_row.append(0)
		else:
			potential_row.append(potential_rating[value])
	potential_writer.writerow(potential_row)

def main():

	analysis = input("\nChoose analysis to run:\n1. Analysis of totals\nOR\n2. Analysis by geography\nEnter number: ")

	file_count = 1

	if analysis == '1':
		for filename in list_of_files:
			df = pd.read_csv(filename, usecols=['CURRENT_ENERGY_RATING','POTENTIAL_ENERGY_RATING'], dtype={'CURRENT_ENERGY_RATING': 'string', 'POTENTIAL_ENERGY_RATING': 'string'})
			aggregate_data(df)
			verbose and print("Global values:")
			verbose and print(global_current_rating)
			verbose and print(global_potential_rating)
			print("Parsed File " + str(file_count) + ": "+ filename)
			file_count = file_count + 1
	elif analysis == '2':
		with open('current_ratings_by_location.csv', mode='w') as output_file_current, open('potential_ratings_by_location.csv', mode='w') as output_file_potential:
			current_writer = csv.writer(output_file_current, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			potential_writer = csv.writer(output_file_potential, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			headers = values.copy()
			headers.insert(0, 'LOCATION')
			current_writer.writerow(headers)
			potential_writer.writerow(headers)
			for filename in list_of_files:
				df = pd.read_csv(filename, usecols=['CURRENT_ENERGY_RATING','POTENTIAL_ENERGY_RATING'], dtype={'CURRENT_ENERGY_RATING': 'string', 'POTENTIAL_ENERGY_RATING': 'string'})
				aggregate_data_geographically(df, current_writer, potential_writer, filename)
				print("Parsed File " + str(file_count) + ": "+ filename)
				file_count = file_count + 1
	else:
		print("Invalid Entry")

if __name__ == "__main__":
    main()