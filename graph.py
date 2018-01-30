import random

INFINITY = float("inf")

#----------------------------------------------------------
def random_weight(min_weight, max_weight):
	w = None
	if min_weight!=None and max_weight!=None and min_weight<=max_weight:
		w = random.randint(min_weight, max_weight)
	return w

#----------------------------------------------------------
# n - number of vertices
# p - edge probability
# directed - edge direction
#----------------------------------------------------------
def random_graph(
		n,
		p,
		directed=True,
		strict=True,
		seed=None,
		min_weight=None,
		max_weight=None,
	):
	random.seed(seed)
	if directed:
		g = DGraph()
	else:
		g = Graph()
	for i in range(n):
		g.add_vertex(i)
	for i in g.Vertices:
		for j in g.Vertices:
			if not strict or i!=j:
				if random.random() < p:
					g.add(i, j, random_weight(min_weight, max_weight))
				if directed and random.random() < p:
					g.add(j, i, random_weight(min_weight, max_weight))
	return g

#----------------------------------------------------------
# n - number of vertices
# p - edge probability
# directed - edge direction
#----------------------------------------------------------
def random_bipartite_graph(
		n, 
		m,
		p,
		directed=True,
		seed=None,
		min_weight=None,
		max_weight=None,
	):
	random.seed(seed)
	if directed:
		g = DGraph('group')
	else:
		g = Graph('group')

	for i in range(n):
		g.add_vertex(i)
		g[i].group = 0

	for i in range(n,m+n):
		g.add_vertex(i)
		g[i].group = 1

	for i in g.Vertices:
		for j in g.Vertices:
			if g[i].group != g[j].group:
				if random.random() < p:
					g.add(i, j, random_weight(min_weight, max_weight))
				if directed and random.random() < p:
					g.add(j, i, random_weight(min_weight, max_weight))
	return g

#----------------------------------------------------------
class Node(object):
	def __init__(self, id):
		self.id = id

	def __str__(self):
		out = 'Node {} '.format(self.id)
		attr = []
		for a in dir(self):
			if not a.startswith('__') and not a.endswith('__'):
				attr.append('{}: {}'.format(a, getattr(self,a)))
		if len(attr) > 0:
			out += '[' + '; '.join(attr) + ']'
		return out

#----------------------------------------------------------
class Graph(object):
	def __init__(self, *vertex_attrs):
		self.Edges = {}
		self.Vertices = {}
		self.Neighbors = {}
		self.vertex_attrs = vertex_attrs

	def add_vertex(self, i):
		if i not in self.Vertices:
			self.Vertices[i] = Node(i)
			for a in self.vertex_attrs:
				setattr(self.Vertices[i], a, None)
			self.Neighbors[i] = set()

	def delete_vertex(self, i):
		if i in self.Vertices:
			del self.Vertices[i]
			for j in self.Neighbors[i]:
				del self.Edges[i,j]
				del self.Edges[j,i]
				self.Neighbors[j].remove(i)
			del self.Neighbors[i]

	def add(self, i,j, w=None):
		self.Edges[i,j] = w
		self.add_vertex(i)
		self.Neighbors[i].add(j)
		self.Edges[j,i] = w
		self.add_vertex(j)
		self.Neighbors[j].add(i)

	def __getitem__(self, thing):
		if isinstance(thing, tuple):
			if thing not in self.Edges:
				return None
			return self.Edges[thing]
		else:
			if thing not in self.Vertices:
				return None
			return self.Vertices[thing]

	def __contains__(self, thing):
		if isinstance(thing, int):
			return thing in self.Vertices
		else:
			return thing in self.Edges

	def show(self):
		for v, n_v in self.Neighbors.items():
			print('Neighbors of node {}: {}'.format(v, n_v))

#----------------------------------------------------------
class DGraph(object):
	def __init__(self, *vertex_attrs):
		self.Edges = {}
		self.Vertices = {}
		self.In = {}
		self.Out = {}
		self.vertex_attrs = vertex_attrs

	def add_vertex(self, i):
		if i not in self.Vertices:
			self.Vertices[i] = Node(i)
			for a in self.vertex_attrs:
				setattr(self.Vertices[i], a, None)
			self.Out[i] = set()
			self.In[i] = set()

	def delete_vertex(self, i):
		if i in self.Vertices:
			del self.Vertices[i]
			OUT = [j for j in self.Out[i]]
			for j in OUT:
				del self.Edges[i,j]
				self.Out[i].remove(j)
				self.In[j].remove(i)
			del self.Out[i]
			IN = [j for j in self.In[i]]
			for j in IN:
				del self.Edges[j,i]
				self.Out[j].remove(i)
			del self.In[i]

	def add(self, i,j, w=None):
		self.Edges[i,j] = w
		self.add_vertex(i)
		self.Out[i].add(j)
		self.add_vertex(j)
		self.In[j].add(i)

	def __getitem__(self, thing):
		if isinstance(thing, tuple):
			if thing not in self.Edges:
				return None
			return self.Edges[thing]
		else:
			if thing not in self.Vertices:
				return None
			return self.Vertices[thing]

	def __contains__(self, thing):
		if isinstance(thing, int):
			return thing in self.Vertices
		else:
			return thing in self.Edges

	def show(self):
		for e,w in self.Edges.items():
			print('Edge {} has weight {}'.format(e,w))

#----------------------------------------------------------
def draw(g, output='mygraph', engine='dot', format='svg'):
	try:
		import graphviz
	except:
		print('Must install graphviz to draw graphs.')
		return

	if type(g) == Graph:
		gv = graphviz.Graph(format=format, engine=engine, strict=True, node_attr={'shape':'circle'})
	elif type(g) == DGraph:
		gv = graphviz.Digraph(format=format, engine=engine, strict=True, node_attr={'shape':'circle'})
	else:
		print('Unknown graph type')
		return

	for vid in g.Vertices:
		gv.node(str(vid), str(vid))
	for e,w in g.Edges.items():
		if w is not None:
			gv.edge(str(e[0]),str(e[1]),label=str(w))
		else:
			gv.edge(str(e[0]), str(e[1]))
	print('Output saved to {}.{}'.format(output, format))
	gv.render(output)

#----------------------------------------------------------

