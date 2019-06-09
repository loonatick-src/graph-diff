#!/usr/bin/env python
import pydot


class Edge(object):
    '''
    Represent an edge in the graph.
    '''
    def __init__(self, src, dest, label=None):
        self.src = src
        self.dest = dest
        if not label:
            self.label = ""
        else:
            self.label = label
    
    def __eq__(self, other):
        return self.src == other.src and self.dest == other.dest and self.label == self.label

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "(" + self.src + ", " + self.dest + ")"

    def __hash__(self):
        return hash((self.src, self.dest, self.label))


class Graph(object):
    '''
    Represents a graph.
    '''
    def __init__(self, edges=None, nodes=None):
        if not edges:
            self.edges = set()
        else:
            self.edges = edges
        if not nodes:
            self.nodes = set()
        else:
            self.nodes = nodes


def generate_diff_graph(first_graph, second_graph):
    
    # generate nodes
    removed_nodes = set(first_graph.nodes) - set(second_graph.nodes)
    added_nodes = set(second_graph.nodes) - set(first_graph.nodes)
    nodes = set(second_graph.nodes) & set(first_graph.nodes)

    removed_edges  = first_graph.edges - second_graph.edges
    for removed_edge in removed_edges:
        if removed_edge.src in removed_nodes:
            removed_edge.src = "-" + removed_edge.src
        if removed_edge.dest in removed_nodes:
            removed_edge.dest = "-" + removed_edge.dest

    added_edges = second_graph.edges - first_graph.edges
    for added_edge in added_edges:
        if added_edge.src in added_nodes:
            added_edge.src = "+" + added_edge.src
        if added_edge.dest in added_nodes:
            added_edge.dest = "+" + added_edge.dest
    edges = second_graph.edges & first_graph.edges
    
    graph = Graph()
    for removed_node in removed_nodes:
        graph.nodes.add("-" + removed_node)
    for added_node in added_nodes:
        graph.nodes.add("+" + added_node)
    for node in nodes:
        graph.nodes.add(node)
    
    for removed_edge in removed_edges:
        graph.edges.add(Edge(removed_edge.src, removed_edge.dest, "-del"))
    for added_edge in added_edges:
        graph.edges.add(Edge(added_edge.src, added_edge.dest, "+add"))
    for edge in edges:
        graph.edges.add(edge)

    return graph


def from_dot(pydot_graph):
    graph = Graph()
    
    for node in pydot_graph.get_nodes():
        graph.nodes.add(node.get_name())
    
    for edge in pydot_graph.get_edges():
        graph.edges.add(Edge(edge.get_source(), edge.get_destination()))
    return graph


def to_dot(graph):
    pydot_graph = pydot.Dot(graph_type='graph')
    for edge in graph.edges:
        pydot_graph.add_edge(pydot.Edge(edge.src, edge.dest, label=edge.label))
    for node in graph.nodes:
        pydot_graph.add_node(pydot.Node(node))
    return pydot_graph
