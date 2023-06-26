#################################################################
# calls functions and methods from the other files
################################################################

# import
import sys
from sys import argv
sys.path.append("Classes")
from chip import *
from testing import *
sys.path.append("Visualization")
from plot import *
from graph import *
from bargraph import bargraph
sys.path.append("algorithms")
from greedy import *
from randomize import *
from randomize_twee_d import *
# from hillclimber_per_unit import *
from hillclimber import *
from astar import *
from order_sorting import *


def choose_algorithm(algorithm, chip, order_choice):
    """
    Function that selects the algorithm to use for our simulation.

    Args:
        algorithm (name): the name of the algorithm
        chip (chip): the chip of the current problem, with it's subparts
        order_choice (str): choice in order of connections made by algorithm.
    """
    chip.wire_connections = change_netlist_order(chip, order_choice)
    n = 10
    # if greedy is selected, run the greedy algorithm
    if algorithm == "greedy":
        greedy_algorithm(chip)
    
    # if algoritm is random, run the random algorithm
    elif algorithm == "random":
        random_algorithm(chip)
    
    elif algorithm == "random2D":
        random_twee_d(chip)
    
    # if algoritm is astar, run the astar algorithm
    elif algorithm == "astar":
        astar_algorithm(chip.wires, chip.wire_connections, chip.grid, chip.gates, "optimal")
    
    # if algoritzhm is hillclimber, run the hillclimber algorithm
    elif algorithm == "hillclimber":
        hillclimber_algorithm(chip)

def main():
    """
    main function, calling to 
    """
    # check for valid usage
    if len(argv) not in [1, 2, 3, 4, 5]:
        print("Usage: python main.py [number_chip] [number_netlist] [algorithm] [sorting_order]")
        print("sorting order cosists of: \"basic\", \"random\", \"short\", \"long\", \"most-connections\", \"least-connections\"")
        exit(1)

    if len(argv) == 2:
        if argv[1] == "ordertest":
            test("order")
        elif argv[1] == "algorithmtest":
            test("algorithms")
        elif argv[1] == "average_random":
            test("average_random")
        elif argv[1] == "average_random2D":
            test("average_random2D")
        elif argv[1] == "average_hillclimber":
            test("average_hillclimber")
        else:
            print("Usage: python main.py [number_chip] [number_netlist] [algorithm] [sorting_order]")

    else:
        # get all the necessary information.
        number_chip = 0
        number_netlist = 1
        number_gates_file = 0
        algorithm = "greedy"
        order_choice = "basic"

        # if we have a third argument, we should take that as our netlists.
        if len(argv) in [3, 4, 5]:
            number_chip = argv[1]
            number_netlist = argv[2]
            number_gates_file = argv[1]

            # if we have a fourth argument, then it specifies our algorithm
            if len(argv) in [4, 5]:
                algorithm = argv[3]

                # check for order argument
                if len(argv) == 5:
                    order_choice = argv[4]

        netlist = f"netlist_{number_netlist}"
        chip_id = f"{number_chip}"
        gates_file = f"print_{number_gates_file}"

        # make new chip
        chip = Chip(chip_id, netlist, gates_file)

        # load everything
        chip.load_gates()
        chip.load_netlist()

        # run algorithm and output
        choose_algorithm(algorithm, chip, order_choice)
        print("final:", chip.calculate_cost())
        visualize(chip.gate_list, chip.grid, chip.wires)
        
        chip.output_to_csv()

# def main():

#     # normal running of the code
#     if len[argv] == 1:
#         continue

#     # probably testing
#     if len[argv] == 2:

#         # we want to do testing
#         if argv[1] == "test":
#             netlist_number = input("What netlist do you want to test?")


#         else:
#             print("Usage: main.py test[optional]")
#             break


if __name__ == "__main__":
    main()