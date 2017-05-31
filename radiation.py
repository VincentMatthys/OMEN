# -*- coding: utf-8 -*-


def extract_radiation_value(fichier):
	"""
	Extract the radiation value from the radiation pattern input file
	The file has to contain :
	- Introduction part with some technical content
	- First part :
		-- HORIZONTAL + Number of Discretisation (first line)
		-- Angle + Value (for other lines)
	- Second part :
		-- HORIZONTAL + Number of Discretisation (first line)
		-- Angle + Value (for other lines)
	"""
	# Ouvterdure du fichier en lecture seulemenbt
	f = open(fichier, 'r')

	# Lecture de la première ligne du fichier
	ligne = f.readline()

	# Initialisation de la liste des valeurs :
	# 	- values[0] : horizontal attenuation - dictionary
	#	- values[1] : vertical attenuation - dictionary
	values = [{}, {}]

	# cur vaut 0 si horizontal part, 1 si vertical, -1 si partie introductive
	cur = -1

	# Variable de stockage de la discrétisation
	size = 0

	# Boucle sur toutes les lignes non vides de ligne
	while ligne != "":
		# Splited ligne
		split = ligne.split()
		# Si la ligne marque le début de la partie horizontal :
		if split[0] == 'HORIZONTAL' or split[0] == 'VERTICAL':
			if split[0] == 'HORIZONTAL':
				cur = 0
			else:
				cur = 1
			size = int(split[1])
			ligne = f.readline()
			split = ligne.split()

		# If we are in the first or second part, add values to current dictionary
		if cur >= 0:
			values[cur][float(split[0])] = float(split[1])
		# Go to the next ligne
		ligne = f.readline()
	return values[0], values[1]

################################################################################
################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
	rad_h, rad_v = extract_radiation_value("data/antenna/80010664_0821_x_co_m45_02t.msi")
