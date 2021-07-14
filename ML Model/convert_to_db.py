import pandas as pd

def example_main():

    output_label = 'CURRENT_ENERGY_EFFICIENCY'
    used_cols = ['CURRENT_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'MAINS_GAS_FLAG', 'GLAZED_TYPE', 'NUMBER_HABITABLE_ROOMS', 'LOW_ENERGY_LIGHTING', 'HOTWATER_DESCRIPTION', 'FLOOR_DESCRIPTION', 'WALLS_DESCRIPTION', 'ROOF_DESCRIPTION', 'MAINHEAT_DESCRIPTION', 'MAINHEATCONT_DESCRIPTION', 'MAIN_FUEL', 'SOLAR_WATER_HEATING_FLAG', 'CONSTRUCTION_AGE_BAND']
    data_types = {'CURRENT_ENERGY_EFFICIENCY': 'string', 'PROPERTY_TYPE': 'string', 'MAINS_GAS_FLAG': 'string', 'GLAZED_TYPE': 'string', 'NUMBER_HABITABLE_ROOMS': 'string', 'LOW_ENERGY_LIGHTING': 'string', 'HOTWATER_DESCRIPTION': 'string', 'FLOOR_DESCRIPTION': 'string', 'WALLS_DESCRIPTION': 'string', 'ROOF_DESCRIPTION': 'string', 'MAINHEAT_DESCRIPTION': 'string', 'MAINHEATCONT_DESCRIPTION': 'string', 'MAIN_FUEL': 'string', 'SOLAR_WATER_HEATING_FLAG': 'string', 'CONSTRUCTION_AGE_BAND': 'string'}
    
    data = pd.read_csv("all-domestic-certificates/domestic-E08000035-Leeds/certificates.csv", usecols=used_cols, dtype=data_types)

    output = pd.DataFrame(columns=used_cols)

    output['CURRENT_ENERGY_EFFICIENCY'] = data['CURRENT_ENERGY_EFFICIENCY']

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

    print(output)

    # write to a new file 
    output.to_csv("Leeds_output.csv", index=False)

if __name__ == "__main__":
    example_main()
