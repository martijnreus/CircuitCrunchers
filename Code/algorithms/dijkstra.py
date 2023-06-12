###################################################
# Dijkstra's algorithm
###################################################

import sys
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def dijkstralgorithm(wire, wire_connections):

    # get gates
    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire name for the wire between gate a and b.
        wire = wires[f"{gate_a}-{gate_b}"]

        