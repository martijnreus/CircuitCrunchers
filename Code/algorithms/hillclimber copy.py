###################################################
# Hill Climber's algorithm
###################################################
import random
import sys
from randomize import check_if_valid
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def hillclimber_algorithm(wires, wire_connections, grid, gates, chip):
    
    # Kies een random start state
    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]
        print(gate_a, gate_b)

        wire = wires[f"{gate_a}-{gate_b}"]

        while True:
        # Herhaal:
        # Doe een kleine random aanpassing
            old_cost = chip.calculate_cost()
            if wire.wireparts:
                old_distance = wire.gateB.location - wire.wireparts[-1].to_location
            else: 
                old_distance = wire.gateB.location - wire.gateA.location
            direction = random.choice(possibilities)
            location = Location(direction[0], direction[1], direction[2])
            if check_if_valid(wire, grid, location, gates):
                wire.add_wire_part(location)

            new_distance = wire.gateB.location - wire.wireparts[-1].to_location
            
            if old_distance <= new_distance:
                # print("bad move")
                wire.remove_wire_part()
            
            if chip.calculate_cost() > old_cost +1:
                # print("bad move")
                if check_if_other_valid_move(wire, grid, possibilities, gates):
                    wire.remove_wire_part()
            
            if wire.wireparts and wire.check_is_connected() == True:
                print("is connected")
                break

def check_if_other_valid_move(wire, grid, possibilities, gates):
    # get other possible options: 
    # current_wire_location = wire.wireparts[-1].to_location
    for direction in possibilities: 
        if check_if_valid(wire, grid, direction, gates):
            return True
    return False
