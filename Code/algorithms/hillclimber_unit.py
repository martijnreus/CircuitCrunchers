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



def hillclimber_unit(chip):
    # get wire a and b with locations
    for connection in chip.wire_connections:
        print("new wire")
        gate_a = connection[0]
        gate_b = connection[1]

        wire = chip.wires[f"{gate_a}-{gate_b}"]

        
        while True:
            # calculate difference x y and z
            location_a = wire.get_wire_part_start()
            location_b = wire.gateB.location
            distance = calculate_distance(location_a, location_b) 
            print(distance)

            # lay down wire in x direction
            if distance.x != 0:
                x_direction = Location(check_sign(distance.x), 0, 0)
                x_cost = chip.calculate_cost_wirepart(location_a, x_direction)
                wire.add_wire_part(x_direction)

                # if y direction better, do that
                if distance.y != 0:
                    y_direction = Location(0, check_sign(distance.y), 0)
                    y_cost = chip.calculate_cost_wirepart(location_a, y_direction)
                    
                    if x_cost > y_cost:
                        wire.remove_wire_part()
                        wire.add_wire_part(y_direction) 
                    
                    # if z direction better, do that
                    if distance.z != 0:
                        z_direction = Location(0, 0, check_sign(distance.z))
                        z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
                        if  y_cost > z_cost and  x_cost > z_cost:
                            wire.remove_wire_part()
                            wire.add_wire_part(z_direction)    
                    else: 
                        z_direction = Location(0,0,1)
                        z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
                        if  y_cost > z_cost and  x_cost > z_cost:
                            wire.remove_wire_part()
                            wire.add_wire_part(z_direction)    
            
            
            #########################################################
            # continue with y
            elif distance.y != 0:
                # get direction as e.g.(0,1,0)
                y_direction = Location(0, check_sign(distance.y), 0)
                y_cost = chip.calculate_cost_wirepart(location_a, y_direction)
                wire.add_wire_part(y_direction)
                # if z direction better, do that
                if distance.z != 0:
                    z_direction = Location(0, 0, check_sign(distance.z))
                    z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
                    if  y_cost > z_cost:
                        wire.remove_wire_part()
                        wire.add_wire_part(z_direction)    
                else: 
                    z_direction = Location(0,0,1)
                    z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
                    if y_cost > z_cost:
                        wire.remove_wire_part()
                        wire.add_wire_part(z_direction) 
            
            # if not yet on same z, go one step further
            elif distance.z != 0:
                # get direction as e.g.(0,0,1)
                direction = Location(0, 0, check_sign(distance.z))
                wire.add_wire_part(direction)

            if wire.check_is_connected():
                break


    # if cost is lower in y direction lay down wire in y direction

    # if cost is lower in z direction, lay wire in z direction (if no z then z = 1)
    # repeat for every wirepart
    # stop if connected
    

# ###################################################
# # Hill Climber's algorithm
# ###################################################
# import random
# import sys
# from randomize import check_if_valid
# from greedy import calculate_distance, check_sign
# sys.path.append("../Classes")
# from gate import *
# from location import *
# from wire import *
# from grid import *
# from chip import *



# def hillclimber_unit(chip):
#     # get wire a and b with locations
#     for connection in chip.wire_connections:
#         print("new wire")
#         gate_a = connection[0]
#         gate_b = connection[1]

#         wire = chip.wires[f"{gate_a}-{gate_b}"]
#         while True:
#             # calculate difference x y and z
#             location_a = wire.get_wire_part_start()
#             location_b = wire.gateB.location
#             distance = calculate_distance(location_a, location_b) 
#             print(distance)

#             for difference in x_distance:
#                 x_direction = Location(check_sign(x_distance),0,0)
#                 chip.add_wire_part(x_direction)  
#                 x_cost = chip.calculate_cost_wirepart(location_a, x_direction)







#             # lay down wire in x direction
#             if distance.x != 0:
#                 x_direction = Location(check_sign(distance.x), 0, 0)
#                 x_cost = chip.calculate_cost_wirepart(location_a, x_direction)
#                 wire.add_wire_part(x_direction)

#                 # if y direction better, do that
#                 if distance.y != 0:
#                     y_direction = Location(0, check_sign(distance.y), 0)
#                     y_cost = chip.calculate_cost_wirepart(location_a, y_direction)
                    
#                     if x_cost > y_cost:
#                         wire.remove_wire_part()
#                         wire.add_wire_part(y_direction) 
                    
#                     # if z direction better, do that
#                     if distance.z != 0:
#                         z_direction = Location(0, 0, check_sign(distance.z))
#                         z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
#                         if  y_cost > z_cost and  x_cost > z_cost:
#                             wire.remove_wire_part()
#                             wire.add_wire_part(z_direction)    
#                     else: 
#                         z_direction = Location(0,0,1)
#                         z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
#                         if  y_cost > z_cost and  x_cost > z_cost:
#                             wire.remove_wire_part()
#                             wire.add_wire_part(z_direction)    
            
            
#             #########################################################
#             # continue with y
#             elif distance.y != 0:
#                 # get direction as e.g.(0,1,0)
#                 y_direction = Location(0, check_sign(distance.y), 0)
#                 y_cost = chip.calculate_cost_wirepart(location_a, y_direction)
#                 wire.add_wire_part(y_direction)
#                 # if z direction better, do that
#                 if distance.z != 0:
#                     z_direction = Location(0, 0, check_sign(distance.z))
#                     z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
#                     if  y_cost > z_cost:
#                         wire.remove_wire_part()
#                         wire.add_wire_part(z_direction)    
#                 else: 
#                     z_direction = Location(0,0,1)
#                     z_cost = chip.calculate_cost_wirepart(location_a, z_direction)
#                     if y_cost > z_cost:
#                         wire.remove_wire_part()
#                         wire.add_wire_part(z_direction) 
            
#             # if not yet on same z, go one step further
#             elif distance.z != 0:
#                 # get direction as e.g.(0,0,1)
#                 direction = Location(0, 0, check_sign(distance.z))
#                 wire.add_wire_part(direction)

#             if wire.check_is_connected():
#                 break


#     # if cost is lower in y direction lay down wire in y direction

#     # if cost is lower in z direction, lay wire in z direction (if no z then z = 1)
#     # repeat for every wirepart
#     # stop if connected
    
