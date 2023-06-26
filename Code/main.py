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

def main2():

    # check for second argument
    if len(argv) == 2:

        # we want to do testing
        if argv[1] == "test":

            # what type of test do we want
            testing_type = input("Do you want to do an order or algorithm test?")
            while testing_type not in ["order", "algorithm"]:
                testing_type = input("Please specify \"order\" or \"algorithm\".")

        # unclear what the user wants, quit the program
        else:
            print("Usage: main.py test[optional]")
            sys.exit()

    # get the input that we need to run / test
    if len(argv) in [1,2]:
        # check the netlist we want to run/test
        netlist_number = input("What netlist do you want to run?")

        # if we are running normally, we may not give "full" as input.
        if len(argv) == 2:
            if argv[1] == "test" and netlist_number == "all":
                print("changed netlist to 0")
                netlist_number = 0

        while netlist_number not in ["1","2","3","4","5","6","7","8","9", "all"]:
            netlist_number = input("Please specify your netlist number - options are: 1,2,3,4,5,6,7,8,9, full[only for testing purposes]")

            # if we are running normally, we may not give "full" as input.
            if len(argv) == 2:
                if argv[1] == "test" and netlist_number == "all":
                    print("changed netlist to 0")
                    netlist_number = 0

        # check what algorithm we want to run and check for validity
        algorithm = input("What algorithm do you want to use? ")

        while algorithm not in ["greedy", "hillclimber", "astar", "random", "random2D"]:
            algorithm = input("This algorithm is invalid, please specify one of the following - greedy, hillclimber, astar, random, random2D")

        # check what order we want to run / test
        order = input("What sorting order do you want to use? ")
        while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
            order = input("Please choose one of the following orders: basic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted")

        # run the testing
        if len(argv) == 2:
            if testing_type == "order":
                test("order", algorithm)

            elif testing_type == "algorithm":

                if algorithm == "random":
                    test("average_random", None)
            
                elif algorithm == "random2D":
                    test("average_random2D", None)

                elif algorithm == "hillclimber":
                    test("average_hillclimber", None)

                # moet nog gemaakt worden ----------------------------------------------------
                elif algorithm == "greedy":
                    test("greedy_once", None)
                elif algorithm == "astar":
                    test("astar_once", None)

        # run the normal process
        else:
            if netlist_number in ["1","2","3"]:
                number_chip = 0

            elif netlist_number in ["4","5","6"]:
                number_chip = 1

            elif netlist_number in ["7","8","9"]:
                number_chip = 2

            
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