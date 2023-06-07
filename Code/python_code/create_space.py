# import classes 
from gate import *
from wire import *
from grid import *
from location import *

def main():

    # test hardcoded for chip 0 and netlist_1
    netlist = "netlist_1"
    chip = "0"

    chip = Chip(chip, netlist)
    chip.load_netlist()

class Chip():

    def __init__(self, chip, netlist, gates):
        # save chip and netlist file
        self.chip = chip
        self.netlist = netlist

        # save gates file
        self.gates = gates

        # remember the wires
        self.wires = {}

    def load_netlist(self):
        # import data from files
        with open(f"../gates&netlists/chip{self.chip}/{self.netlist}.csv") as f:
            i = 0
            while True:

                netlist_info = f.readline()
                if netlist_info == "\n":
                    break

                # 
                netlist_info = netlist_info.split(",")
                gate_a = netlist_info[0]
                gate_b = netlist_info[1]
                new_wire = Wire(gate_a, gate_b)
                self.wires[i] = new_wire
                i = i + 1

    def load_gates(self):
        with open(f"../gates&netlists/chip{self.chip}/{self.gates}.csv") as f:
            i = 0


            gates_info = f.readline()
            if gates_info == "\n":
                break

            # get info from file 
            gates_info = gates_info.split(",")
            gate_id = gates_info[0]
            x = gates_info[1]
            y = gates_info[2]

            # add to gates 
            new_gate = Gate(gate_id, x, y)
            self.gates[i] = new_gate

            i = i + 1



if __name__ == "__main__":
    main()