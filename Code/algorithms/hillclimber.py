###################################################
# Hill Climber's algorithm with 
# add-on simulated annealing
###################################################
# import from libraries
import sys
import random
import os
import math
import csv

# import algorithms
from randomize import random_add_wire
from greedy import greedy_algorithm
from astar import *
from csv import writer

# import classes
sys.path.append("../Classes")
from gate import *
from location import *
from wire import *
from grid import *

# import visualization
sys.path.append("../Visualization")
from histogram import *

# class hillclimber
class Hillclimber:
    def __init__(self, chip, subject, n, order) -> None:
        """
        Initialize the Hillclimber object.
        """
        # get the hilclimber info
        self.subject = subject
        self.wire: object
        self.chip = chip
        self.n = n
        self.order = order
        
        # initialize empty class variables
        self.old_wire = []
        self.old_cost = 0
        self.new_cost = 0
        self.cost_list = []
        self.title = f"{chip.netlist}_{self.subject}_{n}_{self.order}"

        # initialize possibilities
        self.possibilities = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    # make new wire
    def start_wire(self, connection):
        """
        Set up the wire to be optimized.

        Args:
            connection (tuple): The gate connection associated with the wire.
        """
        # get gate a and gate b
        gate_a = connection[0]
        gate_b = connection[1]

        # get the associated wire
        self.wire = self.chip.wires[f"{gate_a}-{gate_b}"]
        
        # save wire and calculate cost
        self.old_wire = self.wire.wireparts
        self.old_cost = self.chip.calculate_cost()

    # make valid solution with greedy
    def start_with_greedy(self):
        """
        Start the optimization process with the greedy algorithm.
        """
        greedy_algorithm(self.chip)
    
    # make valid solution with astar
    def start_with_astar(self, version):
        """
        Start the optimization process with the A* algorithm.

        Args:
            version (str): The version of the A* algorithm to use.
        """
        astar_algorithm(self.chip, version)
    
    # check if change is better
    def check_is_better(self, i):
        """
        Check if the new cost is better than the old cost.

        Args:
            i (int): The index of the movement direction in the possibilities list.
        """

        # if cost is lower, make the change
        if self.new_cost <= self.old_cost: 
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
            self.cost_list.append(self.old_cost)
            self.write_to_csv()

        # else don't make the change  
        else:
            self.wire.wireparts = self.old_wire

    # check for simulated annealing
    def check_is_better_annealing(self, start_t, i, n):
        """
        Check if the new cost is better than the old cost based on the acceptance probability in simulated annealing.

        Args:
            start_t (float): The initial temperature for simulated annealing.
            i (int): The current iteration of the annealing process.
        """
        # calculate the accepting chance
        difference = self.old_cost - self.new_cost
        # temperature = start_t-(start_t/n)*i
        temperature = start_t*0.99999**i
        accept = 2**(difference / temperature)
        r = random.random()

        # if accepting, make change
        if r < accept:
            self.old_wire = self.wire.wireparts
            self.old_cost = self.new_cost
            print("accept:", self.new_cost)
            self.cost_list.append(self.old_cost)
            self.write_to_csv()

        # else don't make the change
        else:
            self.wire.wireparts = self.old_wire

    # create new wire and calculate cost 
    def make_new_wire(self):
        """
        Create a new wire for optimization and calculate its cost.
        """
        # set everything to 0
        self.new_cost = 0
        self.wire.wireparts = []

        # add random new wire and calculate new cost
        random_add_wire(self.possibilities, self.wire, self.chip)
        self.new_cost = self.chip.calculate_cost()
    
    # make a line graph
    def make_graph(self):
        """
        Generate a graph of the cost during optimization.
        """
        cost_list = get_info(self.filepath)
        x = list(range(len(cost_list)))
        graph(x,cost_list, self.title)
    
    # output to csv
    def make_csv(self, filepath):
        """
        Create a new CSV file.

        Args:
            filepath (str): The path of the CSV file to create.
        """
        with open(filepath, 'w', newline='') as newfile:
            writer = csv.writer(newfile, dialect='excel')
            writer.writerow(["test", "cost"])

    # write one line to the csv
    def write_to_csv(self):
        """
        Write the current cost to the CSV file.
        """
        filepath = f"output/algorithm/{self.subject}/{self.title}.csv"
        
        if not os.path.exists(filepath):
            self.make_csv(filepath)

        with open(filepath, 'a') as f_object:
            # Pass this file object to csv.writer() and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into the writerow()
            writer_object.writerow(["new_cost: ",self.old_cost])
        
            # Close the file object
            f_object.close()

# main hillclimber algorithm
def hillclimber_algorithm(chip:object, n, order):
    """
    Perform the hill climbing algorithm to optimize wire connections on a chip.

    Pre-conditions:
        - `wires` is a dictionary containing wire objects with unique keys representing wire connections.
        - `wire_connections` is a list of keys.

    Post-conditions:
        - The wire connections are optimized based on the hill climbing algorithm.
    """

    # make hillclimber object
    hillclimber = Hillclimber(chip, "hillclimber", n, order)

    # start with greedy algorithm
    hillclimber.start_with_greedy()

    # randomly get a wire and change it via the random algorithm
    for number in range(n):
        # shuffle connections
        random.shuffle(chip.wire_connections)
        
        # go through shuffled list
        for connection in chip.wire_connections:
            
            # make new wire
            hillclimber.start_wire(connection)

            # continue to make new wires and check if the cost is better
            for i in range(2):
                
                # make and check
                hillclimber.make_new_wire()
                hillclimber.check_is_better(i)

    
# simulated annealing add-on
def simulated_annealing(chip:object, n, order):
    """
    Perform the simulated annealing algorithm for optimizing wire connections in a chip.

    Args:
        chip (object): The chip object representing the circuit.
        n (int): The number of iterations for the annealing process.
    """
    # make hillclimber object
    i = 0
    hillclimber = Hillclimber(chip, "annealing", n, order)
    hillclimber.start_with_greedy()

    # define start
    start_t = 5

    # randomly get a wire and change it via the random algorithm
    for number in range(n):
        # shuffle connections
        random.shuffle(chip.wire_connections)
        
        # go through shuffled list
        for connection in chip.wire_connections:
            
            # make new wire
            hillclimber.start_wire(connection)

            # continue to make new wires and check if the cost is better
            for i in range(2):
                
                # make and check
                hillclimber.make_new_wire()
                hillclimber.check_is_better_annealing( start_t, number, n)

    