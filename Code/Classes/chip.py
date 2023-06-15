import csv
from location import *
from gate import *
from wire import *
from grid import *

# class chip, as in which chip are we working on
class Chip():

    def __init__(self, chip_id: str, netlist: str, gates: str)-> None:
        # save chip and netlist file
        self.chip_id = chip_id
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

    # load connections
    def load_netlist(self):
        csv_file = f"./../gates&netlists/chip_{self.chip_id}/{self.netlist}.csv"
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
        csv_file = f"./../gates&netlists/chip_{self.chip_id}/{self.gates_file}.csv"

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
            self.grid = Grid(max_x +1, max_y +1, 7)

    # output
    def output_to_csv(self)-> None:
        """
        Output the chip information to a CSV file.

        Pre-conditions:
            - Assumes the chip has been initialized and loaded with netlist and gates.

        Post-conditions:
            - Writes the chip information to a CSV file, including wire connections and their wireparts.
            - Calculates the total cost of the chip and includes it in the CSV file.
        """
        # open csv
        with open('output/output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')

            # write the first line
            writer.writerow(["net","wires"])
            for connection in self.wire_connections:
                # gate a and b
                gate_ab = f"({int(connection[0])},{int(connection[1])})"
                gate_ab = gate_ab.strip()

                # list of wireparts
                list_of_wireparts = self.wires[f"{connection[0]}-{connection[1]}"].wireparts
                print(list_of_wireparts[0])
                output_wireparts = []
                for wirepart in list_of_wireparts:
                    output_wireparts.append((int(wirepart.from_location.x),
                                            int(wirepart.from_location.y),
                                            int(wirepart.from_location.z)))
                print(wirepart.from_location.x,wirepart.from_location.y)
                # write to csv
                writer.writerow((gate_ab,(output_wireparts)))

            # test total cost
            total_cost = self.calculate_cost()

            # write the last line
            netlist_number = self.netlist.split("_")
            netlist_number = netlist_number[1]
            writer.writerow([f"chip_{int(self.chip_id)}_net_{int(netlist_number)}", f"{int(total_cost)}"])
    
    # calculate cost
    def calculate_cost(self):

        # get number of wireparts
        n = 0
        k = self.calculate_collision_amount()

        for connection in self.wires:
            n += self.wires[connection].get_wire_length()
        
        cost = n + k * 300
        return cost
    
    def calculate_collision_amount(self):

        k = 0

        # loop over every location of the grid
        for x in range(0, self.grid.width):
            for y in range(0, self.grid.height):
                for z in range(0, self.grid.layers):
                    location = Location(x, y, z)
                    collisions = 0
                    on_gate = False

                    # check if the location is not on a gate
                    for gate_ids in self.gates:
                        if self.gates[gate_ids].location == location:
                            on_gate = True

                    if (on_gate == False):
                        for connection in self.wires:
                            for wire_unit in self.wires[connection].wireparts:
                                if wire_unit.to_location == location:
                                    collisions += 1

                    if collisions != 0:
                        k += collisions - 1

        return k

