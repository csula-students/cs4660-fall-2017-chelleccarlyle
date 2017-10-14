"""
utils package is for some quick utility methods

such as parsing
"""

from graph.graph import *

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    file = open(file_path, "r")
    lines = []
    # TODO: read the filepaht line by line to construct nodes & edges
    # TODO: for each node/edge above, add it to graph
    for line in file:
        lines.append(line)

    # Get rid of boundaries of grid 
    lines = lines[1:-1]
    lines = [line[1:-2] for line in lines]

    #Create 2d array
    for i, line in enumerate(lines):
        #Split into array for every two characters
        lines[i] = [line[i:i+2] for i in range(0, len(line), 2)]

    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            #Construct node using tile
            if tile != "##":
                graph.add_node(Node(Tile(x, y, tile)))

    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile != "##":
                #Construct edge for each direction, if possible
                #Check if 
                #Left - West
                if (x - 1) != -1 and lines[y][x - 1] != "##":
                    graph.add_edge(Edge(Node(Tile(x, y, tile)), Node(Tile(x - 1, y, lines[y][x - 1])), 1))
                #Right - East
                if (x + 1) != len(line) and lines[y][x + 1] != "##":
                    graph.add_edge(Edge(Node(Tile(x, y, tile)), Node(Tile(x + 1, y, lines[y][x + 1])), 1))
                #Up - North
                if (y - 1) != -1 and lines[y - 1][x] != "##":
                    graph.add_edge(Edge(Node(Tile(x, y, tile)), Node(Tile(x, y - 1, lines[y - 1][x])), 1))
                #Down - South
                if (y + 1) != len(lines) and lines[y + 1][x] != "##":
                    graph.add_edge(Edge(Node(Tile(x, y, tile)), Node(Tile(x, y + 1, lines[y + 1][x])), 1))
    
    file.close()

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """

    result = ""

    for edge in edges:
        if edge.from_node.data.x > edge.to_node.data.x:
            result += "W"
        elif edge.from_node.data.x < edge.to_node.data.x:  
            result += "E"
        elif edge.from_node.data.y > edge.to_node.data.y:  
            result += "N"
        elif edge.from_node.data.y < edge.to_node.data.y:  
            result += "S"

    return result
