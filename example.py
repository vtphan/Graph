from graph import Graph, DGraph

print("Example of unweighted undirected graph")
G = Graph()
G.add(2,3)       						# add edge (2,3); (3,2) is automatically addeded.
G.add(3,5)       						# add edge (3,5); (5,3) is automatically addeded.
G.add(3,10)      						# add edge (3,10); (10,3) is automatically addeded.
print( (3,5) in G )					# True
print( (5,3) in G )					# True
print( (10,5) in G )					# False
for v in G.Vertices:
	print("vertex", v)
for e in G.Edges:
	print("edge", e)
print("Neighbors of vertex 3:")
for v in G.Neighbors[3]:
	print("\t", v)

print("\nExample of weighted directed graph")
D = DGraph()
D.add(2,3,10)
D.add(2,5,20)
D.add(3,5,30)
for e in D.Edges:
	print("Edge", e, "has weight", D[e])

print("Vertices that vertex 3 points to")
for v in D.Out[3]:
	print("\t", v)
print("Vertices that point to vertex 5.")
for v in D.In[5]:
	print("\t", v)
