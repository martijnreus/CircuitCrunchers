###################################################
# Hill Climber's algorithm
###################################################
import sys
import math
import random
from randomize import random_add_wire
from greedy import greedy_algorithm
from astar import *
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *


class Hillclimber:
    def __init__(self, chip) -> None:
        self.wire: object
        self.chip = chip
        
        self.old_wire = []
        self.old_cost = 0
        self.new_cost = 0
        self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        self.cost_list = []
    
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
    
    def check_is_better(self):
        if self.new_cost <= self.old_cost: 
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
            self.cost_list.append(self.old_cost)
        else:
            self.wire.wireparts = self.old_wire
    
    def check_is_better_annealing(self, start_t, i):
        difference = self.old_cost - self.new_cost
        temperature = start_t*0.999999999**i
        accept = (2 ** difference)/temperature
        r = random.random()
        if r < accept:
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
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
    hillclimber = Hillclimber(chip)
    hillclimber.start_with_greedy()

    while True:
        random.shuffle(chip.wire_connections)
        
        for connection in chip.wire_connections:

            hillclimber.start_wire(connection)

            j = 0
            # repeat
            while True:
                
                hillclimber.make_new_wire()
                hillclimber.check_is_better()
                j += 1
                # repeat this ... times
                if j == 20:
                    # print("connected")
                    break
        i += 1
        # repeat this ... times
        if i == n:
            print("done")
            print(hillclimber.cost_list)
            break


def simulated_annealing(chip:object, n):
    i = 0
    hillclimber = Hillclimber(chip)
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
            print("done")
            break
