import csv
import hashlib

class node_chido:

	direccion, necesidades, tipo = "","",""

	def __init__(self, direccion, necesidades, tipo):
		self.direccion, self.necesidades, self.tipo = direccion, necesidades, tipo

	def print_node(self):
		print(self.direccion, self.necesidades, self.tipo)

class hash_entry:

	value = node_chido
	key = ""

	def __init__(self, value, key):
		self.value = value
		self.key = key

	def get_key(self):
		return self.key

	def get_value(self):
		return self.value

class hash_table:

	table = []*10000

	def __init__(self):
		self.table = [[]]*10000

	def insert(self, key, value):
		if(len(key) == 0):
			return
		else:
			entry = hash_entry(value,key)
			index = 0
			for i in list(key):
				index = index + ord(i)

			print(index)
			self.table[index].append(entry)
			print(index)

	def value(self,key):
		if(len(key) == 0):
			return
		else:
			index = 0
			for i in list(key):
				index = index + ord(i)

			#Colisiona
			if len(self.table[index])>1:
				for entry in self.table[index]:
					if key == entry.get_key():
						print(entry.get_value().print_node())
			#pOS NO COLISIONA
			else:
				print("No Colisiono")
				print(self.table[index][0].get_value().print_node())

	def print_table(self):
		for l in range(329):
			for n in self.table[l]:
				print(n.get_value().print_node(), " - ", n.get_key())






#====================== MAIN =========================
hash_tab = []


#Remove names from adjacency matrix and push into centros_de_acopio
with open('hash_table.csv', newline='') as csvfile:
	file_csv = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
	for node in file_csv:
		hash_tab.append(node)

ht = hash_table()

n = node_chido(hash_tab[1][2], hash_tab[1][3], hash_tab[1][4])
ht.insert(hash_tab[1][1], n)

n2 = node_chido(hash_tab[2][2], hash_tab[2][3], hash_tab[2][4])
ht.insert(hash_tab[2][1], n2)

ht.value("Beyork Loreto")
ht.value("Gimnasio G3")


