# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import overpass
from tools import convert_metter_to_longitude

import sys

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

#def plot_antennas()

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

	#test = np.array(pos[0])
