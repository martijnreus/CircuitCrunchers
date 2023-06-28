###################################################
# Hill Climber's algorithm
###################################################
import sys
import math
import random
import os
import csv
from randomize import random_add_wire
from greedy import greedy_algorithm
from astar import *
from csv import writer
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *
sys.path.append("../Visualization")
from graph import *
from histogram import *
class Hillclimber:
    def __init__(self, chip, subject, n) -> None:
        self.subject = subject
        self.wire: object
        self.chip = chip
        self.n = n
        
        self.old_wire = []
        self.old_cost = 0
        self.new_cost = 0
        self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        self.cost_list = []
        self.title = f"{chip.netlist}_{self.subject}_{n}"

    def start_wire(self, connection):
        # get gate a and gate b
        gate_a = connection[0]
        gate_b = connection[1]
        # print(gate_a, gate_b)

        # get the associated wire
        self.wire = self.chip.wires[f"{gate_a}-{gate_b}"]

        self.old_wire = self.wire.wireparts
        self.old_cost = self.chip.calculate_cost()

    def start_with_greedy(self):
        greedy_algorithm(self.chip)
    
    def start_with_astar(self, version):
        astar_algorithm(self.chip, version)
    
    def check_is_better(self, i):
        if self.new_cost <= self.old_cost: 
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
            self.cost_list.append(self.old_cost)
            self.write_to_csv()
            
        else:
            self.wire.wireparts = self.old_wire
    def make_graph(self):
        cost_list = get_info(self.filepath)
        x = list(range(len(cost_list)))
        graph(x,cost_list, self.title)
    # output to csv
    def make_csv(self, filepath):
        
        with open(filepath, 'w', newline='') as newfile:
            writer = csv.writer(newfile, dialect='excel')
            writer.writerow(["test", "cost"])

    def write_to_csv(self):
        filepath = f"output/algorithm/{self.subject}/{self.title}.csv"
        
        if not os.path.exists(filepath):
            self.make_csv(filepath)

        with open(filepath, 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(["new_cost: ",self.old_cost])
        
            # Close the file object
            f_object.close()

    def check_is_better_annealing(self, start_t, i):
        difference = self.old_cost - self.new_cost
        temperature = start_t*0.999999999**i
        accept = (2 ** difference)/temperature
        r = random.random()
        if r < accept:
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
            self.cost_list.append(self.old_cost)
            make_graph(i, self.old_cost, self.title + "annealing")
        else:
            self.wire.wireparts = self.old_wire
        
    def make_new_wire(self):
        self.new_cost = 0
        self.wire.wireparts = []
        # add random new wire and calculate new cost
        random_add_wire(self.possibilities, self.wire, self.chip)
        self.new_cost = self.chip.calculate_cost()


def hillclimber_algorithm(chip:object, n):
    """
    Perform the hill climbing algorithm to optimize wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - The wire connections are optimized based on the hill climbing algorithm.
    """
    # for every wire
    i = 0
    hillclimber = Hillclimber(chip, "hillclimber", n)
    hillclimber.start_with_greedy()

    while True:
        random.shuffle(chip.wire_connections)
        
        for connection in chip.wire_connections:

            hillclimber.start_wire(connection)

            j = 0
            # repeat
            while True:
                
                hillclimber.make_new_wire()
                hillclimber.check_is_better(i)
                j += 1
                # repeat this ... times
                if j == 20:
                    # print("connected")
                    break
        i += 1
        # repeat this ... times
        if i == n:
            break
    

def simulated_annealing(chip:object, n):
    i = 0
    hillclimber = Hillclimber(chip, "annealing", n)
    hillclimber.start_with_greedy()
    start_t = 1000
    while True:
        random.shuffle(chip.wire_connections)
        
        for connection in chip.wire_connections:

            hillclimber.start_wire(connection)

            j = 0
            # repeat
            while True:
                
                hillclimber.make_new_wire()
                hillclimber.check_is_better_annealing(start_t, i)
                j += 1
                # repeat this ... times
                if j == 2:
                    # print("connected")
                    break
        i += 1
        # repeat this ... times
        if i == n:
            break
    return hillclimber.cost_list