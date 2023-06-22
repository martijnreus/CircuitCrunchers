###################################################
# Hill Climber's algorithm
###################################################
import random
import sys
from randomize import check_if_valid
from greedy import calculate_distance, check_sign
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *
from chip import *



# class HillClimber:

    # def __init__(self):
    #     self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    # def get_random_direction(self):
    #     if self.possibilities:
    #         direction = random.choice(self.possibilities)
    #         index = self.possibilities.index(direction)
    #         direction = Location(direction[0], direction[1], direction[2])
    #         self.possibilities.pop(index)
    #         return direction
    
    # def reset(self):
    #     self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

def hillclimber_unit(chip):
    print("hello there")
    # for every connection
    for connection in chip.wire_connections:
        
        gate_a = connection[0]
        gate_b = connection[1]

        wire = chip.wires[f"{gate_a}-{gate_b}"]
        hillclimbing = HillClimber()
        print("New Wire", gate_a, gate_b)

        # repeat putting down small wireparts
        while True:
            # get location of the current location and the end location
            location_a = wire.get_wire_part_start()
            location_b = wire.gateB.location

            # Remember all the differences
            # calculate distance between the locations
            distance = calculate_distance(location_a, location_b) 

            # if not yet on same x, go one step closer on the x axis.
            if distance.x != 0:
                # get direction as e.g.(1,0,0)
                x_direction = Location(check_sign(distance.x), 0, 0)
                x_cost = chip.calculate_cost_wirepart(location_a, x_direction)
            # if not yet on same y, go one step closer on the y axis.
            if distance.y != 0:

                # get direction as e.g.(0,1,0)
                y_direction = Location(0, check_sign(distance.y), 0)
                y_cost = chip.calculate_cost_wirepart(location_a, y_direction)
            
            # if not yet on same z, go one step further
            if distance.z != 0:
                # get direction as e.g.(0,0,1)
                z_direction = Location(0, 0, check_sign(distance.z))
                z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
            
            if y_cost > z_cost and x_cost > z_cost:
                wire.add_wire_part(z_direction)
            if x_cost >= y_cost:
                wire.add_wire_part(y_direction)
            else:
                wire.add_wire_part(x_direction)











            # hillclimbing.reset()
            # # print("new wirepart")
            # # get starting location
            # start_location = wire.get_wire_part_start()

            # # get random direction
            # direction = hillclimbing.get_random_direction()
            # # print("got a random direction", direction)
            # # print("start location",start_location)

            # # if valid, add wire
            # if check_if_valid(wire, chip.grid, direction, chip.gates):
            #     # print("valid")
            #     print("add wire")
            #     old_cost = chip.calculate_cost_wirepart(start_location, direction)
            #     wire.add_wire_part(direction)
                
            # if wire.check_is_connected():
            #     print("connected")
            #     break

            # # check all possibilities if they are better
            # for possibility in range(5):
            #     # print(hillclimbing.possibilities)
            #     # print("in for loop")
            #     # get random direction
            #     new_direction = hillclimbing. get_random_direction()

            #     # if valid, check if expensive
            #     if check_if_valid(wire, chip.grid, direction, chip.gates):
            #         new_cost = chip.calculate_cost_wirepart(start_location, new_direction)
                    
            #         # if better, remove old and add new
            #         if old_cost > new_cost:
            #             print("better", old_cost, new_cost)
            #             # print(new_direction)
            #             wire.remove_wire_part()
            #             wire.add_wire_part(new_direction)
            #             old_cost = new_cost
            #         else: 
            #             print("worse")
            
           