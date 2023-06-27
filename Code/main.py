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
        random_2D(chip)
    
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
def get_number_chip(netlist_number):
    if netlist_number in ["1","2","3"]:
        number_chip = 0

    elif netlist_number in ["4","5","6"]:
        number_chip = 1

    elif netlist_number in ["7","8","9"]:
        number_chip = 2
    
    return number_chip

def main2():

    # check for second argument
    if len(argv) in [1,3]:
        testing = False
        # we want to do testing
        if len(argv) == 3 and argv[1] == "test":
           
            testing = True
            if argv[2] not in ["order", "algorithm"]:
                print("Usage: main.py test[optional] testingtype[required in case of test]")
                sys.exit()
            else:
                testing_type = argv[2]

        # check the netlist we want to run/test
        netlist_number = input("Netlist: ")

        # if we are running normally, we may not give "all" as input.
        if len(argv) == 1 and netlist_number == "all":
            netlist_number = 0

        while netlist_number not in ["1","2","3","4","5","6","7","8","9", "all"]:
            netlist_number = input(f"Please specify your netlist number \n - options are: 1,2,3,4,5,6,7,8,9, all[only for testing purposes] \n")

            # if we are running normally, we may not give "all" as input.
            if len(argv) == 1 and netlist_number == "all":
                netlist_number = 0

        # check what algorithm we want to run and check for validity
        algorithm = input("Algorithm: ")

        while algorithm not in ["greedy", "hillclimber", "astar", "random", "random2D"]:
            algorithm = input(f"This algorithm is invalid, please specify one of the following \n - greedy, hillclimber, astar, random, random2D\n")

    # unclear what the user wants, quit the program
    else:
        print("Usage: main.py test[optional] testingtype")
        sys.exit()
    
    # if test
    if testing:

        if testing_type == "order":
            # ask if later we want to test the specified orders or the random ordering sort.
            order_choice = input("Test all orders or random order? ")
            while order_choice not in ["random", "all"]:
                order_choice = input("Please specify: \"orders\" or \"random\" ->")

            test("order", algorithm, netlist_number, order_choice)
            
        elif testing_type == "algorithm":
            order_choice = None
             # check what order we want to run / test
            order = input("Sorting order: ")
            while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
                order = input("Please choose one of the following orders: \nbasic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted\n")
            test("algorithm", algorithm, netlist_number, order_choice)

    # run the normal process
    else:
        get_number_chip(netlist_number)
        order = input("Sorting order: ")
        while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
            order = input("Please choose one of the following orders: \nbasic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted\n")
        test("order", algorithm, netlist_number)
            
        netlist = f"netlist_{netlist_number}"
        chip_id = f"{number_chip}"
        gates_file = f"print_{number_chip}"

        # make new chip
        chip = Chip(chip_id, netlist, gates_file)

        # load everything
        chip.load_gates()
        chip.load_netlist()

        # run algorithm and output
        choose_algorithm(algorithm, chip, order)
        print("final:", chip.calculate_cost())
        visualize(chip.gate_list, chip.grid, chip.wires)

        chip.output_to_csv()


if __name__ == "__main__":
    main2()