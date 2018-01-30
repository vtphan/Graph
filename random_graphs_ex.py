import graph

g = graph.random_graph(6,0.3,directed=True,min_weight=1,max_weight=10)
graph.draw(g)