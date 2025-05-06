from data.graph import Graph, Node, Edge
import networkx as nx
import matplotlib.pyplot as plt

def simple_viz(graph: Graph):
    # Create a mapping of node IDs to their names
    labels = {node: data.get('name', str(node)) for node, data in graph.G.nodes(data=True)}
    nx.draw(graph.G, labels=labels, with_labels=True)
    plt.show()

def simple_viz_from_json(json_str: str):
    graph = Graph().from_json(json_str)
    simple_viz(graph)
    plt.show()

if __name__ == "__main__":
    graph = Graph()
    simple_viz(graph)

    graph.add_node(Node(1, "Node 1", "Description 1"))
    graph.add_node(Node(2, "Node 2", "Description 2"))
    graph.add_edge(Edge(1, 2, "Relationship 1"))
    simple_viz(graph)
