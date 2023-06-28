#################################################################
# calls functions and methods from the other files
################################################################

# import from libraries
import sys
from sys import argv

# import classes
sys.path.append("Classes")
from chip import *
from testing import *

# import visualization
sys.path.append("Visualization")
from plot import *
from graph import *

# import algorithms
sys.path.append("algorithms")
from greedy import *
from randomize import *
from randomize_twee_d import *
from hillclimber import *
from astar import *
from order_sorting import *

# choose the algorithm
def choose_algorithm(algorithm, chip, order_choice):
    """
    Function that selects the algorithm to use for our simulation.

    Args:
        algorithm (name): the name of the algorithm
        chip (chip): the chip of the current problem, with it's subparts
        order_choice (str): choice in order of connections made by algorithm.
    """
    chip.wire_connections = change_netlist_order(chip, order_choice)
    # if greedy is selected, run the greedy algorithm
    if algorithm == "greedy":
        greedy_algorithm(chip)
    
    # if algoritm is random, run the random algorithm
    elif algorithm == "random":
        random_algorithm(chip)
    
    elif algorithm == "random2D":
        random2D(chip)
    
    # if algoritm is astar, run the astar algorithm
    elif algorithm == "astar":
        astar_algorithm(chip, "optimal")
    
    # if algoritzhm is hillclimber, run the hillclimber algorithm
    elif algorithm == "hillclimber":
        n = input("n: ")
        hillclimber_algorithm(chip, n)
    
    # if algoritzhm is hillclimber, run the hillclimber algorithm
    elif algorithm == "annealing":
        n = input("n: ")
        simulated_annealing(chip, n)

# get number of chip associated with netlist
def get_number_chip(netlist_number):
    if netlist_number in ["1","2","3"]:
        number_chip = 0

    elif netlist_number in ["4","5","6"]:
        number_chip = 1

    elif netlist_number in ["7","8","9"]:
        number_chip = 2
    
    return number_chip

# main
def main():
    # check for second argument
    if len(argv) in [1,3]:
        n = 0
        testing = False

        # in case we want to do testing
        if len(argv) == 3 and argv[1] == "test":
           
            testing = True

            # check if a valid test option was given
            if argv[2] not in ["order", "algorithm"]:
                print("Usage: main.py test[optional] testingtype[required in case of test]")
                sys.exit()

            # set the testing type
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
        while algorithm not in ["greedy", "hillclimber", "annealing","astar", "random", "random2D"]:
            algorithm = input(f"This algorithm is invalid, please specify one of the following \n - greedy, hillclimber, annealing, astar, random, random2D\n")
        
    # unclear what the user wants, quit the program
    else:
        print("Usage: main.py test[optional] testingtype[required in case of test]")
        sys.exit()
    
    # if testing we should run the following code
    if testing:

        # if we are testing algorithms with randomness, we should ask how many times we should run it (n)
        if algorithm in ["hillclimber","random", "random2D", "annealing"]:
            n = int(input("n: "))

        # 
        if testing_type == "order":
            # ask if later we want to test the specified orders or the random ordering sort.
            order_choice = input("Test all orders or random order? ")
            while order_choice not in ["random", "all"]:
                order_choice = input("Please specify: \"orders\" or \"random\" ->")
            if order_choice == "random":
                n = int(input("n: "))
            test("order", algorithm, netlist_number, order_choice, n)
            
        elif testing_type == "algorithm":
            order_choice = None
            # check what order we want to run / test
            test("algorithm", algorithm, netlist_number, order_choice, n)

    # run the normal process (not testing)
    else:
        number_chip=get_number_chip(netlist_number)
        netlist = f"netlist_{netlist_number}"
        chip_id = f"{number_chip}"
        gates_file = f"print_{number_chip}"

        # make new chip
        chip = Chip(chip_id, netlist, gates_file)

        # load everything
        chip.load_gates()
        chip.load_netlist()
        
        # choose version for astar
        if algorithm == "astar":
            version = input("Version: ")
            while version not in ["optimal", "avoid_center", "avoid_gates", "avoid_both", "normal"]:
                print("choose from optimal, avoid_center, avoid_gates, avoid_both, normal")
                version = input("Version: ")
                astar_algorithm(chip, version)

        # get sorting order
        order = input("Sorting order: ")
        while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
            order = input("Please choose one of the following orders: \nbasic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted\n")
        
        # run algorithm and output
        print(f"---chip: {number_chip} and netlist: {netlist_number}-------------------")    
        choose_algorithm(algorithm, chip, order)

        # visualize and output
        title = f"{algorithm}_{netlist}"
        visualize(chip, title)
        chip.output_to_csv()
        print("final cost: ", chip.calculate_cost())

# main
if __name__ == "__main__":
    main()