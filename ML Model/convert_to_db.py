import pandas as pd
import re

list_of_files = [
"all-domestic-certificates/domestic-E06000001-Hartlepool/certificates.csv",
"all-domestic-certificates/domestic-E06000002-Middlesbrough/certificates.csv",
"all-domestic-certificates/domestic-E06000003-Redcar-and-Cleveland/certificates.csv",
"all-domestic-certificates/domestic-E06000004-Stockton-on-Tees/certificates.csv",
"all-domestic-certificates/domestic-E06000005-Darlington/certificates.csv",
"all-domestic-certificates/domestic-E06000006-Halton/certificates.csv",
"all-domestic-certificates/domestic-E06000007-Warrington/certificates.csv",
"all-domestic-certificates/domestic-E06000008-Blackburn-with-Darwen/certificates.csv",
"all-domestic-certificates/domestic-E06000009-Blackpool/certificates.csv",
"all-domestic-certificates/domestic-E06000010-Kingston-upon-Hull-City-of/certificates.csv",
"all-domestic-certificates/domestic-E06000011-East-Riding-of-Yorkshire/certificates.csv",
"all-domestic-certificates/domestic-E06000012-North-East-Lincolnshire/certificates.csv",
"all-domestic-certificates/domestic-E06000013-North-Lincolnshire/certificates.csv",
"all-domestic-certificates/domestic-E06000014-York/certificates.csv",
"all-domestic-certificates/domestic-E06000015-Derby/certificates.csv",
"all-domestic-certificates/domestic-E06000016-Leicester/certificates.csv",
"all-domestic-certificates/domestic-E06000017-Rutland/certificates.csv",
"all-domestic-certificates/domestic-E06000018-Nottingham/certificates.csv",
"all-domestic-certificates/domestic-E06000019-Herefordshire-County-of/certificates.csv",
"all-domestic-certificates/domestic-E06000020-Telford-and-Wrekin/certificates.csv",
"all-domestic-certificates/domestic-E06000021-Stoke-on-Trent/certificates.csv",
"all-domestic-certificates/domestic-E06000022-Bath-and-North-East-Somerset/certificates.csv",
"all-domestic-certificates/domestic-E06000023-Bristol-City-of/certificates.csv",
"all-domestic-certificates/domestic-E06000024-North-Somerset/certificates.csv",
"all-domestic-certificates/domestic-E06000025-South-Gloucestershire/certificates.csv",
"all-domestic-certificates/domestic-E06000026-Plymouth/certificates.csv",
"all-domestic-certificates/domestic-E06000027-Torbay/certificates.csv",
"all-domestic-certificates/domestic-E06000030-Swindon/certificates.csv",
"all-domestic-certificates/domestic-E06000031-Peterborough/certificates.csv",
"all-domestic-certificates/domestic-E06000032-Luton/certificates.csv",
"all-domestic-certificates/domestic-E06000033-Southend-on-Sea/certificates.csv",
"all-domestic-certificates/domestic-E06000034-Thurrock/certificates.csv",
"all-domestic-certificates/domestic-E06000035-Medway/certificates.csv",
"all-domestic-certificates/domestic-E06000036-Bracknell-Forest/certificates.csv",
"all-domestic-certificates/domestic-E06000037-West-Berkshire/certificates.csv",
"all-domestic-certificates/domestic-E06000038-Reading/certificates.csv",
"all-domestic-certificates/domestic-E06000039-Slough/certificates.csv",
"all-domestic-certificates/domestic-E06000040-Windsor-and-Maidenhead/certificates.csv",
"all-domestic-certificates/domestic-E06000041-Wokingham/certificates.csv",
"all-domestic-certificates/domestic-E06000042-Milton-Keynes/certificates.csv",
"all-domestic-certificates/domestic-E06000043-Brighton-and-Hove/certificates.csv",
"all-domestic-certificates/domestic-E06000044-Portsmouth/certificates.csv",
"all-domestic-certificates/domestic-E06000045-Southampton/certificates.csv",
"all-domestic-certificates/domestic-E06000046-Isle-of-Wight/certificates.csv",
"all-domestic-certificates/domestic-E06000047-County-Durham/certificates.csv",
"all-domestic-certificates/domestic-E06000049-Cheshire-East/certificates.csv",
"all-domestic-certificates/domestic-E06000050-Cheshire-West-and-Chester/certificates.csv",
"all-domestic-certificates/domestic-E06000051-Shropshire/certificates.csv",
"all-domestic-certificates/domestic-E06000052-Cornwall/certificates.csv",
"all-domestic-certificates/domestic-E06000053-Isles-of-Scilly/certificates.csv",
"all-domestic-certificates/domestic-E06000054-Wiltshire/certificates.csv",
"all-domestic-certificates/domestic-E06000055-Bedford/certificates.csv",
"all-domestic-certificates/domestic-E06000056-Central-Bedfordshire/certificates.csv",
"all-domestic-certificates/domestic-E06000057-Northumberland/certificates.csv",
"all-domestic-certificates/domestic-E06000058-Bournemouth-Christchurch-and-Poole/certificates.csv",
"all-domestic-certificates/domestic-E06000059-Dorset/certificates.csv",
"all-domestic-certificates/domestic-E07000004-Aylesbury-Vale/certificates.csv",
"all-domestic-certificates/domestic-E07000005-Chiltern/certificates.csv",
"all-domestic-certificates/domestic-E07000006-South-Bucks/certificates.csv",
"all-domestic-certificates/domestic-E07000007-Wycombe/certificates.csv",
"all-domestic-certificates/domestic-E07000008-Cambridge/certificates.csv",
"all-domestic-certificates/domestic-E07000009-East-Cambridgeshire/certificates.csv",
"all-domestic-certificates/domestic-E07000010-Fenland/certificates.csv",
"all-domestic-certificates/domestic-E07000011-Huntingdonshire/certificates.csv",
"all-domestic-certificates/domestic-E07000012-South-Cambridgeshire/certificates.csv",
"all-domestic-certificates/domestic-E07000026-Allerdale/certificates.csv",
"all-domestic-certificates/domestic-E07000027-Barrow-in-Furness/certificates.csv",
"all-domestic-certificates/domestic-E07000028-Carlisle/certificates.csv",
"all-domestic-certificates/domestic-E07000029-Copeland/certificates.csv",
"all-domestic-certificates/domestic-E07000030-Eden/certificates.csv",
"all-domestic-certificates/domestic-E07000031-South-Lakeland/certificates.csv",
"all-domestic-certificates/domestic-E07000032-Amber-Valley/certificates.csv",
"all-domestic-certificates/domestic-E07000033-Bolsover/certificates.csv",
"all-domestic-certificates/domestic-E07000034-Chesterfield/certificates.csv",
"all-domestic-certificates/domestic-E07000035-Derbyshire-Dales/certificates.csv",
"all-domestic-certificates/domestic-E07000036-Erewash/certificates.csv",
"all-domestic-certificates/domestic-E07000037-High-Peak/certificates.csv",
"all-domestic-certificates/domestic-E07000038-North-East-Derbyshire/certificates.csv",
"all-domestic-certificates/domestic-E07000039-South-Derbyshire/certificates.csv",
"all-domestic-certificates/domestic-E07000040-East-Devon/certificates.csv",
"all-domestic-certificates/domestic-E07000041-Exeter/certificates.csv",
"all-domestic-certificates/domestic-E07000042-Mid-Devon/certificates.csv",
"all-domestic-certificates/domestic-E07000043-North-Devon/certificates.csv",
"all-domestic-certificates/domestic-E07000044-South-Hams/certificates.csv",
"all-domestic-certificates/domestic-E07000045-Teignbridge/certificates.csv",
"all-domestic-certificates/domestic-E07000046-Torridge/certificates.csv",
"all-domestic-certificates/domestic-E07000047-West-Devon/certificates.csv",
"all-domestic-certificates/domestic-E07000061-Eastbourne/certificates.csv",
"all-domestic-certificates/domestic-E07000062-Hastings/certificates.csv",
"all-domestic-certificates/domestic-E07000063-Lewes/certificates.csv",
"all-domestic-certificates/domestic-E07000064-Rother/certificates.csv",
"all-domestic-certificates/domestic-E07000065-Wealden/certificates.csv",
"all-domestic-certificates/domestic-E07000066-Basildon/certificates.csv",
"all-domestic-certificates/domestic-E07000067-Braintree/certificates.csv",
"all-domestic-certificates/domestic-E07000068-Brentwood/certificates.csv",
"all-domestic-certificates/domestic-E07000069-Castle-Point/certificates.csv",
"all-domestic-certificates/domestic-E07000070-Chelmsford/certificates.csv",
"all-domestic-certificates/domestic-E07000071-Colchester/certificates.csv",
"all-domestic-certificates/domestic-E07000072-Epping-Forest/certificates.csv",
"all-domestic-certificates/domestic-E07000073-Harlow/certificates.csv",
"all-domestic-certificates/domestic-E07000074-Maldon/certificates.csv",
"all-domestic-certificates/domestic-E07000075-Rochford/certificates.csv",
"all-domestic-certificates/domestic-E07000076-Tendring/certificates.csv",
"all-domestic-certificates/domestic-E07000077-Uttlesford/certificates.csv",
"all-domestic-certificates/domestic-E07000078-Cheltenham/certificates.csv",
"all-domestic-certificates/domestic-E07000079-Cotswold/certificates.csv",
"all-domestic-certificates/domestic-E07000080-Forest-of-Dean/certificates.csv",
"all-domestic-certificates/domestic-E07000081-Gloucester/certificates.csv",
"all-domestic-certificates/domestic-E07000082-Stroud/certificates.csv",
"all-domestic-certificates/domestic-E07000083-Tewkesbury/certificates.csv",
"all-domestic-certificates/domestic-E07000084-Basingstoke-and-Deane/certificates.csv",
"all-domestic-certificates/domestic-E07000085-East-Hampshire/certificates.csv",
"all-domestic-certificates/domestic-E07000086-Eastleigh/certificates.csv",
"all-domestic-certificates/domestic-E07000087-Fareham/certificates.csv",
"all-domestic-certificates/domestic-E07000088-Gosport/certificates.csv",
"all-domestic-certificates/domestic-E07000089-Hart/certificates.csv",
"all-domestic-certificates/domestic-E07000090-Havant/certificates.csv",
"all-domestic-certificates/domestic-E07000091-New-Forest/certificates.csv",
"all-domestic-certificates/domestic-E07000092-Rushmoor/certificates.csv",
"all-domestic-certificates/domestic-E07000093-Test-Valley/certificates.csv",
"all-domestic-certificates/domestic-E07000094-Winchester/certificates.csv",
"all-domestic-certificates/domestic-E07000095-Broxbourne/certificates.csv",
"all-domestic-certificates/domestic-E07000096-Dacorum/certificates.csv",
"all-domestic-certificates/domestic-E07000098-Hertsmere/certificates.csv",
"all-domestic-certificates/domestic-E07000099-North-Hertfordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000102-Three-Rivers/certificates.csv",
"all-domestic-certificates/domestic-E07000103-Watford/certificates.csv",
"all-domestic-certificates/domestic-E07000105-Ashford/certificates.csv",
"all-domestic-certificates/domestic-E07000106-Canterbury/certificates.csv",
"all-domestic-certificates/domestic-E07000107-Dartford/certificates.csv",
"all-domestic-certificates/domestic-E07000108-Dover/certificates.csv",
"all-domestic-certificates/domestic-E07000109-Gravesham/certificates.csv",
"all-domestic-certificates/domestic-E07000110-Maidstone/certificates.csv",
"all-domestic-certificates/domestic-E07000111-Sevenoaks/certificates.csv",
"all-domestic-certificates/domestic-E07000112-Folkestone-and-Hythe/certificates.csv",
"all-domestic-certificates/domestic-E07000113-Swale/certificates.csv",
"all-domestic-certificates/domestic-E07000114-Thanet/certificates.csv",
"all-domestic-certificates/domestic-E07000115-Tonbridge-and-Malling/certificates.csv",
"all-domestic-certificates/domestic-E07000116-Tunbridge-Wells/certificates.csv",
"all-domestic-certificates/domestic-E07000117-Burnley/certificates.csv",
"all-domestic-certificates/domestic-E07000118-Chorley/certificates.csv",
"all-domestic-certificates/domestic-E07000119-Fylde/certificates.csv",
"all-domestic-certificates/domestic-E07000120-Hyndburn/certificates.csv",
"all-domestic-certificates/domestic-E07000121-Lancaster/certificates.csv",
"all-domestic-certificates/domestic-E07000122-Pendle/certificates.csv",
"all-domestic-certificates/domestic-E07000123-Preston/certificates.csv",
"all-domestic-certificates/domestic-E07000124-Ribble-Valley/certificates.csv",
"all-domestic-certificates/domestic-E07000125-Rossendale/certificates.csv",
"all-domestic-certificates/domestic-E07000126-South-Ribble/certificates.csv",
"all-domestic-certificates/domestic-E07000127-West-Lancashire/certificates.csv",
"all-domestic-certificates/domestic-E07000128-Wyre/certificates.csv",
"all-domestic-certificates/domestic-E07000129-Blaby/certificates.csv",
"all-domestic-certificates/domestic-E07000130-Charnwood/certificates.csv",
"all-domestic-certificates/domestic-E07000131-Harborough/certificates.csv",
"all-domestic-certificates/domestic-E07000132-Hinckley-and-Bosworth/certificates.csv",
"all-domestic-certificates/domestic-E07000133-Melton/certificates.csv",
"all-domestic-certificates/domestic-E07000134-North-West-Leicestershire/certificates.csv",
"all-domestic-certificates/domestic-E07000135-Oadby-and-Wigston/certificates.csv",
"all-domestic-certificates/domestic-E07000136-Boston/certificates.csv",
"all-domestic-certificates/domestic-E07000137-East-Lindsey/certificates.csv",
"all-domestic-certificates/domestic-E07000138-Lincoln/certificates.csv",
"all-domestic-certificates/domestic-E07000139-North-Kesteven/certificates.csv",
"all-domestic-certificates/domestic-E07000140-South-Holland/certificates.csv",
"all-domestic-certificates/domestic-E07000141-South-Kesteven/certificates.csv",
"all-domestic-certificates/domestic-E07000142-West-Lindsey/certificates.csv",
"all-domestic-certificates/domestic-E07000143-Breckland/certificates.csv",
"all-domestic-certificates/domestic-E07000144-Broadland/certificates.csv",
"all-domestic-certificates/domestic-E07000145-Great-Yarmouth/certificates.csv",
"all-domestic-certificates/domestic-E07000146-King-s-Lynn-and-West-Norfolk/certificates.csv",
"all-domestic-certificates/domestic-E07000147-North-Norfolk/certificates.csv",
"all-domestic-certificates/domestic-E07000148-Norwich/certificates.csv",
"all-domestic-certificates/domestic-E07000149-South-Norfolk/certificates.csv",
"all-domestic-certificates/domestic-E07000150-Corby/certificates.csv",
"all-domestic-certificates/domestic-E07000151-Daventry/certificates.csv",
"all-domestic-certificates/domestic-E07000152-East-Northamptonshire/certificates.csv",
"all-domestic-certificates/domestic-E07000153-Kettering/certificates.csv",
"all-domestic-certificates/domestic-E07000154-Northampton/certificates.csv",
"all-domestic-certificates/domestic-E07000155-South-Northamptonshire/certificates.csv",
"all-domestic-certificates/domestic-E07000156-Wellingborough/certificates.csv",
"all-domestic-certificates/domestic-E07000163-Craven/certificates.csv",
"all-domestic-certificates/domestic-E07000164-Hambleton/certificates.csv",
"all-domestic-certificates/domestic-E07000165-Harrogate/certificates.csv",
"all-domestic-certificates/domestic-E07000166-Richmondshire/certificates.csv",
"all-domestic-certificates/domestic-E07000167-Ryedale/certificates.csv",
"all-domestic-certificates/domestic-E07000168-Scarborough/certificates.csv",
"all-domestic-certificates/domestic-E07000169-Selby/certificates.csv",
"all-domestic-certificates/domestic-E07000170-Ashfield/certificates.csv",
"all-domestic-certificates/domestic-E07000171-Bassetlaw/certificates.csv",
"all-domestic-certificates/domestic-E07000172-Broxtowe/certificates.csv",
"all-domestic-certificates/domestic-E07000173-Gedling/certificates.csv",
"all-domestic-certificates/domestic-E07000174-Mansfield/certificates.csv",
"all-domestic-certificates/domestic-E07000175-Newark-and-Sherwood/certificates.csv",
"all-domestic-certificates/domestic-E07000176-Rushcliffe/certificates.csv",
"all-domestic-certificates/domestic-E07000177-Cherwell/certificates.csv",
"all-domestic-certificates/domestic-E07000178-Oxford/certificates.csv",
"all-domestic-certificates/domestic-E07000179-South-Oxfordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000180-Vale-of-White-Horse/certificates.csv",
"all-domestic-certificates/domestic-E07000181-West-Oxfordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000187-Mendip/certificates.csv",
"all-domestic-certificates/domestic-E07000188-Sedgemoor/certificates.csv",
"all-domestic-certificates/domestic-E07000189-South-Somerset/certificates.csv",
"all-domestic-certificates/domestic-E07000192-Cannock-Chase/certificates.csv",
"all-domestic-certificates/domestic-E07000193-East-Staffordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000194-Lichfield/certificates.csv",
"all-domestic-certificates/domestic-E07000195-Newcastle-under-Lyme/certificates.csv",
"all-domestic-certificates/domestic-E07000196-South-Staffordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000197-Stafford/certificates.csv",
"all-domestic-certificates/domestic-E07000198-Staffordshire-Moorlands/certificates.csv",
"all-domestic-certificates/domestic-E07000199-Tamworth/certificates.csv",
"all-domestic-certificates/domestic-E07000200-Babergh/certificates.csv",
"all-domestic-certificates/domestic-E07000202-Ipswich/certificates.csv",
"all-domestic-certificates/domestic-E07000203-Mid-Suffolk/certificates.csv",
"all-domestic-certificates/domestic-E07000207-Elmbridge/certificates.csv",
"all-domestic-certificates/domestic-E07000208-Epsom-and-Ewell/certificates.csv",
"all-domestic-certificates/domestic-E07000209-Guildford/certificates.csv",
"all-domestic-certificates/domestic-E07000210-Mole-Valley/certificates.csv",
"all-domestic-certificates/domestic-E07000211-Reigate-and-Banstead/certificates.csv",
"all-domestic-certificates/domestic-E07000212-Runnymede/certificates.csv",
"all-domestic-certificates/domestic-E07000213-Spelthorne/certificates.csv",
"all-domestic-certificates/domestic-E07000214-Surrey-Heath/certificates.csv",
"all-domestic-certificates/domestic-E07000215-Tandridge/certificates.csv",
"all-domestic-certificates/domestic-E07000216-Waverley/certificates.csv",
"all-domestic-certificates/domestic-E07000217-Woking/certificates.csv",
"all-domestic-certificates/domestic-E07000218-North-Warwickshire/certificates.csv",
"all-domestic-certificates/domestic-E07000219-Nuneaton-and-Bedworth/certificates.csv",
"all-domestic-certificates/domestic-E07000220-Rugby/certificates.csv",
"all-domestic-certificates/domestic-E07000221-Stratford-on-Avon/certificates.csv",
"all-domestic-certificates/domestic-E07000222-Warwick/certificates.csv",
"all-domestic-certificates/domestic-E07000223-Adur/certificates.csv",
"all-domestic-certificates/domestic-E07000224-Arun/certificates.csv",
"all-domestic-certificates/domestic-E07000225-Chichester/certificates.csv",
"all-domestic-certificates/domestic-E07000226-Crawley/certificates.csv",
"all-domestic-certificates/domestic-E07000227-Horsham/certificates.csv",
"all-domestic-certificates/domestic-E07000228-Mid-Sussex/certificates.csv",
"all-domestic-certificates/domestic-E07000229-Worthing/certificates.csv",
"all-domestic-certificates/domestic-E07000234-Bromsgrove/certificates.csv",
"all-domestic-certificates/domestic-E07000235-Malvern-Hills/certificates.csv",
"all-domestic-certificates/domestic-E07000236-Redditch/certificates.csv",
"all-domestic-certificates/domestic-E07000237-Worcester/certificates.csv",
"all-domestic-certificates/domestic-E07000238-Wychavon/certificates.csv",
"all-domestic-certificates/domestic-E07000239-Wyre-Forest/certificates.csv",
"all-domestic-certificates/domestic-E07000240-St-Albans/certificates.csv",
"all-domestic-certificates/domestic-E07000241-Welwyn-Hatfield/certificates.csv",
"all-domestic-certificates/domestic-E07000242-East-Hertfordshire/certificates.csv",
"all-domestic-certificates/domestic-E07000243-Stevenage/certificates.csv",
"all-domestic-certificates/domestic-E07000244-East-Suffolk/certificates.csv",
"all-domestic-certificates/domestic-E07000245-West-Suffolk/certificates.csv",
"all-domestic-certificates/domestic-E07000246-Somerset-West-and-Taunton/certificates.csv",
"all-domestic-certificates/domestic-E08000001-Bolton/certificates.csv",
"all-domestic-certificates/domestic-E08000002-Bury/certificates.csv",
"all-domestic-certificates/domestic-E08000003-Manchester/certificates.csv",
"all-domestic-certificates/domestic-E08000004-Oldham/certificates.csv",
"all-domestic-certificates/domestic-E08000005-Rochdale/certificates.csv",
"all-domestic-certificates/domestic-E08000006-Salford/certificates.csv",
"all-domestic-certificates/domestic-E08000007-Stockport/certificates.csv",
"all-domestic-certificates/domestic-E08000008-Tameside/certificates.csv",
"all-domestic-certificates/domestic-E08000009-Trafford/certificates.csv",
"all-domestic-certificates/domestic-E08000010-Wigan/certificates.csv",
"all-domestic-certificates/domestic-E08000011-Knowsley/certificates.csv",
"all-domestic-certificates/domestic-E08000012-Liverpool/certificates.csv",
"all-domestic-certificates/domestic-E08000013-St-Helens/certificates.csv",
"all-domestic-certificates/domestic-E08000014-Sefton/certificates.csv",
"all-domestic-certificates/domestic-E08000015-Wirral/certificates.csv",
"all-domestic-certificates/domestic-E08000016-Barnsley/certificates.csv",
"all-domestic-certificates/domestic-E08000017-Doncaster/certificates.csv",
"all-domestic-certificates/domestic-E08000018-Rotherham/certificates.csv",
"all-domestic-certificates/domestic-E08000019-Sheffield/certificates.csv",
"all-domestic-certificates/domestic-E08000021-Newcastle-upon-Tyne/certificates.csv",
"all-domestic-certificates/domestic-E08000022-North-Tyneside/certificates.csv",
"all-domestic-certificates/domestic-E08000023-South-Tyneside/certificates.csv",
"all-domestic-certificates/domestic-E08000024-Sunderland/certificates.csv",
"all-domestic-certificates/domestic-E08000025-Birmingham/certificates.csv",
"all-domestic-certificates/domestic-E08000026-Coventry/certificates.csv",
"all-domestic-certificates/domestic-E08000027-Dudley/certificates.csv",
"all-domestic-certificates/domestic-E08000028-Sandwell/certificates.csv",
"all-domestic-certificates/domestic-E08000029-Solihull/certificates.csv",
"all-domestic-certificates/domestic-E08000030-Walsall/certificates.csv",
"all-domestic-certificates/domestic-E08000031-Wolverhampton/certificates.csv",
"all-domestic-certificates/domestic-E08000032-Bradford/certificates.csv",
"all-domestic-certificates/domestic-E08000033-Calderdale/certificates.csv",
"all-domestic-certificates/domestic-E08000034-Kirklees/certificates.csv",
"all-domestic-certificates/domestic-E08000035-Leeds/certificates.csv",
"all-domestic-certificates/domestic-E08000036-Wakefield/certificates.csv",
"all-domestic-certificates/domestic-E08000037-Gateshead/certificates.csv",
"all-domestic-certificates/domestic-E09000001-City-of-London/certificates.csv",
"all-domestic-certificates/domestic-E09000002-Barking-and-Dagenham/certificates.csv",
"all-domestic-certificates/domestic-E09000003-Barnet/certificates.csv",
"all-domestic-certificates/domestic-E09000004-Bexley/certificates.csv",
"all-domestic-certificates/domestic-E09000005-Brent/certificates.csv",
"all-domestic-certificates/domestic-E09000006-Bromley/certificates.csv",
"all-domestic-certificates/domestic-E09000007-Camden/certificates.csv",
"all-domestic-certificates/domestic-E09000008-Croydon/certificates.csv",
"all-domestic-certificates/domestic-E09000009-Ealing/certificates.csv",
"all-domestic-certificates/domestic-E09000010-Enfield/certificates.csv",
"all-domestic-certificates/domestic-E09000011-Greenwich/certificates.csv",
"all-domestic-certificates/domestic-E09000012-Hackney/certificates.csv",
"all-domestic-certificates/domestic-E09000013-Hammersmith-and-Fulham/certificates.csv",
"all-domestic-certificates/domestic-E09000014-Haringey/certificates.csv",
"all-domestic-certificates/domestic-E09000015-Harrow/certificates.csv",
"all-domestic-certificates/domestic-E09000016-Havering/certificates.csv",
"all-domestic-certificates/domestic-E09000017-Hillingdon/certificates.csv",
"all-domestic-certificates/domestic-E09000018-Hounslow/certificates.csv",
"all-domestic-certificates/domestic-E09000019-Islington/certificates.csv",
"all-domestic-certificates/domestic-E09000020-Kensington-and-Chelsea/certificates.csv",
"all-domestic-certificates/domestic-E09000021-Kingston-upon-Thames/certificates.csv",
"all-domestic-certificates/domestic-E09000022-Lambeth/certificates.csv",
"all-domestic-certificates/domestic-E09000023-Lewisham/certificates.csv",
"all-domestic-certificates/domestic-E09000024-Merton/certificates.csv",
"all-domestic-certificates/domestic-E09000025-Newham/certificates.csv",
"all-domestic-certificates/domestic-E09000026-Redbridge/certificates.csv",
"all-domestic-certificates/domestic-E09000027-Richmond-upon-Thames/certificates.csv",
"all-domestic-certificates/domestic-E09000028-Southwark/certificates.csv",
"all-domestic-certificates/domestic-E09000029-Sutton/certificates.csv",
"all-domestic-certificates/domestic-E09000030-Tower-Hamlets/certificates.csv",
"all-domestic-certificates/domestic-E09000031-Waltham-Forest/certificates.csv",
"all-domestic-certificates/domestic-E09000032-Wandsworth/certificates.csv",
"all-domestic-certificates/domestic-E09000033-Westminster/certificates.csv",
"all-domestic-certificates/domestic-W06000001-Isle-of-Anglesey/certificates.csv",
"all-domestic-certificates/domestic-W06000002-Gwynedd/certificates.csv",
"all-domestic-certificates/domestic-W06000003-Conwy/certificates.csv",
"all-domestic-certificates/domestic-W06000004-Denbighshire/certificates.csv",
"all-domestic-certificates/domestic-W06000005-Flintshire/certificates.csv",
"all-domestic-certificates/domestic-W06000006-Wrexham/certificates.csv",
"all-domestic-certificates/domestic-W06000008-Ceredigion/certificates.csv",
"all-domestic-certificates/domestic-W06000009-Pembrokeshire/certificates.csv",
"all-domestic-certificates/domestic-W06000010-Carmarthenshire/certificates.csv",
"all-domestic-certificates/domestic-W06000011-Swansea/certificates.csv",
"all-domestic-certificates/domestic-W06000012-Neath-Port-Talbot/certificates.csv",
"all-domestic-certificates/domestic-W06000013-Bridgend/certificates.csv",
"all-domestic-certificates/domestic-W06000014-Vale-of-Glamorgan/certificates.csv",
"all-domestic-certificates/domestic-W06000015-Cardiff/certificates.csv",
"all-domestic-certificates/domestic-W06000016-Rhondda-Cynon-Taf/certificates.csv",
"all-domestic-certificates/domestic-W06000018-Caerphilly/certificates.csv",
"all-domestic-certificates/domestic-W06000019-Blaenau-Gwent/certificates.csv",
"all-domestic-certificates/domestic-W06000020-Torfaen/certificates.csv",
"all-domestic-certificates/domestic-W06000021-Monmouthshire/certificates.csv",
"all-domestic-certificates/domestic-W06000022-Newport/certificates.csv",
"all-domestic-certificates/domestic-W06000023-Powys/certificates.csv",
"all-domestic-certificates/domestic-W06000024-Merthyr-Tydfil/certificates.csv"
# "all-dmoestic-certificates/domestic-_unknown_local_authority--Unknown-Local-Authority-/certificates.csv"
]

