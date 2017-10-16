"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

# DON'T NEED TO CREATE A GRAPH FROM SCRATCH: THE SERVER IS THE GRAPH!
# JSON OF STATE IS THE NODE
# JSON OF TRANSITION STATE IS THE EDGE
# Node will store JSON as data of state

#JSON = Dictionary
import sys
sys.path.append('../')
from graph import graph as gr
# from search import searches
from queue import Queue, PriorityQueue
import json
import codecs
import time

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"


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

def get_neighbors(node, discoveredNodes):
    """
    Gets neighbors from node consisiting of JSON data (uses the JSON data to get neighbors)
    Returns a list of nodes consisting of JSON data
    """

    neighbors = []

    #Get json data from node
    state = node.data
    neighbors_json = state["neighbors"]

    for neighbor in neighbors_json:
        alreadyDiscovered = False
        #Get state from neighbor id
        neighbor_id = neighbor["id"]
        for node in discoveredNodes:
            if node.data["id"] == neighbor_id:
                alreadyDiscovered = True
                break
        if not alreadyDiscovered:
            neighbors.append(get_state(neighbor_id))

    #Convert states to nodes in neighbors
    for i, neighbor in enumerate(neighbors):
        neighbors[i] = gr.Node(neighbor)

    return neighbors

def get_distance(node_1, node_2):
    """
    Gets the distance (edge weight = effect) of two nodes
    """
    #Get states
    state_1 = node_1.data
    state_2 = node_2.data
    #Get transition state from state ids
    path = transition_state(state_1["id"], state_2["id"])
    
    #Return the event effect from path as edge cost
    return path["event"]["effect"]

def get_node_str(node):
    data = node.data
    return "{}({})".format(data['location']['name'], data['id'])

def get_edge_str(edge):
    #get from node, to node and edge weight
    weight = edge.weight

    from_node_string = get_node_str(edge.from_node)
    to_node_string = get_node_str(edge.to_node)

    return "{}:{}:{}".format(from_node_string, to_node_string, weight)

def dijkstra_search(initial_node, dest_node):
    
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    #Distance of each node
    #Parents of each node
    #Actions will be list of edges returned
    #For priority queue, you want to get the highest distance (effect): must make distances negative when putting to priority queue
    distances = {}
    parents = {}
    actions = []
    discoveredNodes = []

    #Create priority queue
    queue = PriorityQueue()

    initial_node.isDiscovered = False

    #Set distance of initial_node to 0
    distances[initial_node] = 0

    #Create counter for priority queue in case there is a tie between distances of nodes, will get node that comes in first (FIFO)
    counter = 1
    nodesDiscovered = 0
    #Store initial node distance and initial node as tuple in priority queue
    queue.put((distances[initial_node], counter, initial_node))

    while not queue.empty():
        
        #Get cheapest node
        current_node = queue.get()
        currentDistance = current_node[0]
        print("\nHighest distance: {}\n".format(currentDistance * -1))
        current_node = current_node[2] #Get the node, which is third element of tuple

        #Only use if node has not been discovered
        if current_node.isDiscovered or current_node in discoveredNodes:
            print("\n\nNode was already discovered.\n\n")
            continue
        else:
            current_node.isDiscovered = True
            #Replace node in grpah with current_node to update isDiscovered attribute
            # listOfEdges = graph.adjacency_list.pop(current_node)
            # graph.adjacency_list[current_node] = listOfEdges
            nodesDiscovered += 1
            discoveredNodes.append(current_node)

        print("\nCurrent Node: {}\n".format(current_node))
        print("\nNumber of nodes discovered: {}\n".format(nodesDiscovered))

        #Get neighbors of current_node from server
        neighbors = get_neighbors(current_node, discoveredNodes)

        # for n in neighbors:
        #     #Add node to graph
        #     graph.add_node(n)
        #     distance = get_distance(current_node, n)
        #     #Construct edge between neighbor and current_node and add to graph
        #     edge = gr.Edge(current_node, n, distance)
        #     graph.add_edge(edge)

        #Check neighbors inside graph
        for n in neighbors:           
            if not hasattr(n, 'isDiscovered'):
                n.isDiscovered = False

            #Node hasn't been added a distance yet
            if n not in distances:
                distances[n] = -sys.maxsize - 1

            # #Move to next neighbor if n is already discovered
            # if n.isDiscovered:
            #     print("\n\nNeighbor was already discovered.\n\n")
            #     continue

            print("\nNeighbor: {}\n".format(n))

            alt = distances[current_node] + get_distance(current_node, n)

            if alt > distances[n]:
                distances[n] = alt
                parents[n] = current_node

            #Increase counter
            counter = counter + 1
            queue.put((-1 * distances[n], counter, n)) #Multiply by -1 to get max value instead of min value for priority queue

            # if n == dest_node:
            #     print("\nDestination node is found!\n")
            #     queue.queue.clear()
            #     break

    #After queue is empty, shortest path for dest_node is stored by parents (updated each time a shorter path is found)
    print("\nQueue is empty!!!\n")
    while dest_node in parents:
        print("\nDestination node: {}\n".format(dest_node))
        actions.append(gr.Edge(parents[dest_node], dest_node, get_distance(parents[dest_node], dest_node)))
        dest_node = parents[dest_node]

    actions.reverse()
    return actions


def bfs(initial_node, dest_node):
    """
    Breadth First Search
    uses server to do search from the initial_node to dest_node
    returns a list of actions (edges) going from the initial node to dest_node
    """
    actions = []

    q = Queue()
    q.put(initial_node) #Put initial node in queue

    while not q.empty():
        
        current_node = q.get() #Dequeue 

        print("\nCurrent Node: {}\n".format(current_node))

        #Get neighbors of current_node:
        neighbors = get_neighbors(current_node, [])

        # for n in neighbors:
        #     #Add node to graph
        #     graph.add_node(n)
        #     #Construct edge between neighbor and current_node and add to graph
        #     edge = gr.Edge(current_node, n, get_distance(current_node, n))
        #     graph.add_edge(edge)

        for n in neighbors:
            
            print("\nNeighbor: {}\n".format(n))

            if not hasattr(n, 'parent'):
                n.parent = current_node

            if n == dest_node:
                endTile = n
                while hasattr(endTile, 'parent'):
                    #Get edge weight of two nodes
                    actions.append(gr.Edge(endTile.parent, endTile, get_distance(endTile.parent, endTile)))
                    endTile = endTile.parent;
                actions.reverse() #Reverse the order of the actions array
                return actions

            #Add to queue
            q.put(n)


if __name__ == "__main__":

    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')

    start_time = time.time()
    bfs_actions = bfs(gr.Node(empty_room), gr.Node(dark_room))
    bfs_time = time.time() - start_time

    start_time = time.time()
    dij_actions = dijkstra_search(gr.Node(empty_room), gr.Node(dark_room))
    dij_time = time.time() - start_time

    print("BFS: %.6f seconds" % (bfs_time))

    print("BFS Path:")
    for action in bfs_actions:
        print(get_edge_str(action))

    print("Dijkstra: %.6f seconds" % (dij_time))

    print("Dijkstra Path:")
    for action in dij_actions:
        print(get_edge_str(action))