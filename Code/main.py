#################################################################
# The gates and netlists from the files are being read in 
# and the objects are created
# and the output is being put out as an csv file
# having the right structure but not yet any input
################################################################

# import classes 
import csv
import sys
from sys import argv
sys.path.append("./Classes")
from gate import *
from wire import *
from grid import *
from location import *
sys.path.append("./Visualization")
from plot import *
sys.path.append("./algorithms")
from greedy import *

def main():
    pass

# class chip, as in which chip are we working on
class Chip():

    def __init__(self, chip: str, netlist: str, gates: str)-> None:
        # save chip and netlist file
        self.chip = chip
        self.netlist = netlist

        # save gates file
        self.gates_file = gates

        # remember the wires and gates
        self.wires = {}
        self.wire_connections = []
        self.gates = {}

        # list for visualisation
        self.gate_list = []

        # grid
        self.grid: object

    def load_netlist(self):
        csv_file = f"./../gates&netlists/chip_{self.chip}/{self.netlist}.csv"
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # get info from file

                gate_a_id = int(row["chip_a"])
                gate_b_id = int(row["chip_b"])
                gate_a = self.gates[gate_a_id]
                gate_b = self.gates[gate_b_id]

                # add connection
                self.wire_connections.append([gate_a_id, gate_b_id])
                
                # make new wire and add to wires
                new_wire = Wire(gate_a, gate_b)
                wire_key = f"{gate_a_id}-{gate_b_id}"
                self.wires[wire_key] = new_wire

    # load gates
    def load_gates(self)-> None:
        # put all possible x and y in list for grid
        x_list = []
        y_list = []
        csv_file = f"./../gates&netlists/chip_{self.chip}/{self.gates_file}.csv"
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:

                # get info from file 
                gate_id = int(row["chip"])
                x = int(row["x"])
                y = int(row["y"])
                z = 0

                # add to x and y list
                x_list.append(x)
                y_list.append(y)

                # make new location
                new_location = Location(x, y, z)

                # make new gate and add to gates 
                new_gate = Gate(gate_id, new_location)
                self.gates[gate_id] = new_gate
                self.gate_list.append(new_gate)

            # get max x and y
            max_x = max(x_list)
            max_y = max(y_list)

            # make grid
            self.grid = Grid(max_x +1, max_y +1, z)

    # output
    def output_to_csv(self)-> None:

        # open csv
        with open(f'output_{self.netlist}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')

            # write the first line
            writer.writerow(["net", "wires"])
            for connection in self.wire_connections:
                # gate a and b
                gate_ab = f"{connection[0]},{connection[1]}"
                gate_ab = gate_ab.strip()

                # list of wireparts
                list_of_wireparts = self.wires[f"{connection[0]}-{connection[1]}"].wires
                output_wireparts = []
                for wirepart in list_of_wireparts:
                    output_wireparts.append([wirepart.from_location.x,
                                            wirepart.from_location.y,
                                            wirepart.from_location.z])

                # write to csv
                writer.writerow([gate_ab.strip(),output_wireparts])

            # test total cost
            total_cost = self.calculate_cost()

            # write the last line
            writer.writerow([f"chip_{self.chip}_{self.netlist}", total_cost])
    
    # calculate cost
    def calculate_cost(self):

        # get number of wireparts
        n = 0
        for connection in self.wires:
            n +=self.wires[connection].get_wire_length()
        
        
        # hardcode k
        k = 5
        return n + 300 * k

# main
if __name__ == "__main__":

    # Check command line arguments
    if len(argv) not in [1,4]:
        print("Usage: python main.py [number_chip] [number_netlist] [number_gates_file]")
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
    chip.calculate_cost()
    chip.output_to_csv()