import sys
from randomize import random_add_wire
sys.path.append("../Classes")
from gate import *
from location import *

# main random algorithm
def random2D(chip):
    """
    Perform a random algorithm to generate wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - Wire connections are randomly generated based on the algorithm.
    """

    # possibilities for moving
    possibilities = [[0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0]]
    
    # get wire
    for connection in chip.wire_connections:
        # get gates a and b
        gate_a = connection[0]
        gate_b = connection[1]
        # print(gate_a, gate_b)
    
        # get wire
        wire = chip.wires[f"{gate_a}-{gate_b}"]

        # add wire
        random_add_wire(possibilities, wire, chip)
 
