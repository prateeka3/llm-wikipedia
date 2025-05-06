import networkx as nx
import json

class Node:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

class Edge:
    def __init__(self, source_id: int, target_id: int, relationship: str):
        self.source_id = source_id
        self.target_id = target_id
        self.relationship = relationship

class Graph:
    def __init__(self):
        self.G = nx.DiGraph()
    
    def to_json(self):
        return json.dumps(nx.node_link_data(self.G), indent=4)

    def from_json(self, json_str: str) -> 'Graph':
        self.G = nx.node_link_graph(json.loads(json_str))
        return self
    
    def add_node(self, node: Node):
        self.G.add_node(node.id, name=node.name, description=node.description)
    
    def add_edge(self, edge: Edge):
        self.G.add_edge(edge.source_id, edge.target_id, relationship=edge.relationship)
    
    def __str__(self):
        return self.to_json()
    
    
if __name__ == "__main__":
    graph = Graph()
    graph.add_node(Node(1, "Node 1", "Description 1"))
    graph.add_node(Node(2, "Node 2", "Description 2"))
    graph.add_edge(Edge(1, 2, "Relationship 1"))
    print(graph)