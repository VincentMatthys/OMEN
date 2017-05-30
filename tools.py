# -*- coding: utf-8 -*-

import pandas
import math

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
	Returns xmin, xmax (LON), ymin, ymax (LAT)
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

	return x - delta_x, x + delta_x, y - delta_y, y + delta_y


def call_api_mapQuery(xmin, xmax, ymin, ymax):
	"""
	Give the coordinates of the area where the site
	"""


if __name__ == '__main__':
	# Prefix for data storage
	prefix = "data/"

	# File containing coordinates of the site
	coord_sites_file = "Coordinates.csv"

	# Extension suffix for site antenna
	suffix = "_Antennes.csv"

	sites = get_features(prefix, coord_sites_file, suffix)

	for site in sites:
		sites[site]['area'] = area_per_site(sites[site])
