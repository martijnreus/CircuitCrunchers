###################################################
# initializes chip class 
###################################################
# import from libraries
import csv

# import from classes
from location import *
from gate import *
from wire import *
from grid import *

# class chip, as in which chip are we working on
class Chip():
    """
    Represents a chip and provides methods for manipulating and analyzing the chip.

    Methods:
        load_netlist(): Loads the connections from the netlist file.
        load_gates(): Loads the gates from the gates file.
        output_to_csv(): Outputs the chip information to a CSV file.
        calculate_cost(): Calculates the cost of the chip.
        calculate_collision_amount(): Calculates the number of wire collisions on the chip.
    """

    def __init__(self, chip_id: str, netlist: str, gates: str)-> None:
        """
        Initialize a Chip object with the given chip ID, netlist, and gates.

        Post-conditions:
            - Initializes a Chip object with the provided attributes:
            chip_id (str): The ID of the chip.
            netlist (str): The netlist file name.
            gates_file (str): The gates file name.
            wires(dict), wire_connections(list), gate_list(list) and gates(dict): empty, to be filled with methods
        """
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
        """
        Load the connections from the netlist file.

        Pre-conditions:
            - Assumes the netlist file exists and is in the correct format.

        Post-conditions:
            - Adds the wire connections to the `wire_connections` list.
            - Creates wire objects and adds them to the `wires` dictionary.
        """

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
        """
        Load the gates from the gates file.

        Pre-conditions:
            - Assumes the gates file exists and is in the correct format.

        Post-conditions:
            - Adds the gates to the `gates` dictionary.
            - Updates the `gate_list` attribute.
            - Creates the chip grid based on the maximum x and y values of the gates.
        """

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
    def output_to_csv(self) -> None:
        """
        Output the chip information to a CSV file.

        Pre-conditions:
            - Assumes the chip has been initialized and loaded with netlist and gates.

        Post-conditions:
            - Writes the chip information to a CSV file, including wire connections and their wire parts.
            - Calculates the total cost of the chip and includes it in the CSV file.
        """
        # Open CSV file
        with open('output/output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')

            # Write the header
            writer.writerow(["net", "wires"])

            for connection in self.wire_connections:
                # Gate a and b
                gate_ab = f"({int(connection[0])},{int(connection[1])})"
                gate_ab = gate_ab.strip()

                # List of wire parts
                list_of_wireparts = self.wires[f"{connection[0]}-{connection[1]}"].wireparts
                output_wireparts = []
                for wirepart in list_of_wireparts:
                    output_wireparts.append((int(wirepart.from_location.x),
                                            int(wirepart.from_location.y),
                                            int(wirepart.from_location.z)))

                # Add end location coordinates of the last wirepart
                if list_of_wireparts:
                    last_wirepart = list_of_wireparts[-1]
                    output_wireparts.append((int(last_wirepart.to_location.x),
                                            int(last_wirepart.to_location.y),
                                            int(last_wirepart.to_location.z)))

                # Write to CSV
                wireparts_str = ",".join([f"({x},{y},{z})" for x, y, z in output_wireparts])
                writer.writerow((gate_ab, "[" + wireparts_str + "]"))

            # Calculate total cost
            total_cost = self.calculate_cost()

            # Write the last line
            netlist_number = self.netlist.split("_")
            netlist_number = netlist_number[1]
            writer.writerow([f"chip_{int(self.chip_id)}_net_{int(netlist_number)}", f"{int(total_cost)}"])

    # calculate cost
    def calculate_cost(self):
        """
        Calculate the cost of the chip.

        Pre-conditions:
            - Assumes the chip has been initialized and loaded with netlist, gates, and wire connections.

        Post-conditions:
            - Calculates the cost of the chip based on the number of wireparts and collisions.
            - Returns the calculated cost.
        """

        # get number of wireparts
        n = 0
        k = self.calculate_collision_amount()
        n = sum(self.wires[connection].get_wire_length() for connection in self.wires)

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

                    if on_gate == False:
                        for connection in self.wires:
                            for wire_unit in self.wires[connection].wireparts:
                                if wire_unit.to_location == location:
                                    collisions += 1

                    if collisions > 1:
                        k += collisions - 1

        return k

