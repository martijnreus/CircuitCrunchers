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

def unit_hillclimber_algorithm(wires, wire_connections, grid, gates, chip):

    for connection in wire_connections:
        
        gate_a = connection[0]
        gate_b = connection[1]
        print("WIREEEEEEEEEEEE################################", gate_a, gate_b)

        wire = wires[f"{gate_a}-{gate_b}"]
        print(wire.wireparts)
        print(wire.gateA.location)

        # for every wire_unit
        while True:
            if wire.wireparts:
                location = wire.wireparts[-1].to_location
            else:
                location = wire.gateA.location
            direction = 0
            best_direction = 0
            print("NEWWWW WIREEEEEUNITTTTT")
            possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
            # lay a random valid wire_unit
            direction = random.choice(possibilities)
            index = possibilities.index(direction)
            direction = Location(direction[0], direction[1], direction[2])
            print(possibilities)
            possibilities.pop(index)
            print(possibilities)

            # print(possibilities)
            while check_if_valid(wire, grid, direction, gates) == False:
                print("not valid")
                direction = random.choice(possibilities)
                index = possibilities.index(direction)
                direction = Location(direction[0], direction[1], direction[2])
                possibilities.pop(index)
                print(possibilities)

                print("first", best_direction)
            print("valid")
            best_direction = location + direction
            # stop when connected
            if wire.wireparts and wire.check_is_connected() == True:
                print("is connected")
                break


            # go through all possibilities of laying a wire
            while True:
                # print(possibilities)
                if len(possibilities) == 0:
                    print("tested all possibilities", possibilities)
                    break
                
                # get another random direction
                direction = random.choice(possibilities)
                index = possibilities.index(direction)
                direction = Location(direction[0], direction[1], direction[2])
                possibilities.pop(index)
                print(possibilities)

                
                # check if valid and less expensive and add wireunits
                if check_if_valid(wire, grid, direction, gates):
                    second_direction = location + direction
                    print("second is valid")

                    if chip.calculate_cost_wirepart(location, best_direction) < chip.calculate_cost_wirepart(location, second_direction):
                        best_direction = second_direction
                        print("is worse")
                else:
                    print("second not valid")
                print("second", second_direction)
                print("best", best_direction)
                new_location = location + best_direction
                wire.add_wire_part(new_location)
                print("added wire")
