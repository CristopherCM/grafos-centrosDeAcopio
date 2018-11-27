import sys
import csv

def export_prim(dist, padre, vertices, centros_de_acopio):
    to_csv = []

    for i in range(1, vertices):
        if dist[i] == sys.maxsize:
            #No existe conexión
            pass
        else:
            conection = "%d - %d" % (padre[i], i)
            distance = adjacency_matrix[i][padre[i]]
            to_csv.append([conection, distance])

    to_csv.insert(0,["Conexion","Distancia"])

    with open('arbol_abarcador.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(to_csv)

def print_solution(dist, padre, vertices, centros_de_acopio):
    print("Conexión \tDistancia")
    for i in range(1, vertices):
        if dist[i] == sys.maxsize:
            #No existe conexión
            pass
        else:
            print(padre[i]," - ", i,"\t", adjacency_matrix[i][padre[i]])

    export_prim(dist, padre, vertices, centros_de_acopio)
    print("****** Solution exported to csv ******")


def min_distance(dist, mstSet, vertices):
    min = sys.maxsize
    min_index = -1

    for v in range(vertices):
        if dist[v] < min and mstSet[v] == False:
            min = dist[v]
            min_index = v
    return min_index

def prim(vertices, adjacency_matrix, centros_de_acopio):
    dist = [sys.maxsize] * vertices
    padre = [None] * vertices
    dist[0] = 0
    mstSet = [False] * vertices

    padre[0] = -1

    for cout in range(vertices):
        u = min_distance(dist, mstSet, vertices)
        mstSet[u] = True

        for v in range(vertices):
            if adjacency_matrix[u][v] > 0 and mstSet[v] == False and dist[v] > adjacency_matrix[u][v]:
                dist[v] = adjacency_matrix[u][v]
                padre[v] = u
    print_solution(dist, padre, vertices, centros_de_acopio)


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
prim(len(adjacency_matrix), adjacency_matrix, centros_de_acopio)
