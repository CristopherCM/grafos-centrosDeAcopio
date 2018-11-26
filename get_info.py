# pip3 install --upgrade google-api-python-client oauth2client
# pip3 install gspread
# you must have a client_secret.json

import gspread
import random
import csv
import sys
from oauth2client.service_account import ServiceAccountCredentials
from math import sin, cos, sqrt, atan2, radians

import sys # Library for INT_MAX 
  
def get_distance(lat1, lon1, lat2, lon2):
	# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return c * 6373.0 #radius of earth in km

def get_data(names):
	# https://www.youtube.com/watch?v=vISRn5qFrkM
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open('centros_acopio').sheet1 # this document is already shared
	centros_de_acopio = sheet.get_all_records()

	coor = []
	for r in centros_de_acopio:
		if type(r['id']) is int: # is not empty
			if type(r['lat']) is float: # is not empty
				names.append(r['Nombre del centro de acopio'])
				coor.append([r['lat'],r['lon']])
	return coor

def export_to_csv(matrix, names):
	#https://docs.python.org/3/library/csv.html
	to_csv = []
	for i in range(0, len(matrix)):
		to_csv.append(matrix[i])
		to_csv[i].insert(0, names[i])
	
	with open('adjacency_matrix.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(to_csv)

def export_dijkstra(dist,vertices,centros_de_acopio):
	to_csv = []

	for i in range(vertices):
		"""
		In cases where the distance stands as MAX_INT
		We output 'Distance too long to compute'
		"""
		if dist[i] == sys.maxsize:
			distance = "Distance too long to compute / No path found form origin to destination" 
		else:
			distance = dist[i]
		to_csv.append([centros_de_acopio[i],distance])

	to_csv.insert(0,["Destino","Distancia desde Origen"])

	with open('rutas_cortas.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(to_csv)


def print_solution(dist,vertices,centros_de_acopio): 
	print ("Destino  -  Distancia desde Origen")
	"""
	In cases where the distance stands as MAX_INT
	We output 'Distance too long to compute'
	"""	
	for i in range(vertices): 
		if dist[i] == sys.maxsize:
			distance = "Distance too long to compute / No path found form origin to destination"
		else:
			distance = dist[i]
		print (centros_de_acopio[i],"  -  ", distance)
	export_dijkstra(dist,vertices,centros_de_acopio)
	print("****** Solution exported to csv ******")
  

def min_distance(dist, spath_set,vertices): 

    min = sys.maxsize 
    min_index = -1

    for v in range(vertices): 
        if dist[v] < min and spath_set[v] == False: 
            min = dist[v] 
            min_index = v 

    return min_index 

"""
Find shortest path to all nodes from origin, print them, and export them to csv file.
Using Dijkstra's Algorithm and an adjacency list

@param integer 	origin: 			Index of the Origin
@param integer 	vertices: 			Number of vertices in matrix
@param list 	adjacency_matrix: 	Graph represented in adjacency list
@param list 	centros_de_acopio:	List of names to be used in printing and exporting.

"""
def dijkstra(origin,vertices,adjacency_matrix,centros_de_acopio): 

    dist = [sys.maxsize] * vertices 
    dist[origin] = 0
    spath_set = [False] * vertices 

    for i in range(vertices): 

        u = min_distance(dist, spath_set,vertices) 

        spath_set[u] = True

        for v in range(vertices): 
            if (adjacency_matrix[u][v] > 0) and (spath_set[v] == False) and (dist[v] > dist[u] + adjacency_matrix[u][v]): 
                    dist[v] = dist[u] + adjacency_matrix[u][v] 

    print_solution(dist,vertices,centros_de_acopio) 
	

#====================== MAIN =========================
centros_de_acopio = [] # pass by reference
coordinates = get_data(centros_de_acopio)
length = len(coordinates)
adjacency_matrix = [[0 for col in range(length)] for row in range(length)] #initialices the matrix with 0's

#fill the matrix
for i in range(0,length):
	for j in range(0,length):
		if j != i:
			distance = (get_distance(coordinates[i][0], coordinates[i][1], coordinates[j][0], coordinates[j][1]))
			if distance < 10:
				adjacency_matrix[i][j] = distance

#connect disconnected vertices
for y in range(0, length):
	z = 0
	while adjacency_matrix[y][z] == 0:
		z += 1
		if z == length - 1:
			break
	if(z == length - 1):
		#it's alone
		someone_to_connect = random.randint(0,length - 1) #choose j
		distance = get_distance(coordinates[y][0], coordinates[y][1], coordinates[someone_to_connect][0], coordinates[someone_to_connect][1])
		adjacency_matrix[y][someone_to_connect] = distance
		adjacency_matrix[someone_to_connect][y] = distance

		# print(str(y) + "  ", end = "")
		# print(str(centros_de_acopio[y]) + " - ", end='')
		# print(adjacency_matrix[y])

#write csv
export_to_csv(adjacency_matrix, centros_de_acopio)

#Remove names from adjacency matrix
for node in adjacency_matrix:
	node.pop(0)
#Find shortest path from origin to all nodes using Dijkstra
dijkstra(100, (len(adjacency_matrix)), adjacency_matrix, centros_de_acopio)

# #print all the matrix
# for y in range(0, length):
# 	print(str(y) + " - " + str(centros_de_acopio[y]) + " - ", end='')
# 	print(adjacency_matrix[y])