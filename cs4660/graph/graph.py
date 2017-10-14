"""
Implemented by Chelle Cruz
CS 4660
"""

"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    file = open(file_path, "r")

    for i, line in enumerate(file):
        if i == 0:
            #Get number of nodes from first line and add nodes to graph
            num_of_nodes = int(line)  
            for n in range(num_of_nodes):
                graph.add_node(Node(n))
        else:
            #Add edge to graph
            #First split string into array
            edge = line.split(":")
            graph.add_edge(Edge(Node(int(edge[0])), Node(int(edge[1])), int(edge[2]))) 

    file.close()

    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        #find edge where from_node = node_1 and to_node = node_2
        listOfEdges = self.adjacency_list[node_1]

        for edge in listOfEdges:
            if edge.to_node == node_2:
                return True
            
        return False

    def neighbors(self, node):
        neighbors = []
        for edge in self.adjacency_list[node]:
            neighbors.append(edge.to_node)
        return neighbors

    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        else:
            #Add node to dictionary with empty array of edges
            self.adjacency_list[node] = []
            return True

    def remove_node(self, node):
        if node in self.adjacency_list:
            #Remove node key
            del self.adjacency_list[node]
            #Also remove edges where node = to_node from adjacency list
            for listOfEdges in self.adjacency_list.values():
                for edge in listOfEdges:
                    if edge.to_node == node:
                        self.remove_edge(edge)
            return True
        else:
            return False

    def add_edge(self, edge):
         #Edge already exists
         if edge in self.adjacency_list[edge.from_node]:
             return False
         else:
            #Add edge to corresponding from_node in adjacency list
            self.adjacency_list[edge.from_node].append(edge)
            return True

    def remove_edge(self, edge):
        if edge in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].remove(edge);
            return True
        else:
            return False

    #Distance of two adjacent nodes
    def distance(self, node_1, node_2):
        
        #get list of edges from node_1
        listOfEdges = self.adjacency_list[node_1]

        for edge in listOfEdges:
            if edge.to_node == node_2:
                return edge.weight

        return None

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        #Get index of node_1 = from_node and node_2 = to_node
        node_1_index = self.__get_node_index(node_1)
        node_2_index = self.__get_node_index(node_2)

        if self.adjacency_matrix[node_1_index][node_2_index] != 0:
            return True
        else:
            return False

    def neighbors(self, node):
        neighbors = []
        node_index = self.__get_node_index(node)
        row = self.adjacency_matrix[node_index]

        for index, weight in enumerate(row):
            if weight != 0:
                #This is a neighbor; get corresponding node from nodes
                neighbors.append(self.nodes[index])

        return neighbors

    def add_node(self, node):
        #Node already exists
        if node in self.nodes:
            return False
        else:
            #Add a 0 to each row of adjacency matrix
            for row in self.adjacency_matrix:
                row.append(0);
            #Add node to nodes
            self.nodes.append(node)
            #Add row of 0s with size of nodes to adjacency matrix which will represent corresponding node
            self.adjacency_matrix.append([0] * len(self.nodes))
            
            return True

    def remove_node(self, node):
        if node in self.nodes:
            #Get index of node from nodes array
            index = self.__get_node_index(node)
            del self.nodes[index] #Remove element corresponding to node
            del self.adjacency_matrix[index] #Remove row corresponding to node
            for row in self.adjacency_matrix:
                del row[index] #Remove column corresponding to node

            return True
        else:
            return False

    def add_edge(self, edge):
        #Check if edge already exists
        #Get indexes of from_node and to_node
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)

        if self.adjacency_matrix[from_node_index][to_node_index] != 0:
            return False
        else:
            #Add edge weight to matrix
            self.adjacency_matrix[from_node_index][to_node_index] = edge.weight
            return True

    def remove_edge(self, edge):
        #Check if edge exists
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)

        if self.adjacency_matrix[from_node_index][to_node_index] != 0:
            self.adjacency_matrix[from_node_index][to_node_index] = 0
            return True
        else:
            return False

    #Distance of two adjacent nodes
    def distance(self, node_1, node_2):
        return self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)]

    def __get_node_index(self, node):
        """helper method to find node index"""
        if node in self.nodes:
            return self.nodes.index(node)

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return True

        return False

    def neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge.from_node == node:
                neighbors.append(edge.to_node)

        return neighbors

    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            return True

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            #Also remove edges where node = to_node or node = from_node from edges
            for edge in self.edges:
                if edge.from_node == node or edge.to_node == node:
                    self.edges.remove(edge)
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge in self.edges:
            return False
        else:
            self.edges.append(edge)
            return True

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        else:
            return False

    #Distance of two adjacent nodes
    def distance(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return edge.weight

        return None      

#Test
if __name__ == "__main__":
    print("Test")