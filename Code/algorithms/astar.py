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
    
def a_star(wires, wire_connections):

    # go over all the connections between two gates
    for connection in wire_connections:

        # get gate indexes to get the appropriate wire
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire for the two gates
        wire = wires[f"{gate_a}-{gate_b}"]

        # reset alle path nodes
        # zorg ervoor dat alle path nodes met een kabel een cost van 300 extra krijgen 
        start_node = Node(None, wire.gateA.location)
        Debug.Log(start_node)


