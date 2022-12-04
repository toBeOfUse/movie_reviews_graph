import matplotlib.pyplot as plt
import networkx as nx
from movienetwork import network

def draw_graph():
    edge_weights = [e[2] for e in network.edges.data("weight")]
    min_weight, max_weight = min(edge_weights), max(edge_weights)
    weight_range = max_weight-min_weight
    normalize_weight = lambda e: (e-min_weight)/weight_range
    colors = [(1-normalize_weight(e), normalize_weight(e), 0, 1) for e in edge_weights]
    nx.draw_networkx(network, edge_color=colors)
    plt.draw()
    plt.show()

if __name__ == "__main__":
    for node, attributes in network.nodes.items():
        print(node, "was directed by", attributes["director"])
    draw_graph()
