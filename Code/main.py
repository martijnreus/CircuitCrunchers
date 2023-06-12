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

def main():
    pass

# main
if __name__ == "__main__":

    # Check command line arguments
    if len(argv) not in [1,4]:
        print("Usage: python main.py [number_chip] [number_netlist] [number_print]")
        exit(1)

    # Load the requested chip or else example
    if len(argv) == 1:
        number_chip = 0
        number_netlist = 1
        number_gates_file = 0
    elif len(argv) == 4:
        number_chip = argv[1]
        number_netlist = argv[2]
        number_gates_file = argv[3]

    netlist = f"netlist_{number_netlist}"
    chip = f"{number_chip}"
    gates_file = f"print_{number_gates_file}"

    # make new chip 
    chip = Chip(chip, netlist, gates_file)

    # load everything
    chip.load_gates()
    chip.load_netlist()

    # run algorithm and output
    greedy_algorithm(chip.wires, chip.wire_connections)
    visualize(chip.gate_list, chip.grid, chip.wires)
    print("final:", chip.calculate_cost())
    chip.output_to_csv()