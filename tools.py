# -*- coding: utf-8 -*-

import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

#from buildings import *
#from map import *
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
	Given a list of features, return a dictionary of positions :
		- StreetMap id of the building : np.array(pos)
	Input format, with the actual dictionary :
		- get_positions(sites['site_name']['buildings'])
	"""

	# dictionary of positions
	positions = {}

	# For every element in the features
	for element in features:
		# Append the list of coordinates
		positions[element["id"]] = np.array(element['geometry']['coordinates'])

	return positions

def plot_buildings(positions):
	"""
	Given the list of positions of buildings (polygons), plot them
	"""

	for b in positions:
		temp = np.array(b)
		plt.plot(temp[:, 0], temp[:, 1], c = 'b')

def convert_metter_to_longitude(distance, lattitude):
	"""
	Given a distance in metter, and the lattitude, returns the corresponding deltalongitude
	"""
	return 360 * distance / (40075160 * math.cos(math.pi * lattitude / 180))

def plot_map(site):
	"""
	Given a site stored in the sites dictionary, plot the buildings, then the antenna and the radius
	"""

	plt.figure()

	plot_buildings(get_positions(site['buildings']))

	# Position of the antenna
	x_a, y_a = site['LON'], site['LAT']

	# Perimeter of the antenna_field
	per = site['Antennes'][0]['Perimeter']

	antenna_field = plt.Circle((x_a, y_a), convert_metter_to_longitude(per, y_a), color = 'r')

	plt.gcf().gca().add_artist(antenna_field)
	plt.show()



def get_features(prefix = "data/", coord_sites_file = "Coordinates.csv", suffix = "_Antennes.csvr"):
	"""
	prefix : path where the .csv are stored
	coord_sites_file : name of the file containing the sites positions
	suffix : extensions for the features of each site, like :
			-- GE_002A_Antennes.csv
			-- GE_0014C_Antennes.csv
			=> suffix = "_Antennes.csv"

	Returns a dictionary :
		- values : sites
		- keys :
			-- list of antenna and their features
			-- lattitude of the site
			-- longitude of the site
	"""

	# Open the csv file containing the coordinates of the site
	with open(prefix + coord_sites_file, "r") as f:
		reader = pandas.read_csv(f, sep = ";")
	# To get a dictionary like {'SITE' : XX, 'LAT' : YY , 'LON' : ZZZ}
	sites = reader.set_index('SITE').T.to_dict()

	for site in sites:
		with open(prefix + site + suffix, "r") as f:
			features = pandas.read_csv(f, sep = ";")
			sites[site]['Antennes'] = features.to_dict(orient = 'records')

	return sites

def get_xy_pos(p1, p2):
	"""
	Calculates X and Y distances in meters.
	p[0] : longitude
	p[1] : lattitude
	"""

	# Equator perimeter
	equator = 40075160

	# Delta lat / long
	deltaLatitude = p2[1] - p1[1]
	deltaLongitude = p2[0] - p1[0]

	# Conversion into meter
	resultX = deltaLongitude * (equator * cos(pi * p1[1] / 360)) / 360
	resultY = deltaLatitude * equator / 360
	return abs(resultX), abs(resultY)

def convert_metter_to_longitude(distance, lattitude):
	"""
	Given a distance in metter, and the lattitude, returns the corresponding deltalongitude
	"""
	return 360 * distance / (40075160 * math.cos(math.pi * lattitude / 180))

def convert_metter_to_lattitude(distance):
	"""
	Given a distance in metter, give the equivalence in deltalattitude
	"""

	return distance * 360 / 40075160

def area_per_site(site, factor = 2):
	"""
	Given a site as returned by the get_features function, find the maximal perimeter of the antennas.
	Factore is the multiplicatif constant applied to the window defined by the perimeter
	With this max, define an area to call the Overpass API with the call_api_mapQuery function
	Returns the format asked to call api by MapQuery method :
	south, west, north, east :
	ymin, xmin, ymax, xmax
	"""

	# Position of the site
	x = site['LON']
	y = site['LAT']

	# Initialize the minimal perimeter
	perimeter = 0

	# Find the maximal parameter
	for antenna in site['Antennes']:
		if 'Perimeter' in antenna and perimeter < antenna['Perimeter']:
			perimeter = antenna['Perimeter']

	# Size of area around the site, in longitude
	delta_x = factor * convert_metter_to_longitude(perimeter, y)

	# Size of area around the site, in lattitude
	delta_y = factor * convert_metter_to_lattitude(perimeter)

	return y - delta_y, x - delta_x, y + delta_y, x + delta_x


def call_api_mapQuery(site, api, sites):
	"""
	Give the buildings of an area as defined by the area_per_site function
	Entry : take the sites dictionary
	Returns the list of buildings found on the api
	"""

	south, west, north, east = area_per_site(sites[site])

	# Query by map
	map_query = overpass.MapQuery(south, west, north, east)

	# Get the response from the API
	response = api.Get(map_query)

	# Get every buildings from this reponse
	buildings = get_buildings(response)

	return buildings

def map_to_antenna(sites, site_name):
	"""
	Given the sites dictionary and a site_name, returns a dictionary as following :
		- Position of the site (LON, LAT)
		- Relative positions of the antennas
		- Relative positions of the buildings
	"""

	relative = {}
   
	# Position of the site
	x_site = sites[site_name]['LON']
	y_site = sites[site_name]['LAT']
	relative[site_name] = {'LAT' : y_site, 'LON' : x_site}

	# Relative position of the antemma
	relative['Antennes'] = sites[site_name]['Antennes']

	# Relative positions of the buildings
	pos_buildings = get_positions(sites[site_name]['buildings'])

	for building in pos_buildings:
		pos_buildings[building] -= (x_site, y_site)

	relative['buildings'] = pos_buildings

	return relative

################################################################################
############################### MAIN ###########################################
################################################################################

if __name__ == '__main__':
	# Prefix for data storage
	prefix = "data/"

	# File containing coordinates of the site
	coord_sites_file = "Coordinates.csv"

	# Extension suffix for site antenna
	suffix = "_Antennes.csv"

	sites = get_features(prefix, coord_sites_file, suffix)

	api = overpass.API()
	for site in sites:
		print ("J'ai tourné")
		sites[site]['buildings'] = call_api_mapQuery(site, api)


	#plot_map(sites['GE_0002A'])
