from sklearn.neighbors import NearestNeighbors
import numpy as np


X = np.array([[.5, .5], [0, .5 ], [-2, -2], [-2, -3], [-3, -2]])
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

#change the n_neighbors = k to get k nearest neighbors
#print(distances)
#print(indices)

Xplus = np.vstack(([1, 1], X))
nbrsplus = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(Xplus)
#print(Xplus)
distances, indices = nbrsplus.kneighbors(Xplus)
#print(distances) 
print(indices)

def machinelearn():
	#insert thing that iterates dict of bloggers and their weights
	for i in range(5):
		if sum(indices[i])>5:
			print("buy")
		else:
			print("sell")


machinelearn()

