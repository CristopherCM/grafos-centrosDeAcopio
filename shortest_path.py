import sys # Library for INT_MAX 
import csv

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
adjacency_matrix = []
centros_de_acopio = []

#Remove names from adjacency matrix and push into centros_de_acopio
with open('adjacency_matrix.csv', newline='') as csvfile:
	file_csv = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
	for node in file_csv:
		centros_de_acopio.append(node.pop(0))
		adjacency_matrix.append(list(map(float,node)))

#Find shortest path from origin to all nodes using Dijkstra
dijkstra(100, (len(adjacency_matrix)), adjacency_matrix, centros_de_acopio)