###################################################
# Hill Climber's algorithm
###################################################
import sys
from randomize import random_add_wire
from greedy import greedy_algorithm
from astar import *
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def hillclimber_algorithm(chip:object):
    """
    Perform the hill climbing algorithm to optimize wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - The wire connections are optimized based on the hill climbing algorithm.
    """
    greedy_algorithm(chip)
    # initialize moving possibilities
    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    # for every wire

    for connection in chip.wire_connections:

        # get gate a and gate b
        gate_a = connection[0]
        gate_b = connection[1]
        # print(gate_a, gate_b)

        # get the associated wire
        wire = chip.wires[f"{gate_a}-{gate_b}"]

        old_wire = wire.wireparts
        old_cost = chip.calculate_cost()

        j = 0
        # repeat
        while True:

            new_cost = 0
            wire.wireparts = []

            # add random new wire and calculate new cost
            random_add_wire(possibilities, wire, chip)
            new_cost = chip.calculate_cost()

            # if good move: new wire is now the old wire
            if new_cost <= old_cost: 
                old_wire = wire.wireparts
                old_cost = new_cost

            # else if bad move, wire becomes old wire again
            else:
                wire.wireparts = old_wire

            j += 1

            # repeat this ... times
            if j == 10000:
                print("connected")
                break

    
