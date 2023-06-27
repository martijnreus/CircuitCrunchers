import sys
import csv
import os
from csv import writer
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
from plot import *

# Test algorithms and order
class Testing():

    # make empty lists and libraries
    def __init__(self, subject, algorithm, number_netlist, order_choice, order) -> None:
        
        self.subject = subject
        self.algorithm = algorithm
        self.netlist = f"netlist_{int(number_netlist)}"
        self.order_choice = order_choice
        self.order = order
        self.chip_id = f"{get_number_chip(number_netlist)}"
        self.gates_file = f"print_{get_number_chip(number_netlist)}"
        self.title = f"{subject}_{self.netlist}_{algorithm}_{order}"
        self.cost_list = []

        
        self.netlists = []
        self.variables = []

       
    def delete_csv(self):
        filepath = f'output/{self.title}.csv'
        if not os.path.exists(filepath):
            pass
        else:
            os.remove(filepath)

    # output to csv
    def make_csv(self, filepath):
        
        with open(filepath, 'w', newline='') as newfile:
            writer = csv.writer(newfile, dialect='excel')
            writer.writerow(["test", "cost"])

    def get_filepath(self, title):
        if self.subject == "order":
            filepath = f'output/{self.subject}/{title}'
        else:
            filepath = f'output/{self.subject}/{self.algorithm}/{title}'
        return filepath
    
    def write_to_csv(self,title,info):
        
        filepath = self.get_filepath(title) + ".csv"
        
        if not os.path.exists(filepath):
            self.make_csv(filepath)

        with open(filepath, 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(info)
        
            # Close the file object
            f_object.close()

    # test the orders for a netlist and algorithm
    def testing_order(self,algorithm):
        """
        Automated testing
        """

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
            info = [f"sort_{order_choice}_{algorithm}", cost]
            self.write_to_csv(self.title, info)  

    # get the average of the random order
    def testing_random_order(self, algorithm, n):
        
        # do n times
        for number in range(n):
            print(number)
            
            # make new chip
            chip = Chip(self.chip_id, self.netlist, self.gates_file)

            # load everything
            chip.load_gates()
            chip.load_netlist()
            
            # run the random algorithm and calculate the cost
            choose_algorithm(algorithm, chip, "random")
            cost = chip.calculate_cost()
            info = [f"random_try_{number}", cost]
            self.write_to_csv(self.title, info)

    # get the average of some algorithms
    def average(self,n, algorithm):
        
        self.variables = list(range(n))

        # for the random algorithm
        if algorithm == "random":
            for number in range(n): 
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random_algorithm(chip)
                cost = chip.calculate_cost()
                info = [f"random_try_{number}", cost]
                self.write_to_csv(self.title, info)
                
        
        # for the 2D random algorithm
        elif algorithm == "random2D":
            for number in range(n):
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()
                random2D(chip)
                cost = chip.calculate_cost()
                info = [f"random2D_try_{number}", cost]
                self.write_to_csv(self.title, info)

    def hillclimber(self,n,algorithm):    
        # for the hillclimber
        if algorithm == "hillclimber":

            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            cost_list = hillclimber_algorithm(chip, n)
            for cost in cost_list:
                info = ["better", cost]
                self.write_to_csv(f"hillclimber_costlist_{n}",info)
        
        # for the annealing
        elif algorithm == "annealing":
            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            cost_list= simulated_annealing(chip, n)
            for cost in cost_list:
                info = ["better", cost]
                self.write_to_csv(f"simulated_annealing_costlist_{n}",info)

    # test the algorithms that always give the same answer
    def only_once(self,algorithm, order):
        title = f"{algorithm}_{self.netlist}"
        
        if algorithm == "astar":
            versions = ["optimal", "avoid_center", "avoid_gates", "avoid_both", "normal"]
            for version in versions:
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                # load everything
                chip.load_gates()
                chip.load_netlist()

                astar_algorithm(chip,version)
                cost = chip.calculate_cost()
                print(f"{version} cost: {cost}")
                info = [f"astar_algorithm_{version}_{order}", cost]
                self.write_to_csv(self.title, info)
        else:
            # astar
            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            choose_algorithm(algorithm, chip, order)
            cost = chip.calculate_cost()
            print(f"cost: {cost}")
            visualize(chip, title)
            info = [f"{algorithm}_algorithm_{order}", cost]
            self.write_to_csv(self.title, info)


            
    # main test function
def test(subject, algorithm, number_netlist, order_choice, n):
    order = "all"
    if algorithm in ["astar", "greedy", "hillclimber"] and subject == "algorithm":
        order = input("Sorting order: ")
        while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
            order = input("Please choose one of the following orders: \nbasic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted\n")

    # choose if all netlists or just one
    if number_netlist == "all":
        netlists = ["1","2","3","4","5","6","7","8","9"]

        for number_netlist in netlists:
            # make new test object
            testing = Testing(subject, algorithm, number_netlist, order_choice, order)
            testing.delete_csv()
            print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
            choose_test(testing, n, order)
    
    # just one
    else:
        # make new test object
        testing = Testing(subject, algorithm, number_netlist, order_choice, order)
        testing.delete_csv()
        print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
        choose_test(testing, n, order)
        
# function to choose the test
def choose_test(testing, n, order):
    
    algorithm = testing.algorithm
    netlist = testing.netlist
    if testing.order_choice == "random":
        testing.order = "random" 

    # test order
    if testing.subject == "order":
        
        # test random order
        if testing.order_choice == "random":
            testing.testing_random_order(algorithm, n)

        # test all
        else:
            testing.testing_order(algorithm)
        print(f"\nFind output in output/{testing.subject}")
    # test algorithms
    else:
        # test the algorithms that dont give the same answer 
        if algorithm == "random2D":
            testing.average(n,"random2D")
            filepath = testing.get_filepath(testing.title) + ".csv"
            make_histogram(filepath, algorithm, n, order)

        elif algorithm == "random":
            testing.average(n,"random")
            print("here again")
            filepath = testing.get_filepath(testing.title) + ".csv"
            make_histogram(filepath, algorithm, n, order)

        elif algorithm == "hillclimber":
            testing.hillclimber(n,"hillclimber")
        
        elif algorithm == "annealing":
            testing.hillclimber(n,"annealing")

        # test the algorithms that do give the same answer
        elif algorithm == "astar":
            testing.only_once("astar", order)

        elif algorithm == "greedy":
            testing.only_once("greedy", order)

        else:
            print("function not available")

        print(f"Find output in output/{testing.subject}/{algorithm}")