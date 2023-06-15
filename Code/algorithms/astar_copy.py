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

        self.has_wire = False

        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0

        self.extra_cost = 0

    def calculate_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost + self.extra_cost
        self.add_wire_cost()
        return self.f_cost
    
    # add a extra cost of 300 if there is a wire on the node
    def add_wire_cost(self):
        if self.has_wire == True:
            self.f_cost += 300

    # add extra f_cost to nodes that you might want to avoid
    def add_additional_f_cost(self, value):
        self.extra_cost += value

    def __eq__(self, other):
        return self.location == other.location
    
# create the global variables
wires = {}
grid = None
gates = {}
version = "normal"
    
def astar_algorithm(wires_input, wire_connections, grid_input, gates_input, version_input):
    global wires
    wires = wires_input

    global grid
    grid = grid_input

    global gates
    gates = gates_input

    global version
    version = version_input

    # go over all the connections between two gates
    for connection in wire_connections:

        # get gate indexes to get the appropriate wire
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire for the two gates
        wire = wires[f"{gate_a}-{gate_b}"]

        path = find_path(wire)

        make_wire(wire, path)

# put a wireUnit on each part of the path
def make_wire(wire, path):
    for i in range(0, len(path)):
        if i == 0:
            direction = path[i].location - wire.gateA.location
        else:
            direction = path[i].location - path[i - 1].location
        wire.add_wire_part(direction)

def find_path(wire):
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
            path = calculate_path(current_node)
            print(f"Path found: {len(path)}")
            return path

        # move the current node from the open list to the closed list
        open_list.pop(current_node_index)
        close_list.append(current_node)

        neighbour_nodes = []
        # add all the neighbour nodes of the current_node to the list
        add_neighbour_nodes(current_node, neighbour_nodes)

        for neighbour in neighbour_nodes:
            
            # the neighbour is already in the close list so we dont look at it again
            if (check_is_in_list(neighbour, close_list) == False):
                
                # if the neighbour is on a gate place in close list
                if (check_is_on_gate(neighbour, wire)):
                    close_list.append(neighbour)

                else:
                    # put the neighbour node in the open list if it is not in it yet
                    if (check_is_in_list(neighbour, open_list) == False):
                        neighbour.g_cost = neighbour.parent.g_cost + 1
                        neighbour.h_cost = calculate_h_cost(neighbour, end_node)

                        if check_is_on_wire(neighbour):
                            neighbour.has_wire = True

                        # Add extra cost depending on the mode the algoritm is in
                        if (version != "normal"):
                            pick_node_cost_version(neighbour, wire)

                        neighbour.calculate_f_cost()

                        open_list.append(neighbour)

    # no path has been found somehow
    return None

def calculate_path(end_node):
    path = []
    current_node = end_node
    while current_node.parent is not None:
        path.append(current_node)
        current_node = current_node.parent
    
    path.reverse()
    return path

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

def add_neighbour_nodes(current_node, node_list):
    # left
    if current_node.location.x > 0:
        node_position = Location(current_node.location.x - 1, current_node.location.y, current_node.location.z)
        node_list.append(PathNode(current_node, node_position))
    
    # right
    if current_node.location.x < grid.width:
        node_position = Location(current_node.location.x + 1, current_node.location.y, current_node.location.z)
        node_list.append(PathNode(current_node, node_position))

    # forward
    if current_node.location.y > 0:
        node_position = Location(current_node.location.x, current_node.location.y - 1, current_node.location.z)
        node_list.append(PathNode(current_node, node_position))
    
    # backward
    if current_node.location.y < grid.width:
        node_position = Location(current_node.location.x, current_node.location.y + 1, current_node.location.z)
        node_list.append(PathNode(current_node, node_position))

    # down
    if current_node.location.z > -3:
        node_position = Location(current_node.location.x, current_node.location.y, current_node.location.z - 1)
        node_list.append(PathNode(current_node, node_position))
    
    # up
    if current_node.location.z < 4:
        node_position = Location(current_node.location.x, current_node.location.y, current_node.location.z + 1)
        node_list.append(PathNode(current_node, node_position))

def check_is_on_gate(node, wire):
    # check if the location of the gate is on a node
    for gate in gates:
        # the location of gateB is allowed as this is the goal
        if gates[gate] == wire.gateB:
            break
        elif gates[gate].location == node.location:
            return True
    return False

def check_is_on_wire(node):
    for connection in wires:
        for wire_unit in wires[connection].wireparts:
            if node.location == wire_unit.from_location:
                return True
    return False

def check_is_in_list(node, list):
    for nodes in list:
        if node == nodes:
            return True
    return False

def pick_node_cost_version(node, wire):
    if (version == "avoid_gate"):
        for gate in gates:
            # the location of gateB is allowed as this is the goal
            if get_distance_to_gate(node, gates[gate], wire) <= 1:
                node.add_additional_f_cost(20)

def get_distance_to_gate(node, gate, wire):
    if gate.location == wire.gateB.location:
        return 99
    else:
        x_distance = abs(node.location.x - gate.location.x)
        y_distance = abs(node.location.y - gate.location.y)
        z_distance = abs(node.location.z - gate.location.z)

        return x_distance + y_distance + z_distance
