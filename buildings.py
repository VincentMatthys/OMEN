# -*- coding: utf-8 -*-

import overpass

def get_buildings(response):
	"""
	Returns the list of buildings of the overpass api response
	"""

	# List of buildings
	buildings = []

	# For every element in the features of the reponse
	for element in response['features']:
		# when the feature is a building
		if 'building' in element['properties']:
			buildings.append(element)
	return buildings

def get_positions(features):
	"""
	Given a list of features, return the list of positions
	"""

	# List of positions
	positions = []

	# For every element in the features
	for element in features:
		# Append the list of coordinates
		positions.append(element['geometry']['coordinates'])

	return positions


"""
# Query by name
response = api.Get('node["name"="Salt Lake City"]')

print ([(feature['properties']['name'], feature['id']) for feature in response['features']])

"""

if __name__ == '__main__':
	api = overpass.API()
	# Query by map
	map_query = overpass.MapQuery(50.746,7.154,50.748,7.157)
	# Get the response from the API
	response = api.Get(map_query)
	# Get every buildings from this reponse
	buildings = get_buildings(response)
	# Get the positions of every buildings
	pos = get_positions(buildings)
