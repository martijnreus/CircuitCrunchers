#################################################################
# calls functions and methods from other files
################################################################

# import
import sys
from sys import argv
sys.path.append("Classes")
from chip import *
sys.path.append("Visualization")
from plot import *
sys.path.append("algorithms")
from greedy import *
from randomize import *
from hillclimber import *


def choose_algorithm(algorithm, chip):
    """
    Function that selects the algorithm to use for our simulation.

    Args:
        algorithm (name): the name of the algorithm
        chip (chip): the chip of the current problem, with it's subparts
    """
    # if greedy is selected, run the greedy algorithm
    if algorithm == "greedy":
        greedy_algorithm(chip.wires, chip.wire_connections)

    # if algoritm is random, run the random algorithm
    elif algorithm == "random":
        random_algorithm(chip.wires, chip.wire_connections, chip.grid, chip.gates)
    
    # if algoritzhm is hillclimber, run the hillclimber algorithm
    elif algorithm == "hillclimber":
        hillclimber_algorithm(chip.wires, chip.wire_connections, chip.grid, chip.gates, chip)


def main():
    """
    main function, calling to 
    """

    # check for valid usage
    if len(argv) not in [1,2,3,4]:
        print("Usage: python main.py [number_chip] [number_netlist]")
        exit(1)

    # get all the necessary information.
    number_chip = 0
    number_netlist = 1
    number_gates_file = 0
    algorithm = "greedy"

    if len(argv) == 2:
        algorithm = argv[1]

    # if we have a third argument, we should take that as our netlists.
    elif len(argv) in [3,4]:
        number_chip = argv[1]
        number_netlist = argv[2]
        number_gates_file = argv[1]

    # if we have a fourth argument, then it specifies our algorithm
    if len(argv) == 4:
        algorithm = argv[3]

    netlist = f"netlist_{number_netlist}"
    chip_id = f"{number_chip}"
    gates_file = f"print_{number_gates_file}"

    # make new chip
    chip = Chip(chip_id, netlist, gates_file)

    # load everything
    chip.load_gates()
    chip.load_netlist()

    # run algorithm and output
    choose_algorithm(algorithm, chip)
    visualize(chip.gate_list, chip.grid, chip.wires)
    print("final:", chip.calculate_cost())
    chip.output_to_csv()

if __name__ == "__main__":
    main()