def example_main():
	"""
	Convert the CSV files to the form that is used to store the data in the database using a string matching algorithm
	"""

    output_label = 'CURRENT_ENERGY_EFFICIENCY'
    used_cols = ['CURRENT_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'MAINS_GAS_FLAG', 'GLAZED_TYPE', 'NUMBER_HABITABLE_ROOMS', 'LOW_ENERGY_LIGHTING', 'HOTWATER_DESCRIPTION', 'FLOOR_DESCRIPTION', 'WALLS_DESCRIPTION', 'ROOF_DESCRIPTION', 'MAINHEAT_DESCRIPTION', 'MAINHEATCONT_DESCRIPTION', 'MAIN_FUEL', 'SOLAR_WATER_HEATING_FLAG', 'CONSTRUCTION_AGE_BAND']
    data_types = {'CURRENT_ENERGY_EFFICIENCY': 'string', 'PROPERTY_TYPE': 'string', 'MAINS_GAS_FLAG': 'string', 'GLAZED_TYPE': 'string', 'NUMBER_HABITABLE_ROOMS': 'string', 'LOW_ENERGY_LIGHTING': 'string', 'HOTWATER_DESCRIPTION': 'string', 'FLOOR_DESCRIPTION': 'string', 'WALLS_DESCRIPTION': 'string', 'ROOF_DESCRIPTION': 'string', 'MAINHEAT_DESCRIPTION': 'string', 'MAINHEATCONT_DESCRIPTION': 'string', 'MAIN_FUEL': 'string', 'SOLAR_WATER_HEATING_FLAG': 'string', 'CONSTRUCTION_AGE_BAND': 'string'}
    
    for file in list_of_files:
        data = pd.read_csv(file, usecols=used_cols, dtype=data_types)

        output = pd.DataFrame(columns=used_cols)

        output['CURRENT_ENERGY_EFFICIENCY'] = data['CURRENT_ENERGY_EFFICIENCY']

        # for each column convert check the value and convert to form that is used in database

        floor_inuslation = []

        for row in data['FLOOR_DESCRIPTION']:
            if pd.isna(row):
                floor_inuslation.append('False')
            elif 'no insulation' in row.lower() or 'below' in row.lower():
                floor_inuslation.append('False')
            elif 'limited' in row.lower():
                floor_inuslation.append('Limited')
            else:
                floor_inuslation.append('True')

        output['FLOOR_DESCRIPTION'] = floor_inuslation

        solar_water_heating = []

        for row in data['SOLAR_WATER_HEATING_FLAG']:
            if pd.isna(row):
                solar_water_heating.append('False')
            elif 'Y' in row:
                solar_water_heating.append('True')
            else:
                solar_water_heating.append('False')

        output['SOLAR_WATER_HEATING_FLAG'] = solar_water_heating

        output['PROPERTY_TYPE'] = data['PROPERTY_TYPE']

        roof_inuslation = []

        for row in data['ROOF_DESCRIPTION']:
            if pd.isna(row):
                roof_inuslation.append('False')
            elif 'no insulation' in row.lower() or 'above' in row.lower():
                roof_inuslation.append('False')
            elif 'limited' in row.lower():
                roof_inuslation.append('Limited')
            else:
                roof_inuslation.append('True')

        output['ROOF_DESCRIPTION'] = roof_inuslation

        heating_fuel = []

        for row in data['MAIN_FUEL']:
            if pd.isna(row):
                heating_fuel.append('No heating')
            elif 'mains gas' in row.lower():
                heating_fuel.append('Mains gas')
            elif 'electric' in row.lower():
                heating_fuel.append('Electric')
            else:
                heating_fuel.append('Other')

        output['MAIN_FUEL'] = heating_fuel

        thermostat = []

        for row in data['MAINHEATCONT_DESCRIPTION']:
            if pd.isna(row):
                thermostat.append('False')
            elif 'no thermostatic' in row.lower() or 'no time' in row.lower():
                thermostat.append('False')
            elif 'programmer' in row.lower() or 'automatic' in row.lower() or 'manual' in row.lower() or 'thermostats' in row.lower():
                thermostat.append('True')
            else:
                thermostat.append('Other')

        output['MAINHEATCONT_DESCRIPTION'] = thermostat

        gas_connection = []

        for row in data['MAINS_GAS_FLAG']:
            if pd.isna(row):
                gas_connection.append('True')
            elif 'N' in row:
                gas_connection.append('False')
            else:
                gas_connection.append('True')

        output['MAINS_GAS_FLAG'] = gas_connection

        floor_type = []

        for row in data['FLOOR_DESCRIPTION']:
            if pd.isna(row):
                floor_type.append('Other')
            elif 'suspended' in row.lower():
                floor_type.append('Suspended')
            elif 'solid' in row.lower():
                floor_type.append('Solid')
            elif 'below' in row.lower():
                floor_type.append('(another dwelling below)')
            else:
                floor_type.append('Other')

        output['FLOOR_DESCRIPTION'] = floor_type

        heating_type = []

        for row in data['MAINHEAT_DESCRIPTION']:
            if pd.isna(row):
                heating_type.append('Other')
            elif 'boiler' in row.lower():
                heating_type.append('Boiler')
            elif 'electric' in row.lower():
                heating_type.append('Electric')
            elif 'community' in row.lower():
                heating_type.append('Community scheme')
            else:
                heating_type.append('Other')

        output['MAINHEAT_DESCRIPTION'] = heating_type

        hotwater_type = []

        for row in data['HOTWATER_DESCRIPTION']:
            if pd.isna(row):
                hotwater_type.append('Other')
            elif 'main' in row.lower():
                hotwater_type.append('From main')
            elif 'electric' in row.lower():
                hotwater_type.append('Electric')
            elif 'community' in row.lower():
                hotwater_type.append('Community scheme')
            else:
                hotwater_type.append('Other')

        output['HOTWATER_DESCRIPTION'] = hotwater_type

        low_energy_light = []

        for row in data['LOW_ENERGY_LIGHTING']:
            if pd.isna(row):
                low_energy_light.append('0')
            else:
                low_energy_light.append(row)

        output['LOW_ENERGY_LIGHTING'] = low_energy_light

        roof_type = []

        for row in data['ROOF_DESCRIPTION']:
            if pd.isna(row):
                roof_type.append('Other')
            elif 'pitched' in row.lower():
                roof_type.append('Pitched')
            elif 'flat' in row.lower():
                roof_type.append('Flat')
            elif 'above' in row.lower():
                roof_type.append('(another dwelling above)')
            else:
                roof_type.append('Other')

        output['ROOF_DESCRIPTION'] = roof_type

        rooms = []

        for row in data['NUMBER_HABITABLE_ROOMS']:
            if pd.isna(row):
                rooms.append('0')
            else:
                rooms.append(row)

        output['NUMBER_HABITABLE_ROOMS'] = rooms

        wall_type = []

        for row in data['WALLS_DESCRIPTION']:
            if pd.isna(row):
                wall_type.append('Other')
            elif 'cavity' in row.lower():
                wall_type.append('Cavity')
            elif 'solid brick' in row.lower():
                wall_type.append('Solid brick')
            elif 'system' in row.lower():
                wall_type.append('System built')
            else:
                wall_type.append('Other')

        output['WALLS_DESCRIPTION'] = wall_type

        glaze_type = []

        for row in data['GLAZED_TYPE']:
            if pd.isna(row):
                glaze_type.append('Unknown')
            elif 'single' in row.lower():
                glaze_type.append('Single')
            elif 'double' in row.lower():
                glaze_type.append('Double')
            elif 'triple' in row.lower():
                glaze_type.append('Triple')
            else:
                glaze_type.append('Unknown')

        output['GLAZED_TYPE'] = glaze_type

        wall_inuslation = []

        for row in data['WALLS_DESCRIPTION']:
            if pd.isna(row):
                wall_inuslation.append('False')
            elif 'no insulation' in row.lower():
                wall_inuslation.append('False')
            elif 'partial' in row.lower():
                wall_inuslation.append('Partial')
            else:
                wall_inuslation.append('True')

        output['WALLS_DESCRIPTION'] = wall_inuslation

        age = []

        for row in data['CONSTRUCTION_AGE_BAND']:
            if pd.isna(row):
                age.append('Unknown')
            elif 'before 1900' in row.lower():
                age.append('Before 1900')
            elif '1900-1929' in row.lower():
                age.append('1900-1929')
            elif '1930-1949' in row.lower():
                age.append('1930-1949')
            elif '1950-1966' in row.lower():
                age.append('1950-1966')
            elif '1967-1975' in row.lower():
                age.append('1967-1975')
            elif '1976-1982' in row.lower():
                age.append('1976-1982')
            elif '1983-1990' in row.lower():
                age.append('1983-1990')
            elif '1991-1995' in row.lower():
                age.append('1991-1995')
            elif '1996-2002' in row.lower():
                age.append('1996-2002')
            elif '2003-2006' in row.lower():
                age.append('2003-2006')
            elif '2007 onwards' in row.lower():
                age.append('2007 onwards')
            else:
                age.append('Unknown')

        output['CONSTRUCTION_AGE_BAND'] = age

        # write to a new file
        pattern = re.compile("([EW]\d\d\d\d\d\d\d\d)")
        res = pattern.search(file)
        name = "DB Outputs/" + res.group(1) + ".csv"
        output.to_csv(name, index=False)

        print("Parsed file: " + file)

if __name__ == "__main__":
    example_main()
