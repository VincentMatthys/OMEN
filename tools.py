# -*- coding: utf-8 -*-

import pandas

# File containing coordinates of the site
coord_sites_file = "data/Coordinates.csv"

# Open the csv file containing the coordinates of the site
with open(coord_sites_file, "r") as f:
	reader = pandas.read_csv(f, sep = ";")
# To get a dictionary like {'SITE' : XX, 'LAT' : YY , 'LON' : ZZZ}
sites = reader.to_dict(orient = 'records')
