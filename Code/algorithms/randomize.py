import random
 
import sys
sys.path.append("../Classes")
from gate import *
from location import *

# main random algorithm
def random_algorithm(wires: dict[object], wire_connections: list[str], grid: object, gates: list[object]):
    """
    Perform a random algorithm to generate wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - Wire connections are randomly generated based on the algorithm.
    """

    # possibilities for moving
    possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    
    # get wire
    for connection in wire_connections:

        # get gates a and b
        gate_a = connection[0]
        gate_b = connection[1]
        print(gate_a, gate_b)
    
        # get wire
        wire = wires[f"{gate_a}-{gate_b}"]

        # add wire
        random_add_wire(possibilities, wire, grid, gates)
            
# add wire function
def random_add_wire(possibilities: list[(int,int,int)], wire: object, grid: object, gates: list[object]):
    """
    Add a randomly generated wire part to the given wire.

    Post-conditions:
        - A wire part is added to the wire based on a random direction.
        - If the wire becomes connected, the function terminates.
    """
    while True:

        # get random direction
        direction = random.choice(possibilities)
        location = Location(direction[0], direction[1], direction[2])

        # check if valid
        if check_if_valid(wire, grid, location, gates) == True:
            wire.add_wire_part(location)

        # check if connected
        if wire.check_is_connected() == True:
            break

# function to check if valid
def check_if_valid(wire:object, grid:object, direction, gates:list[object]):
    """
    Check if adding a wire part to the wire at the given direction is valid.

    Post-conditions:
        - Returns True if adding the wire part at the given direction is valid.
        - Returns False otherwise.
    """

    # check if there are any wireparts
    if wire.wireparts != []:
        current_wirepart = wire.wireparts[-1].to_location + direction
    else: 
        return True
    
    # check if wire direction goes out of grid
    if current_wirepart.x < 0 or current_wirepart.y < 0 or current_wirepart.z < -3:
        return False
    elif current_wirepart.x > grid.width or current_wirepart.y > grid.height or current_wirepart.z > 4:
        return False
    
    # check if wire goes through gate that is not gate b
    for gate in gates:
        if gates[gate] == wire.gateB:
            break
        if gates[gate].location == current_wirepart:
            return False
    
    # check if wire goes right back, repeating the move
    if current_wirepart == wire.wireparts[-1].from_location:
        return False
    return True