# -*- coding: utf-8 -*-

from buildings import *
import matplotlib.pyplot as plt
import numpy as np
import overpass

def plot_buildings(positions):
	"""
	Given the list of positions of buildings (polygons), plot them
	"""

	for b in positions:
		temp = np.array(b)
		plt.plot(temp[:, 0], temp[:, 1], c = 'b')
	plt.show

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

	plt.figure()
