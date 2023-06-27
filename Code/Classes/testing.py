import sys
import csv
import os
from datetime import datetime
from location import *
from gate import *
from wire import *
from grid import *
from chip import *
sys.path.append("..")
from main import *
sys.path.append("../algorithms")
from greedy import *
from randomize import *
from randomize_twee_d import *
from astar import *
sys.path.append("../Visualization")
from bargraph import *
from histogram import *

# Test algorithms and order
class Testing():

    # make empty lists and libraries
    def __init__(self, subject, algorithm, number_netlist, order_choice) -> None:
        
        self.subject = subject
        self.algorithm = algorithm
        self.netlist = f"netlist_{int(number_netlist)}"
        self.order_choice = order_choice
        self.chip_id = f"{get_number_chip(number_netlist)}"
        self.gates_file = f"print_{get_number_chip(number_netlist)}"

        self.cost_list = []
        self.cost_library = {}
        
        self.netlists = []
        self.variables = []

    # get the current time
    def get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H_%M")
        return current_time

    # output to csv
    def make_csv(self, title):
        time = self.get_time()
        filepath = f'output/{title}_{time}.csv'

        if not os.path.exists(filepath):
            # Create the file if it doesn't exist
            with open(filepath, 'w', newline='') as newfile:
                writer = csv.writer(newfile, dialect='excel')
                writer.writerow(["net", "cost"])

        with open(filepath, 'a', newline='') as csvfile:  
            writer = csv.writer(csvfile, dialect='excel')

            for index in self.cost_library:
                for cost in self.cost_library[index]:
                    writer.writerow([index, cost])
    
    def make_histogram(self, title):
        histogram(self.cost_library, title)

    # test the orders for a netlist and algorithm
    def testing_order(self,algorithm):
        """
        Automated testing
        """
        self.cost_library[f"{self.netlist}"]= []

        sorting_orders = ["basic","reverse", "short", "long","least-connections", "most-connections", "sum-lowest", "sum-highest", "middle", "outside", "intra-quadrant", "inter-quadrant", "manhattan","x","y","x-rev","y,rev", "weighted", "weighted-rev"]
        self.variables = sorting_orders
        
        # go through all the orders
        for order_choice in sorting_orders:

            # make new chip
            chip = Chip(self.chip_id, self.netlist, self.gates_file)

            # load everything
            chip.load_gates()
            chip.load_netlist()
            
            choose_algorithm(algorithm, chip, order_choice)
            cost = chip.calculate_cost()
            print(f"sort: {order_choice} || final score", cost)
            self.cost_library[f"{self.netlist}"].append(cost)
    
    # get the average of the random order
    def testing_random_order(self, algorithm, n):
        self.cost_library[f"{self.netlist}"]= []
        
        # do n times
        for number in range(n):
            
            # make new chip
            chip = Chip(self.chip_id, self.netlist, self.gates_file)

            # load everything
            chip.load_gates()
            chip.load_netlist()
            
            # run the random algorithm and calculate the cost
            choose_algorithm(algorithm, chip, "random")
            cost = chip.calculate_cost()
            self.cost_library[f"{self.netlist}"].append(cost)

    # get the average of some algorithms
    def average(self,n, algorithm):
        
        self.variables = list(range(n))
        self.cost_library = {}
        self.cost_library[f"{self.netlist}"]= []

        # for the random algorithm
        if algorithm == "random":
            for number in range(n):
                
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random_algorithm(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{self.netlist}"].append(cost)
        
        # for the 2D random algorithm
        elif algorithm == "random2D":
            for number in range(n):
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random2D(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{self.netlist}"].append(cost)
        
        # for the hillclimber
        elif algorithm == "hillclimber":
            for number in range(n):
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                hillclimber_algorithm(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{self.netlist}"].append(cost)

    # test the algorithms that always give the same answer
    def only_once(self,algorithm):
        self.cost_library[f"{self.netlist}"] = []
        
        # astar
        if algorithm == "astar":
            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            astar_algorithm(chip.wires, chip.wire_connections, chip.grid, chip.gates, "optimal")
            cost = chip.calculate_cost()
            self.cost_library[f"{self.netlist}"].append(cost)

        # greedy
        elif algorithm == "greedy":
            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            greedy_algorithm(chip)
            cost = chip.calculate_cost()
            self.cost_library[f"{self.netlist}"].append(cost)

# main test function
def test(subject, algorithm, number_netlist, order_choice, n):
    
    # choose if all netlists or just one
    if number_netlist == "all":
        netlists = ["1","2","3","4","5","6","7","8","9"]

        for number_netlist in netlists:
            # make new test object
            testing = Testing(subject, algorithm, number_netlist, order_choice)
            print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
            choose_test(testing, n)
    
    # just one
    else:
        # make new test object
        testing = Testing(subject, algorithm, number_netlist, order_choice)
        print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
        choose_test(testing, n)

# function to choose the test
def choose_test(testing, n):
    algorithm = testing.algorithm
    netlist = testing.netlist
    # test order
    if testing.subject == "order":
        
        # test random order
        if testing.order_choice == "random":
            testing.testing_random_order(algorithm, n)
            testing.make_csv(f"random_ordertest_{netlist}_{algorithm}")

        # test all
        else:
            testing.testing_order(algorithm)
            testing.make_csv(f"ordertest_{netlist}_{algorithm}")
    
    # test algorithms
    else:
        # test the algorithms that dont give the same answer 
        if algorithm == "random2D":
            testing.average(n,"random2D")
            testing.make_csv(f"average_{algorithm}_{netlist}_n_{n}")

        elif algorithm == "random":
            testing.average(n,"random")
            testing.make_csv(f"average_{algorithm}_{netlist}_n_{n}")
            testing.make_histogram(f"average_{algorithm}_{netlist}_n_{n}")

        elif algorithm == "hillclimber":
            testing.average(n,"hillclimber")
            testing.make_csv(f"average_{algorithm}_{netlist}_n_{n}")

        # test the algorithms that do give the same answer
        elif algorithm == "astar":
            testing.only_once("astar")
            testing.make_csv(f"{algorithm}_{netlist}")

        elif algorithm == "greedy":
            testing.only_once("greedy")
            testing.make_csv(f"{algorithm}_{netlist}")