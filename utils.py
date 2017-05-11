import networkx as nx
import matplotlib.pyplot as plt

def parse_neo4j_to_nx(results):
    G = nx.DiGraph()
    
    neo4j2node = {}
    
    # first pass add nodes
    num_nodes = 0
    for r in results:
        node_id = r[0].id
        #if node_id not in G:
        if node_id not in neo4j2node:
            neo4j2node[node_id] = num_nodes
            G.add_node(num_nodes, 
                       neo4j_id=node_id,
                       taxonomyCode=r[0].properties['taxonomyCode'])
            num_nodes += 1

    
    # now add edges
    num_edges = 0
    for r in results:
        if (r[0].id in neo4j2node and r[2].id in neo4j2node):
            node_id = neo4j2node[r[0].id]
            to_id = neo4j2node[r[2].id]
            edge_id = r[1].id

            if (node_id in G and to_id in G):
                    num_edges += 1
                    G.add_edge(node_id, to_id, edge_id=edge_id)
        
    print 'nodes:', num_nodes, 'edges:', num_edges
    return G

def clusterGraph(g, cluster):
    # add nodes in cluster to graph:
    gc = nx.DiGraph()
    for n_id in cluster:
        gc.add_node(n_id)
        
    # add edges to graph if both ends already in graph:
    for u, v in g.edges_iter():
        if (u in gc) and (v in gc):
            gc.add_edge(u, v)
        
    return gc

def labelClusters(graph, clusters):
    neo4j_ids = nx.get_node_attributes(graph, 'neo4j_id')
    labeledClusters = {}
    labeledNodes = {}
    for nx_id, neo4j_id in neo4j_ids.iteritems():
        labeledNodes[neo4j_id] = []
    
    for cluster, nodes in clusters.iteritems():
        labeledClusters[cluster] = []
        for node in nodes:
            labeledClusters[cluster].append(neo4j_ids[node])
            labeledNodes[neo4j_ids[node]].append(cluster)
            
    return labeledClusters, labeledNodes

def displayGraph(graph, title='', color_values = None):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_edges(graph, pos, arrows=True)
    nx.draw_networkx_nodes(graph, pos, cmap=plt.cm.Blues, node_color = color_values, alpha=0.8)

    nx.draw_networkx_labels(graph,pos)
    plt.title(title)
    plt.show()