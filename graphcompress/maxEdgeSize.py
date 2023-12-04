import gzip
import numpy as np

SUBSET = "latest-truthy_small"

max_id = -1
max_edges = -1

with gzip.open(f"{SUBSET}_compressed.gz") as file:
	for l in file:
		line = l.decode()
		line_split = line.split(" ")
		id_actual = int(line_split[0])
		total_edges = 0
		for edge in line_split[1:]:
			total_edges += len(edge.split(".")) - 1
		if (total_edges > max_edges):
			max_edges = total_edges
			max_id = id_actual
		print(id_actual,end="\r")
	print("Calculando máximo")
	print(f"Maximo : {max_edges}")
	print(f"MaxId  : {max_id}")
