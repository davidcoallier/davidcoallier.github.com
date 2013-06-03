from __future__ import with_statement

from pymongo import Connection
from collections import Counter
import sys
import json
import numpy as np
import pandas as pd
import string
import networkx as nx
import networkx.readwrite as nxrw


category = sys.argv[1] if len(sys.argv) > 1 else 'web'

def most_influential(G):
    rank = nx.centrality.eigenvector_centrality(G).items()
    r = [x[1] for x in rank]

    m = np.mean(r) 
    t = m*5
    traversed = G.copy()
    for k, v in rank:
        if v < t:
            traversed.remove_node(k)
    return traversed, rank

def most_bridges(G):
    rank = nx.centrality.betweenness_centrality(G).items()
    r = [x[1] for x in rank]

    m = np.mean(r) 
    t = m*5
    traversed = G.copy()
    for k, v in rank:
        if v < t:
            traversed.remove_node(k)
    return traversed, rank

def clean_main_graph(G, graph):
    conn_mean = np.median([x for x in graph.values()])
    #to_remove = [(x, y) for x, y in graph.iteritems()]
    traversed = G.copy()
    for k, v in graph.iteritems():
        if v < conn_mean*5:
            traversed.remove_node(k)
    return traversed


conn = Connection()
db   = conn['exp003']
col  = db['crunchbase']

find = col.find(
    {"funding_rounds": {"$not": {"$size": 0}}, "category_code": category}
)

print
print "Fetched %s records" % find.count() 
print
graph = Counter()
G = nx.Graph()
investors = {}
for inv in find:
    comp = set()
    rounds = inv['funding_rounds']
    for inv_round in rounds:
        if 'investments' in inv_round:
            invs = inv_round['investments']
            for inv in invs:
                if 'person' in inv and inv['person'] is not None:
                    fname = ''.join(ch for ch in inv['person']['first_name'] if ch.isalnum())
                    lname = ''.join(ch for ch in inv['person']['last_name'] if ch.isalnum())

                    graph += Counter({"%s-%s" % (fname, lname)})
                    comp.add("%s-%s" % (fname, lname))
    if len(comp) > 0:
        for name in comp:
            G.add_node(name)
            #print "Node: %s" % name
            [G.add_edge(name, l) for l in comp if l != name]

gt, rank = most_influential(G)
br, brank = most_bridges(G)

# Normal Graph.
Cg = G.copy()

if len(Cg.nodes()) > 100:
    Cg = clean_main_graph(G, graph)

deps = []
for node in Cg.nodes():
    edges = [x[1] for x in Cg.edges(node)]
    deps.append({"name": node, "size": graph[node], "imports": edges}) 

with open('d3/data/person/%s-graph.json' % category, 'w+') as f:
    f.write(json.dumps(deps))


# First we save the people that are influential.
deps = []
for node in gt.nodes():
    edges = [x[1] for x in gt.edges(node)]
    deps.append({"name": node, "size": graph[node], "imports": edges}) 

with open('d3/data/person/%s-graph-influential.json' % category, 'w+') as f:
    f.write(json.dumps(deps))


# Second we show bridge builders.
deps = []
for node in br.nodes():
    edges = [x[1] for x in br.edges(node)]
    deps.append({"name": node, "size": graph[node], "imports": edges}) 

with open('d3/data/person/%s-graph-bridges.json' % category, 'w+') as f:
    f.write(json.dumps(deps))

rank.sort(key=lambda x: x[-1], reverse=True)
brank.sort(key=lambda x: x[-1], reverse=True)

top10prank = rank[0:int(round(len(rank) - (len(rank)-len(rank)*0.10)))]
top10pbrank = brank[0:int(round(len(brank) - (len(brank) - len(brank)*0.05)))]

with open('d3/data/person/%s-centrality.json' % category, 'w+') as f:
    f.write(json.dumps({
        "count": find.count(),
        "betweenness": top10prank, 
        "eigen": top10pbrank
    }))
