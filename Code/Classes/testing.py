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
sys.path.append("../Visualization")
from bargraph import *

class Testing():

    def __init__(self) -> None:
        self.cost_list = []
        self.cost_library = {}
        
        self.netlists = []
        self.variables = []

    def get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H_%M")
        return current_time

    def make_csv(self, title):
        time = self.get_time()
        filepath = f'output/{title}_{time}.csv'

        if not os.path.exists(filepath):
            # Create the file if it doesn't exist
            with open(filepath, 'w', newline='') as newfile:
                writer = csv.writer(newfile, dialect='excel')
                writer.writerow(["net", "cost"])

        with open(filepath, 'a', newline='') as csvfile:  # Open in append mode
            writer = csv.writer(csvfile, dialect='excel')

            for index in self.cost_library:
                for cost in self.cost_library[index]:
                    writer.writerow([index, cost])

    def get_netlists(self, number_chip):
        if number_chip == 0:
            self.netlists = [1, 2, 3]
        elif number_chip == 1:
            self.netlists = [4, 5, 6]
        elif number_chip == 2:
            self.netlists = [7, 8, 9]

        return self.netlists

    def testing_order(self,netlist, chip_id, gates_file, algorithm):
        """
        Automated testing
        """
        self.cost_library[f"{netlist}"]= []

        sorting_orders = ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]
        self.variables = sorting_orders
        for order_choice in sorting_orders:

            # make new chip
            chip = Chip(chip_id, netlist, gates_file)

            # load everything
            chip.load_gates()
            chip.load_netlist()
            
            choose_algorithm(algorithm, chip, order_choice)
            cost = chip.calculate_cost()
            print(f"sort: {order_choice} || final score", cost)
            self.cost_library[f"{netlist}"].append(cost)
    
    def average(self,netlist, chip_id, gates_file,n, algorithm):
        
        self.variables = list(range(n))
        self.cost_library = {}
        self.cost_library[f"{netlist}"]= []

        if algorithm == "random":
            for number in range(n):
                
                chip = Chip(chip_id, netlist, gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random_algorithm(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{netlist}"].append(cost)
                print(f"algorithm: {algorithm} || score", cost)
        
        elif algorithm == "random2D":
            for number in range(n):
                chip = Chip(chip_id, netlist, gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random2D(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{netlist}"].append(cost)
                print(f"algorithm: {algorithm} || score", cost)
        
        elif algorithm == "hillclimber":
            for number in range(n):
                chip = Chip(chip_id, netlist, gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                hillclimber_algorithm(chip)
                cost = chip.calculate_cost()
                self.cost_library[f"{netlist}"].append(cost)
                print(f"algorithm: {algorithm} || score", cost)


def test(subject):
    number_chip = input("chip: ")
    number_chips = []
    if number_chip == "all":
        number_chips = [0, 1, 2]
    else:
        number_chips.append(int(number_chip))
    print(number_chips)
    testing = Testing()
    print(testing.get_time())
    n = 100
    print(subject)
    if subject == "order":
        algorithm = input("algorithm: ")
    for number_chip in number_chips:
        netlists = testing.get_netlists(number_chip)
        
        for number_netlist in netlists:
            netlist = f"netlist_{number_netlist}"
            chip_id = f"{number_chip}"
            gates_file = f"print_{number_chip}"
        	
            print(f"---chip: {chip_id} and netlist: {number_netlist}-------------------")
            
            if subject == "order":
                testing.testing_order(netlist, chip_id, gates_file, algorithm)
                testing.make_csv(f"ordertest_{netlist}_{algorithm}")

            elif subject == "average_random2D":
                testing.average(netlist, chip_id, gates_file,n,"random2D")
            
            elif subject == "average_random":
                testing.average(netlist, chip_id, gates_file,n,"random")
                testing.make_csv(f"average_random_{netlist}_n_{n}")

            elif subject == "average_hillclimber":
                testing.average(netlist, chip_id, gates_file,n,"hillclimber")
                testing.make_bar_graph()