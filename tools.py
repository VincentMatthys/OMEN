# -*- coding: utf-8 -*-

import pandas

def extract_features(prefix = "data/", coord_sites_file = "Coordinates.csv", suffix = "_Antennes.csvr"):
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

if __name__ == '__main__':
	# Prefix for data storage
	prefix = "data/"

	# File containing coordinates of the site
	coord_sites_file = "Coordinates.csv"

	# Extension suffix for site antenna
	suffix = "_Antennes.csv"

	sites = extract_features(prefix, coord_sites_file, suffix)
