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

def hillclimber_algorithm(wires, wire_connections, grid, gates, chip):
    
    # Kies een random start state
    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    # for every wire
    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]
        print(gate_a, gate_b)

        wire = wires[f"{gate_a}-{gate_b}"]
        i = 0

        # make new random wire
        random_add_wire(possibilities, wire, grid, gates)
        old_wire = wire.wireparts
        old_cost = chip.calculate_cost()

        while True:

            new_cost = 0
            # add random new wire
            wire.wireparts = []
            random_add_wire(possibilities, wire, grid, gates)
            new_cost = chip.calculate_cost()
            # if good move: new wire is now the old wire
            if new_cost < old_cost: 
                # print("good move, new cost:", new_cost)
                old_wire = wire.wireparts
                old_cost = new_cost
            # else if bad move, wire becomes old wire again
            else:
                # print("bad move, old cost:", old_cost, new_cost)
                wire.wireparts = old_wire

            i += 1
            # do it  ... times
            if i == 500:
                print("connected")
                break
