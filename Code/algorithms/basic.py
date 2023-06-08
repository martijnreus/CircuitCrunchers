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


def basic_algorithm( wires, wire_connections):

    # get gates
    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]

        wire = wires[f"{gate_a}-{gate_b}"]

        while True:
            # get location of gate a and b
            location_a = wire.get_wire_part_start()
            location_b = wire.gateB.location
            
            # calculate distance
            distance = calculate_distance(location_a, location_b) 
            
            # if not yet on same x, go one step further
            if distance.x != 0:

                # get direction as e.g.(1,0,0)
                direction = Location(check_sign(distance.x), 0, 0)
                
                # add wire
                wire.add_wire_part(direction)

            # if not yet on same y, go one step further
            elif distance.y != 0:

                # get direction as e.g.(0,1,0)
                direction = Location(check_sign(distance.y), 0, 0)
                
                # add wire
                wire.add_wire_part(direction)

            # if not yet on same z, go one step further
            elif distance.z != 0:
                
                # get direction as e.g.(0,0,1)
                direction = Location(check_sign(distance.z), 0, 0)
                
                # add wire
                wire.add_wire_part(direction)

            

def check_sign(number):
    if number > 0:
        return 1
    else:
        return -1 

def calculate_distance(location_a, location_b):
    x = location_b.x - location_a.x
    y = location_b.y - location_a.y
    z = location_b.z - location_a.z
    return Location(x, y, z)