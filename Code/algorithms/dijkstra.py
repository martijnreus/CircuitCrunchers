###################################################
# Dijkstra's algorithm
###################################################

import sys
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

def dijkstralgorithm(wire, wire_connections, grid):

    # go over all the connections that we should make
    for connection in wire_connections:
        gate_a = connection[0]
        gate_b = connection[1]

        # get the wire name for the wire between gate a and b.
        wire = wires[f"{gate_a}-{gate_b}"]

        # get the starting location
        current_location = wire.get_wire_part_start()

        all_locations = grid.get_max_locations()
        max_x = all_locations[0]
        max_y = all_locations[1]
        max_z = all_locations[2]

        expensive_locations
        
        # loop over all
        while True:

            price_from_current_to_all = 0

            x = 0
            for x < max_x:

                # check if there is a wire on this location

                price_from_current_to_all
                lo


            # go over all the locations in the grid
            locations = 

            location.x
            location.y

            
