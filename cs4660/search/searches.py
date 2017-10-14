"""
Searches module defines all different search algorithms
"""

from queue import Queue
from queue import PriorityQueue
from copy import deepcopy
import sys
sys.path.append('../')
from graph import graph as gr


def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    actions = []

    q = Queue()
    q.put(initial_node) #Put initial node in queue

    while not q.empty():
        
        current_node = q.get() #Dequeue 
        print("Current node: {}", current_node)

        #Get neighbors of intiial_node 
        neighbors = graph.neighbors(current_node)

        for n in neighbors:

            if not hasattr(n, 'parent'):
                n.parent = current_node

            if n == dest_node:
                endTile = deepcopy(n)
                while hasattr(endTile, 'parent'):
                    actions.append(gr.Edge(endTile.parent, endTile, graph.distance(endTile.parent, endTile)))
                    endTile = endTile.parent;
                actions.reverse() #Reverse the order of the actions array
                return actions

            #Add to queue
            q.put(n)

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    return dfs_current(graph, initial_node, dest_node, [])

def dfs_current(graph, current_node, dest_node, actions):
    
    #Get neighbors of current_node 
    neighbors = graph.neighbors(current_node)

    for n in neighbors:
        
        if hasattr(n, 'isDiscovered'):
            continue
        
        n.isDiscovered = True
        actions.append(gr.Edge(current_node, n, graph.distance(current_node, n)))

        if n == dest_node:
            return actions
        
        result = dfs_current(graph, n, dest_node, actions)

        #print("Result {}".format(result))

        #Child went through all neighbors or child contained dest_node from its children
        #If result is not empty, then dest_node is found from the child (Simply copies the result)
        #Else, the child went through all of its children and did not find dest_node, so get rid of that edge containing n
        #Move on to the next n
        if result:
            return result
        else:
            actions.pop()   

def dijkstra_search(graph, initial_node, dest_node):

    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    #Distance of each node
    #Parents of each node
    #Actions will be list of edges returned
    distances = {}
    parents = {}
    actions = []

    #Create priority queue
    queue = PriorityQueue()

    initial_node.isDiscovered = False

    #Set distance of initial_node to 0
    distances[initial_node] = 0

    #Create counter for priority queue in case there is a tie between distances of nodes, will get node that comes in first (FIFO)
    counter = 1
    #Store initial node distance and initial node as tuple in priority queue
    queue.put((distances[initial_node], counter, initial_node))

    while not queue.empty():
        
        #Get cheapest node
        current_node = queue.get()
        current_node = current_node[2] #Get the node, which is third element of tuple

        #Only use if node has not been discovered
        if current_node.isDiscovered:
            continue
        else:
            current_node.isDiscovered = True

        #Get neighbors of current_node
        neighbors = graph.neighbors(current_node)

        for n in neighbors:
            
            if not hasattr(n, 'isDiscovered'):
                n.isDiscovered = False

            #Node hasn't been added a distance yet
            if n not in distances:
                distances[n] = sys.maxsize

            #Move to next neighbor if n is already discovered
            if n.isDiscovered:
                continue

            alt = distances[current_node] + graph.distance(current_node, n)

            if alt < distances[n]:
                distances[n] = alt
                parents[n] = current_node

            #Increase counter
            counter = counter + 1
            queue.put((distances[n], counter, n))

    #After queue is empty, shortest path for dest_node is stored by parents (updated each time a shorter path is found)
    while dest_node in parents:
            actions.append(gr.Edge(parents[dest_node], dest_node, graph.distance(parents[dest_node], dest_node)))
            dest_node = parents[dest_node]

    actions.reverse()  
    #print("\nActions: \n{}\n".format(actions))  
    return actions

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    return []
