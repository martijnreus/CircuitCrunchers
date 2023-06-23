import random
 
import sys
sys.path.append("../Classes")
from gate import *
from location import *

# main random algorithm
def random_algorithm(chip):
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
    for connection in chip.wire_connections:

        # get gates a and b
        gate_a = connection[0]
        gate_b = connection[1]
        # print(gate_a, gate_b)
    
        # get wire
        wire = chip.wires[f"{gate_a}-{gate_b}"]

        # add wire
        random_add_wire(possibilities, wire, chip)
            
# add wire function
def random_add_wire(possibilities: list[(int,int,int)], wire: object, chip: object):
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
        if check_if_valid(wire, chip, location) == True:
            wire.add_wire_part(location)

        # check if connected
        if wire.wireparts and wire.check_is_connected() == True:
            break

# function to check if valid
def check_if_valid(wire:object, chip:object, direction):
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
        current_wirepart = wire.gateA.location + direction
        
    # check if wire direction goes out of grid
    if current_wirepart.x < 0 or current_wirepart.y < 0 or current_wirepart.z < -3:
        # print("negative")
        return False
    elif current_wirepart.x > chip.grid.width or current_wirepart.y > chip.grid.height or current_wirepart.z > 4:
        # print("too high")
        return False
    
    # check if wire goes through gate that is not gate b
    for gate in chip.gates:
        if chip.gates[gate] == wire.gateB:
            break
        if chip.gates[gate].location == current_wirepart:
            # print("a gate in the way")
            return False
    
    # check if wire goes right back, repeating the move
    if wire.wireparts:
        if current_wirepart == wire.wireparts[-1].from_location:
            # print("going back")
            return False
    return True

def random_n_times(chip,n):
    total = 0
    for number in range(n):
        random_algorithm(chip)
        cost = chip.calculate_cost()
        total += cost
    return total / n
