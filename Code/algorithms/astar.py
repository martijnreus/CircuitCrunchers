import sys
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

class PathNode:
    
    def __init__(self, parent: object, location: object):

        self.parent = parent

        self.location = location

        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0

        self.has_cable = False

    def calculate_f_cost(self):
        self.f_cost = self.g_cost + self.f_cost
        self.add_wire_cost()
        return self.f_cost
    
    # add a extra cost of 300 if there is a wire on the node
    def add_wire_cost(self):
        if self.has_cable == True:
            f_cost += 300

    def __eq__(self, other):
        self.location == other.location
    
def astar_algorithm(wires, wire_connections, grid, gates):

    # go over all the connections between two gates
    for connection in wire_connections:

        # get gate indexes to get the appropriate wire
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire for the two gates
        wire = wires[f"{gate_a}-{gate_b}"]

        # reset alle path nodes
        # zorg ervoor dat alle path nodes met een kabel een cost van 300 extra krijgen 
        start_node = PathNode(None, wire.gateA.location)
        end_node = PathNode(None, wire.gateB.location)

        open_list = []
        close_list = []

        open_list.append(start_node)

        start_node.g_cost = 0
        start_node.h_cost = calculate_h_cost(start_node, end_node)
        start_node.calculate_f_cost()

        while(len(open_list) > 0):
            # always pick the node with the lowest f_cost
            current_node_index = get_lowest_f_node_index(open_list)
            current_node = open_list[current_node_index]

            # found a path
            if current_node == end_node:
                print("Path found")
                break

            # move the current node from the open list to the closed list
            open_list.pop(current_node_index)
            close_list.append(current_node)

            neighbour_nodes = []
            # add all the neighbour nodes of the current_node to the list
            add_neighbour_nodes(current_node, neighbour_nodes, grid)



# calculate the h_cost by walking to the end note over the grid
def calculate_h_cost(node, end_node):
    x_distance = abs(node.location.x - end_node.location.x)
    y_distance = abs(node.location.y - end_node.location.y)
    z_distance = abs(node.location.z - end_node.location.z)

    return x_distance + y_distance + z_distance

def get_lowest_f_node_index(node_list):
    lowest_f_node = node_list[0]
    index = 0
    for i in range(len(node_list)):
        if node_list[i].f_cost < lowest_f_node.f_cost:
            lowest_f_node = node_list[i]
            index = i
    return index

def add_neighbour_nodes(current_node, node_list, grid):
    # right
    if current_node.location.x > 0:
        node_position = Location(current_node.x + 1, current_node.y, current_node.z)
        node_list.append(PathNode(current_node, node_position))
    
    # left
    if current_node.location.x < grid.width:
        node_position = Location(current_node.x - 1, current_node.y, current_node.z)
        node_list.append(PathNode(current_node, node_position))

    # forward
    if current_node.location.y > 0:
        node_position = Location(current_node.x, current_node.y + 1, current_node.z)
        node_list.append(PathNode(current_node, node_position))
    
    # backward
    if current_node.location.x < grid.width:
        node_position = Location(current_node.x, current_node.y - 1, current_node.z)
        node_list.append(PathNode(current_node, node_position))

    #TODO add z 
