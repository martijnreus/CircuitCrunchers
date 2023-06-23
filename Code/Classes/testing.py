import sys
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

class Test():

    def __init__(self) -> None:
        self.cost_list = []
        self.cost_library = {}
        
        self.netlists = []
        self.variables = []

    def make_bar_graph(self):
        print(self.cost_library)
        print(self.variables)
        bargraph(self.cost_library, self.variables)

    def make_graph(self):
        pass

    def get_netlists(self, number_chip):
        if number_chip == 0:
            self.netlists = [1, 2, 3]
        # elif number_chip == 1:
        #     self.netlists = [4, 5, 6]
        # elif number_chip == 2:
        #     self.netlists = [7, 8, 9]

        return self.netlists

    def testing_order(self,netlist, chip_id, gates_file, algorithm):
        """
        Automated testing
        """
        
        self.cost_library[f"{netlist}"]= []

        sorting_orders = ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant"]
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

    def testing_all_algorithms(self,netlist,chip_id,gates_file):

        algorithms = ["greedy", "random", "random2D","hillclimber","astar"]
        self.variables = algorithms
        self.cost_library[f"{netlist}"]= []

        for algorithm in algorithms:
            # make new chip
            chip = Chip(chip_id, netlist, gates_file)
            order_choice = "basic"
            
            # load everything
            chip.load_gates()
            chip.load_netlist()

            choose_algorithm(algorithm, chip, order_choice)
            cost = chip.calculate_cost()
            print(f"algorithm: {algorithm} || final score", cost)
            self.cost_list.append(cost)
    
    def average(self,netlist, chip_id, gates_file,n, algorithm):
        
        self.variables = list(range(n))
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
    number_chips = [0]
    test = Test()
    n = 100
    for number_chip in number_chips:
        netlists = test.get_netlists(number_chip)
        
        for number_netlist in netlists:
            netlist = f"netlist_{number_netlist}"
            chip_id = f"{number_chip}"
            gates_file = f"print_{number_chip}"
        	
            print(f"---chip: {chip_id} and netlist: {number_netlist}-------------------")
            
            if subject == "algorithms":
                test.testing_all_algorithms(netlist,chip_id,gates_file)
            
            elif subject == "order":
                algorithm = "astar"
                test.testing_order(netlist, chip_id, gates_file, algorithm)
                test.make_bar_graph()

            elif subject == "average_random2D":
                test.average(netlist, chip_id, gates_file,n,"random2D")
                test.make_bar_graph()
            
            elif subject == "average_random":
                test.average(netlist, chip_id, gates_file,n,"random")
                test.make_bar_graph()

            elif subject == "average_hillclimber":
                test.average(netlist, chip_id, gates_file,n,"hillclimber")
                test.make_bar_graph()