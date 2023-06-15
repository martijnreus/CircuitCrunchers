###################################################
# Hill Climber's algorithm
###################################################
import sys
from randomize import random_add_wire
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def hillclimber_algorithm(wires: dict[object], wire_connections:list[str], grid: object, gates:list[object], chip:object):
    """
    Perform the hill climbing algorithm to optimize wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - The wire connections are optimized based on the hill climbing algorithm.
    """

    # initialize moving possibilities
    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    # for every wire
    for connection in wire_connections:

        # get gate a and gate b
        gate_a = connection[0]
        gate_b = connection[1]
        print(gate_a, gate_b)

        # get the associated wire
        wire = wires[f"{gate_a}-{gate_b}"]
        i = 0

        # make new random wire and save it and the total cost
        random_add_wire(possibilities, wire, grid, gates)
        old_wire = wire.wireparts
        old_cost = chip.calculate_cost()

        # repeat
        while True:

            new_cost = 0
            wire.wireparts = []

            # add random new wire and calculate new cost
            random_add_wire(possibilities, wire, grid, gates)
            new_cost = chip.calculate_cost()

            # if good move: new wire is now the old wire
            if new_cost < old_cost: 
                old_wire = wire.wireparts
                old_cost = new_cost

            # else if bad move, wire becomes old wire again
            else:
                wire.wireparts = old_wire

            i += 1

            # repeat this ... times
            if i == 500:
                print("connected")
                break
