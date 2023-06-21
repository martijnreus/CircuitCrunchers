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
from chip import *


class HillClimber:

    def __init__(self, wire):
        self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        self.wire = wire

    def get_wire(self):
        pass
    
    def get_random_direction(self):
        if self.possibilities:
            direction = random.choice(self.possibilities)
            index = self.possibilities.index(direction)
            direction = Location(direction[0], direction[1], direction[2])
            self.possibilities.pop(index)
            return direction

    
def hillclimber_unit(chip):
    # for every connection
    for connection in chip.wire_connections:
        
        gate_a = connection[0]
        gate_b = connection[1]

        wire = chip.wires[f"{gate_a}-{gate_b}"]
        hillclimbing = HillClimber(wire)
        print("WIREEEEEEEEEEEE################################", gate_a, gate_b)
        
        if not wire.wireparts:
            connected = False
        else:
            connected = wire.check_is_connected()

        # repeat putting down small wireparts
        while not connected:
            print("repaeating from start")
            # get starting location
            start_location = wire.get_wire_part_start()

            # get random direction
            direction = hillclimbing.get_random_direction()
            print("got a random direction", direction)

            # put them together
            print("start location",start_location)

            # if valid, add wire
            if check_if_valid(wire, chip.grid, direction, chip.gates):
                print("valid")
                print("add wire")
                wire.add_wire_part(direction)

            for possibility in hillclimbing.possibilities:
                print(hillclimbing.possibilities)
                print("in for loop")
                # get random direction
                new_direction = hillclimbing. get_random_direction()

                # if valid, check if expensive
                if check_if_valid(wire, chip.grid, direction, chip.gates):
                    old_cost = chip.calculate_cost_wirepart(start_location, direction)
                    new_cost = chip.calculate_cost_wirepart(start_location, new_direction)
                    
                    # if better, remove old and add new
                    if old_cost > new_cost:
                        print("better")
                        print(new_direction)
                        wire.remove_wire_part()
                        wire.add_wire_part(new_direction)
                    else: 
                        print("worse")