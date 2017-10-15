"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""
#JSON = Dictionary
import sys
sys.path.append('../')
from graph import graph as gr
from search import searches
from queue import Queue
import json
import codecs

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, name, id):
        self.x = x
        self.y = y
        self.name = name
        self.id = id

    def __str__(self):
        return 'Tile(x: {}, y: {}, name: {}, id: {})'.format(self.x, self.y, self.name, self.id)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, name: {}, id: {})'.format(self.x, self.y, self.name, self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.name == other.name and self.id == other.id
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.name + self.id)

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

#Only works on neighbors
def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def construct_graph_from_state(graph, state):
    """
    Construct graph from a list of JSON states
    """

    #Create queue to store current states
    q = Queue()
    q.put(state)

    #construct nodes and edges and add them to graph
    while not q.empty():
        
        current_state = q.get()

        print("\nCurrent state:\n {}\n".format(current_state))

        state_id = current_state["id"]
        x = current_state["location"]["x"]
        y = current_state["location"]["y"]
        name = current_state["location"]["name"]

        neighbors = current_state["neighbors"]
        neighbors_states = []

        #Create tile for state
        tile = Tile(x, y, name, state_id)
        graph.add_node(gr.Node(tile)) #Add node to graph

        # State is the dark room
        if state_id == "f1f131f647621a4be7c71292e79613f9":
            print("Dark room found!")
            break

        #Generate actual states of neighbors using their id and store in new array
        for neighbor in neighbors:
            #Get state from neighbor id
            neighbor_id = neighbor["id"]
            neighbors_states.append(get_state(neighbor_id))
        
        #Construct edges between neighbor_states and state
        for neighbor in neighbors_states:
            #Add neighbor state to queue
            q.put(neighbor)

            neighbor_id = neighbor["id"]
            neighbor_x = neighbor["location"]["x"]
            neighbor_y = neighbor["location"]["y"]
            neighbor_name = neighbor["location"]["name"]
            neighbor_tile = Tile(neighbor_x, neighbor_y, neighbor_name, neighbor_id)
            #Get path between current state and neighbor
            path = transition_state(state_id, neighbor_id)
            #Get effect of path and store as edge.weight
            effect = path["event"]["effect"]
            graph.add_edge(gr.Edge(gr.Node(tile), gr.Node(neighbor_tile), effect))

    return graph

if __name__ == "__main__":
    
    states = []

    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')
    # neighbor = get_state('44dfaae131fa9d0a541c3eb790b57b00')

    # states.append(empty_room)
    # states.append(dark_room)

    # # Create empty room tile
    # empty_room_id = empty_room["id"]
    # empty_room_x = empty_room["location"]["x"]
    # empty_room_y = empty_room["location"]["y"]
    # empty_room_name = empty_room["location"]["name"]
    # empty_room_tile = Tile(empty_room_x, empty_room_y, empty_room_name, empty_room_id)

    # #Create dark room tile
    # dark_room_id = dark_room["id"]
    # dark_room_x = dark_room["location"]["x"]
    # dark_room_y = dark_room["location"]["y"]
    # dark_room_name = dark_room["location"]["name"]
    # dark_room_tile = Tile(dark_room_x, dark_room_y, dark_room_name, dark_room_id)

    # for neighbor in empty_room['neighbors']:
    #     for n in neighbor['neighbors']:
    #         states.append(n)
    #     states.append(neighbor)

    # for neighbor in dark_room['neighbors']:
    #     for n in neighbor['neighbors']:
    #         states.append(n)
    #     states.append(neighbor)
        

    #Testing
    # print("\n\nEmptyRoom: {}\n\n".format(empty_room))
    # print("\n\nNeighbor: {}\n\n".format(neighbor))
    # print("\n\nTransition: {}\n\n".format(transition_state(empty_room['id'], empty_room['neighbors'][0]['id'])))

    # # print("\n\n{}\n\n".format(empty_room['neighbors']))
    # # print("\n\nDarkRoom: {}\n\n".format(dark_room))
    # for neighbor in empty_room['neighbors']:
    #     path = transition_state('7f3dc077574c013d98b2de8f735058b4', neighbor['id'])
    #     print("\n\nPath to {}: {}\n\n".format(neighbor['id'], path))

    graph = construct_graph_from_state(gr.AdjacencyList(), empty_room)

    # print("Empty room tile: {}".format(empty_room_tile))
    # print("Dark room tile: {}".format(dark_room_tile))

    print("\ncurrent graph: \n\n{}".format(graph))

    #Use search algorithms to find path between empty room and dark room
    # listOfEdges = searches.bfs(current_graph, gr.Node(empty_room_tile), gr.Node(dark_room_tile))

    # print("\nResult:\n")
    # print(listOfEdges)
    # for edge in listOfEdges:
    #     print(edge)