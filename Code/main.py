#################################################################
# calls functions and methods from the other files
################################################################

# import
import sys
from sys import argv
sys.path.append("Classes")
from chip import *
sys.path.append("Visualization")
from plot import *
from graph import *
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
        return chip.calculate_cost()
    
    # if algoritm is random, run the random algorithm
    elif algorithm == "random":
        random_algorithm(chip)
        return chip.calculate_cost()
    
    elif algorithm == "average_random":
        return random_n_times(chip,n)
    
    elif algorithm == "random2D":
        random_twee_d(chip)
        return chip.calculate_cost()
    elif algorithm == "average_random2D":
        return average_random_twee_d(chip,n)


    # if algoritm is astar, run the astar algorithm
    elif algorithm == "astar":
        astar_algorithm(chip.wires, chip.wire_connections, chip.grid, chip.gates, "optimal")
        return chip.calculate_cost()
    
    # if algoritzhm is hillclimber, run the hillclimber algorithm
    elif algorithm == "hillclimber":
        hillclimber_algorithm(chip)
        return chip.calculate_cost()
    elif algorithm == "average_hillclimber":
        return hillclimber_n_times(chip, n)
        


def get_netlists(number_chip):
        if number_chip == 0:
            netlists = [1, 2, 3]
        # elif number_chip == 1:
        #     netlists = [4, 5, 6]
        # elif number_chip == 2:
        #     netlists = [7, 8, 9]

        return netlists

def testing_order(netlist, chip_id, gates_file, algorithm):
    """
    Automated testing
    """
    sorting_orders = ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant"]
    algorithm = algorithm
    
    for order_choice in sorting_orders:

        # make new chip
        chip = Chip(chip_id, netlist, gates_file)

        # load everything
        chip.load_gates()
        chip.load_netlist()
        
        choose_algorithm(algorithm, chip, order_choice)

        print(f"sort: {order_choice} || final score", chip.calculate_cost())
        

def testing_algorithms(netlist,chip_id,gates_file):
    algorithms = ["greedy","average_random", "average_random2D","average_hillclimber","astar"]
    cost_list = []
    for algorithm in algorithms:
        # make new chip
        chip = Chip(chip_id, netlist, gates_file)
        order_choice = "basic"
        
        # load everything
        chip.load_gates()
        chip.load_netlist()
        cost = choose_algorithm(algorithm, chip, order_choice)

        print(f"algorithm: {algorithm} || final score", cost)
        cost_list.append(cost)
    return cost_list
   
        
def test(subject):
    number_chips = [0, 1, 2]
    algorithm = "astar"
    for number_chip in number_chips:
        netlists = get_netlists(number_chip)
        
        for number_netlist in netlists:
            netlist = f"netlist_{number_netlist}"
            chip_id = f"{number_chip}"
            gates_file = f"print_{number_chip}"
        	
            print(f"---chip: {chip_id} and netlist: {number_netlist}-------------------")
            if subject == "algorithms":
                testing_algorithms(netlist,chip_id,gates_file)
            elif subject == "order":
                testing_order(netlist, chip_id, gates_file, algorithm)


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
        print("final:", choose_algorithm(algorithm, chip, order_choice))
        visualize(chip.gate_list, chip.grid, chip.wires)
        
        chip.output_to_csv()

if __name__ == "__main__":
    main()