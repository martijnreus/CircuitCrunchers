import random
 
import sys
sys.path.append("../Classes")
from gate import *
from location import *

def random_algorithm(wires, wire_connections, grid, gates):

    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    random.shuffle(wire_connections)
    # get gates
    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]
        print(gate_a, gate_b)

        wire = wires[f"{gate_a}-{gate_b}"]

            
        random_add_wire(possibilities, wire, grid, gates)
            

def random_add_wire(possibilities, wire, grid, gates):
    while True:
        direction = random.choice(possibilities)
        location = Location(direction[0], direction[1], direction[2])
        if check_if_valid(wire, grid, location, gates) == True:
            wire.add_wire_part(location)
        
        if wire.check_is_connected() == True:
            # print("is connected")
            break

def check_if_valid(wire, grid, direction, gates):

    if wire.wireparts != []:
        current_wirepart = wire.wireparts[-1].to_location + direction
    else: 
        # print("not yet any wireparts")
        return True
    if current_wirepart.x < 0 or current_wirepart.y < 0 or current_wirepart.z < -3:
        # print("out of the grid")
        return False
    elif current_wirepart.x > grid.width or current_wirepart.y > grid.height or current_wirepart.z > 4:
        # print("out of the grid")
        return False
    for gate in gates:
        if gates[gate] == wire.gateB:
            break
        if gates[gate].location == current_wirepart:
            return False
    if current_wirepart == wire.wireparts[-1].from_location:
        # print("already went there")
        return False
    return True