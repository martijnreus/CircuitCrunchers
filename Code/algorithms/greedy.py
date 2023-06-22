###################################################
# 1st try of an algorithm:
# BASIC 
###################################################

import sys
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def greedy_algorithm(chip):
    """
    greedy algorithm, making the optimal choice for every stage.

    Args:
        wires (wires): the wire object 
        wire_connections (connections): the connections between the wires
    """

    # go over all the connections between two gates
    for connection in chip.wire_connections:

        # get gate indexes to get the appropriate wire
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire for the two gates
        wire = chip.wires[f"{gate_a}-{gate_b}"]

        # loop until we find are at the end location.
        while True:
            # get location of the current location and the end location
            location_a = wire.get_wire_part_start()
            location_b = wire.gateB.location

            # calculate distance between the locations
            distance = calculate_distance(location_a, location_b) 

            # if not yet on same x, go one step closer on the x axis.
            if distance.x != 0:

                # get direction as e.g.(1,0,0)
                direction = Location(check_sign(distance.x), 0, 0)
                wire.add_wire_part(direction)

            # if not yet on same y, go one step closer on the y axis.
            elif distance.y != 0:

                # get direction as e.g.(0,1,0)
                direction = Location(0, check_sign(distance.y), 0)
                wire.add_wire_part(direction)

            # if not yet on same z, go one step further
            elif distance.z != 0:
                # get direction as e.g.(0,0,1)
                direction = Location(0, 0, check_sign(distance.z))
                wire.add_wire_part(direction)

            # we are at the end location
            else:
                # wire.add_wire_part(direction)
                # print("connected!", wire.get_wire_length())
                break

def check_sign(number):
    """
    function to return the direction through the difference between the current and goal location.

    Args:
        number (int): distance between the x, y or z value of the two gates.

    Returns:
        int: the change needed to go one step close to the end location from the current location on the given axis.
    """
    if number > 0:
        return 1
    elif number < 0:
        return -1 
    else:
        return 0

def calculate_distance(location_a, location_b):
    """
    Function that returns the difference between the two locations for two given gates.

    Args:
        location_a (location): the location of the first gate
        location_b (location): the location of the second gate

    Returns:
        location difference: the difference in location between two gates.
    """
    x = location_b.x - location_a.x
    y = location_b.y - location_a.y
    z = location_b.z - location_a.z
    return Location(x, y, z)