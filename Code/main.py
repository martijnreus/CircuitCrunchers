#################################################################
# The gates and netlists from the files are being read in 
# and the objects are created
# and the output is being put out as an csv file
# having the right structure but not yet any input
################################################################

# import classes 
import csv
import sys
sys.path.append("./Classes")
from gate import *
from wire import *
from grid import *
from location import *
sys.path.append("./Visualization")
from plot import *
sys.path.append("./algorithms")
from basic import *

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

    # load connections between gates
    def load_netlist(self)-> None:

        # import data from files
        with open(f"./../gates&netlists/chip_{self.chip}/{self.netlist}.csv") as f:
            i = 0

            # go to second line
            next(f)

            while True:
                
                # read line per line
                netlist_info = f.readline()
                
                try:
                    # get info from file
                    netlist_info = netlist_info.split(",")
                    gate_a = int(netlist_info[0])
                    gate_b = int(netlist_info[1])

                    # add connection
                    self.wire_connections.append([gate_a, gate_b])

                    # make new wire and add to wires
                    new_wire = Wire(gate_a, gate_b)
                    wire_key = f"{gate_a}-{gate_b}"
                    self.wires[wire_key] = new_wire
                    i = i + 1
                except:
                    break

    # load gates
    def load_gates(self)-> None:

        # open csv
        with open(f"./../gates&netlists/chip_{self.chip}/{self.gates_file}.csv") as f:
            i = 0

            # go to second line
            next(f)

            # put all possible x and y in list for grid
            x_list = []
            y_list = []

            while True:

                # read line per line
                gates_info = f.readline()

                try:
                    # get info from file 
                    gates_info = gates_info.split(",")
                    gate_id = int(gates_info[0])
                    x = int(gates_info[1].strip())
                    y = int(gates_info[2].strip())
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
                    i = i + 1
                except:
                    break
            
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

            i = 0
            while True:
                try:
                    # gate a and b
                    gate_ab = f"{self.wires[i].gateA},{self.wires[i].gateB}"
                    gate_ab = gate_ab.strip()

                    # list of wireparts
                    list_of_wireparts = self.wires[i].wires

                    # write to csv
                    writer.writerow([gate_ab.strip(),list_of_wireparts])
                    i += 1
                except:
                    break

            # test total cost
            total_cost = "example"

            # write the last line
            writer.writerow([f"chip_{self.chip}_{self.netlist}", total_cost])


# main
if __name__ == "__main__":

    # test hardcoded for chip 0 and netlist_1
    netlist = "netlist_4"
    chip = "1"
    gates_file = "print_1"

    # make new chip 
    chip = Chip(chip, netlist, gates_file)

    # load everything
    chip.load_netlist()
    chip.load_gates()
    basic_algorithm(chip.wires, chip.wire_connections)
    visualize(chip.gate_list, chip.grid)
    chip.output_to_csv()