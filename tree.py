import random

#---------------------------------------------------
class Tree(object):
	def __init__(self, id, data, left, right):
		self.id = id
		self.data = data
		self.left = left
		self.right = right

	def __str__(self):
		out = ''
		l = '' if self.left is None else self.left.__str__()
		r = '' if self.right is None else self.right.__str__()
		if l=='' and r=='':
			return '{}'.format(self.id)
		return '{}:({}, {})'.format(self.id, l, r)

	def node_ids(self):
		ids = ['{}.{}'.format(self.id,self.data)]
		left_ids = []
		right_ids = []
		if self.left is not None:
			left_ids = self.left.node_ids()
		if self.right is not None:
			right_ids = self.right.node_ids()
		return ids + left_ids + right_ids

#---------------------------------------------------
def draw(t, output='mytree', engine='dot', format='svg'):
	try:
		import graphviz
	except:
		print('Must install graphviz to draw graphs.')
		return

	def draw_tree_edges(node):
		u = '{}.{}'.format(node.id,node.data)
		if node.left is not None:
			v = '{}.{}'.format(node.left.id, node.left.data)
			gv.edge(str(u), str(v))
			draw_tree_edges(node.left)
		if node.right is not None:
			w = '{}.{}'.format(node.right.id, node.right.data)
			gv.edge(str(u), str(w))
			draw_tree_edges(node.right)

	gv = graphviz.Graph(format=format, engine=engine, strict=True, node_attr={'shape':'circle'})
	for vid in t.node_ids():
		gv.node(str(vid), str(vid))
	draw_tree_edges(t)
	print('Output saved to {}.{}'.format(output, format))
	gv.render(output)

	# g = pygraphviz.AGraph(strict=True, directed=False)
	# g.add_nodes_from(t.node_ids())
	# draw_tree_edges(t)
	# # g.graph_attr['dpi'] = 300
	# g.node_attr['shape'] = 'circle'
	# g.layout(prog='dot')
	# g.draw(output)
	# print('Graph image saved to', output)

#---------------------------------------------------
def random_tree(n, seed=None, colors=['red','blue']):
	def random_split(L):
		if len(L)==0:
			return None
		if len(L)==1:
			return L[0]
		i = random.randint(0,len(L)-1)
		root = L[i]
		root.left = random_split(L[0:i])
		root.right = random_split(L[i+1:])
		return root

	random.seed(seed)
	nodes = [ Tree(i+1, random.choice(colors), None, None) for i in range(n) ]
	tree = random_split(nodes)
	return tree

#---------------------------------------------------
def test_1():
	a = Tree(0,'red',None,None)
	b = Tree(1,'blue',None,None)
	c = Tree(2,'red',None,None)
	d = Tree(3,'blue',a,b)
	e = Tree(4,'yellow',c,d)
	print(e)
	print(e.node_ids())
	draw(e)

#---------------------------------------------------
def test_2():
	t = random_tree(20, colors=['r', 'g', 'b'])
	draw(t)

#---------------------------------------------------
# test_2()

