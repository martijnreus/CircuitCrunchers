#################################################################
# The gates and netlists from the files are being read in 
# and the objects are created
# and the output is being put out as an csv file
# having the right structure but not yet any input
################################################################

# import classes 
import csv
import sys
sys.path.append("../Classes")
from gate import *
from wire import *
from grid import *
from location import *

def main():
    pass

# class chip, as in which chip are we working on
class Chip():

    def __init__(self, chip, netlist, gates):
        # save chip and netlist file
        self.chip = chip
        self.netlist = netlist

        # save gates file
        self.gates_file = gates

        # remember the wires and gates
        self.wires = {}
        self.gates = {}

    # load connections between gates
    def load_netlist(self):
        # import data from files
        with open(f"../../gates&netlists/chip_{self.chip}/{self.netlist}.csv") as f:
            i = 0
            next(f)
            while True:
                
                netlist_info = f.readline()
                
                try:
                    print("##################### wire ", i)
                    print("netlist_info: ", netlist_info)
                    
                    # get info from file
                    netlist_info = netlist_info.split(",")
                    gate_a = netlist_info[0]
                    gate_b = netlist_info[1]

                    # make new wire and add to wires
                    new_wire = Wire(gate_a, gate_b)
                    print("wire: ", new_wire)
                    print("wire_a: ", new_wire.gateA)
                    print("wire_b: ", new_wire.gateB)
                    self.wires[i] = new_wire
                    i = i + 1
                except:
                    break

    # load gates
    def load_gates(self):
        with open(f"../../gates&netlists/chip_{self.chip}/{self.gates_file}.csv") as f:
            i = 0
            next(f)
            while True:
                gates_info = f.readline()

                try:
                    print("################## gate ", i)
                    print("gates info: ", gates_info)
                    
                    # get info from file 
                    gates_info = gates_info.split(",")
                    gate_id = gates_info[0]
                    x = gates_info[1].strip()
                    y = gates_info[2].strip()
                    z = 0

                    # make new location
                    new_location = Location(x, y, z)
                    print("location ", new_location)

                    # make new gate and add to gates 
                    new_gate = Gate(gate_id, new_location)
                    print("gate: ", new_gate)
                    print("gate id: ", new_gate.id_num)
                    print("gate_location: ", new_gate.location.x, new_gate.location.y, new_gate.location.z,)
                    self.gates[gate_id] = new_gate
                    i = i + 1
                except:
                    break
    
    # output
    def output_to_csv(self):

        # open csv
        with open(f'output_{self.netlist}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')

            # write the first line
            writer.writerow(["net", "wires"])

            i = 0
            while True:
                try:
                    # gate a and b
                    print("gate a", self.wires[i].gateA)
                    print("gate b", self.wires[i].gateB)
                    gate_ab = f"{self.wires[i].gateA},{self.wires[i].gateB}"
                    gate_ab = gate_ab.strip()
                    print(gate_ab)

                    # list of wireparts
                    list_of_wireparts = self.wires[i].wires
                    print(list_of_wireparts)

                    # write to csv
                    writer.writerow([gate_ab.strip(),list_of_wireparts])
                    i += 1
                except:
                    break

            # test total cost
            total_cost = 20

            # write the last line
            writer.writerow([f"chip_{self.chip}_{self.netlist}", total_cost])


# main
if __name__ == "__main__":

    # test hardcoded for chip 0 and netlist_1
    netlist = "netlist_1"
    chip = "0"
    gates_file = "print_0"
    print(gates_file)

    # make new chip 
    chip = Chip(chip, netlist, gates_file)
    print(chip.gates_file)

    # load everything
    chip.load_netlist()
    chip.load_gates()
    chip.output_to_csv()