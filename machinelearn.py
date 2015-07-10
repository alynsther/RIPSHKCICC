from sklearn.neighbors import NearestNeighbors
import numpy as np

#x is an example array
#'ball-tree' is just a sorting algorithm
X = np.array([[.5, .5], [0, .5 ], [-2, -2], [-2, -3], [-3, -2]])
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

#change the n_neighbors = k to get k nearest neighbors
#print(distances) prints the distances between an object and its nearest neighbors
#print(indices) prints an array of lists where the first element is a series of 3 of the nearest neighbors
# the nth element is a series of the 3 of the nearest elements to the nth element.

#this is how you append an array using numpy
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

