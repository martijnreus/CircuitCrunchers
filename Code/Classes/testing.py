###################################################
# Testing algotithm, to test algorithms and order
#
# options: 
# 1. test all netlists/ only one specific
# 2. which algorithm to test
# 3. which sorting order
# 
# algorithms that are based on randomness will be 
# tested n times
###################################################

# import from libraries
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
    """
    Class for performing testing on algorithms and sorting orders.
    """

    # make empty lists and libraries
    def __init__(self, subject, algorithm, number_netlist, order_choice, order) -> None:
        """
        Initialize the Testing object.

        Args:
            subject (str): The subject of the testing (either "order" or "algorithm").
            algorithm (str): The algorithm to be tested.
            number_netlist (str): The number of the netlist to be tested.
            order_choice (str): The choice of sorting order for testing algorithms.
            order (str): The specific sorting order to be used (valid for algorithm testing).

        Preconditions:
            - subject must be either "order" or "algorithm".
            - algorithm must be a valid algorithm name.
            - number_netlist must be a valid netlist number.
            - order_choice must be a valid sorting order name.
            - order must be a valid sorting order name (applicable only for algorithm testing).

        """

        # initialize class variables to define test
        self.subject = subject
        self.algorithm = algorithm
        self.order_choice = order_choice
        self.order = order

        # get the info for the chip
        self.netlist = f"netlist_{int(number_netlist)}"
        self.chip_id = f"{get_number_chip(number_netlist)}"
        self.gates_file = f"print_{get_number_chip(number_netlist)}"

        # get title
        self.title = f"{subject}_{self.netlist}_{algorithm}_{order}"
        
        # initialize empty variables
        self.cost_list = []
        self.netlists = []
        self.variables = []

    # delete the current csv
    def delete_csv(self):
        """
        Delete the CSV file associated with the current testing.

        Postconditions:
            - The CSV file for the current testing is deleted if it exists.

        """
        filepath = f'output/{self.title}.csv'
        if not os.path.exists(filepath):
            pass
        else:
            os.remove(filepath)

    # output to csv
    def make_csv(self, filepath):
        """
        Create a new CSV file for writing test results.

        Args:
            filepath (str): The path of the CSV file.

        Preconditions:
            - The directory structure for the given filepath must exist.

        """
        with open(filepath, 'w', newline='') as newfile:
            writer = csv.writer(newfile, dialect='excel')
            writer.writerow(["test", "cost"])

    # get the filepath for the csv
    def get_filepath(self, title):
        """
        Get the file path for storing test results.

        Args:
            title (str): The title of the test.

        Returns:
            str: The file path for storing test results.

        """
        if self.subject == "order":
            filepath = f'output/{self.subject}/{title}'
        else:
            filepath = f'output/{self.subject}/{self.algorithm}/{title}'
        return filepath

    # write one line to csv
    def write_to_csv(self,title,info):
        """
        Write the test information to a CSV file.

        Args:
            title (str): The title of the test.
            info (list): The information to be written to the CSV file.

        Preconditions:
            - The directory structure for the given filepath must exist.
            - The CSV file with the given title must exist or be created.

        """
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
        Perform automated testing for different sorting orders.

        Args:
            algorithm (str): The algorithm to be tested.

        Preconditions:
            - algorithm must be a valid algorithm name.

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
        """
        Perform automated testing for the random order algorithm.

        Args:
            algorithm (str): The algorithm to be tested.
            n (int): The number of times the test should be run.

        Preconditions:
            - algorithm must be a valid algorithm name.
            - n must be a positive integer.

        """
        # loop to run the test n amount of times
        for number in range(n):

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
        """
        Perform automated testing for average cost of algorithms.

        Args:
            n (int): The number of times the test should be run.
            algorithm (str): The algorithm to be tested.

        Preconditions:
            - n must be a positive integer.
            - algorithm must be a valid algorithm name.

        """
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

    # test the hillclimber algorithms
    def hillclimber(self,n,algorithm):
        """
        Perform automated testing for hillclimber algorithm.

        Args:
            n (int): The number of times the test should be run.
            algorithm (str): The algorithm to be tested.

        Preconditions:
            - n must be a positive integer.
            - algorithm must be a valid algorithm name.

        """
        # for the hillclimber
        if algorithm == "hillclimber":

            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            hillclimber_algorithm(chip, n)
        
        # for the annealing
        elif algorithm == "annealing":

            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            # load everything
            chip.load_gates()
            chip.load_netlist()
            simulated_annealing(chip, n)

    # test the algorithms that always give the same answer
    def only_once(self,algorithm, order):
        """
        Perform automated testing for algorithms that give the same answer.

        Args:
            algorithm (str): The algorithm to be tested.
            order (str): The sorting order to be used.

        Preconditions:
            - algorithm must be a valid algorithm name.
            - order must be a valid sorting order name.

        """
        # if astar
        if algorithm == "astar":
            
            # define versions
            versions = ["optimal", "avoid_center", "avoid_gates", "avoid_both", "normal"]

            # run all versions
            for version in versions:

                # load new chip
                chip = Chip(self.chip_id, self.netlist, self.gates_file)
                chip.load_gates()
                chip.load_netlist()

                # run algorithm and calulate cost
                astar_algorithm(chip,version)
                cost = chip.calculate_cost()

                # print, visualize and produce output
                print(f"{version} cost: {cost}")
                info = [f"astar_algorithm_{version}_{order}", cost]
                self.write_to_csv(self.title, info)

        else:
            # load new chip
            chip = Chip(self.chip_id, self.netlist, self.gates_file)
            chip.load_gates()
            chip.load_netlist()

            # run algorithm and calulate cost
            choose_algorithm(algorithm, chip, order)
            cost = chip.calculate_cost()

            # print, visualize and produce output
            print(f"cost: {cost}")
            visualize(chip, self.title)
            info = [f"{algorithm}_algorithm_{order}", cost]
            self.write_to_csv(self.title, info)
  
# main test function
def test(subject, algorithm, number_netlist, order_choice, n):
    """
    Perform the main test based on the subject, algorithm, and options chosen.

    Args:
        subject (str): The subject of the test.
        algorithm (str): The algorithm to be tested.
        number_netlist (str): The number of the netlist to be tested.
        order_choice (str): The choice of sorting order.
        n (int): The number of times the test should be run.

    Preconditions:
        - subject must be a valid subject name.
        - algorithm must be a valid algorithm name.
        - number_netlist must be a valid netlist number.
        - order_choice must be a valid order choice.
        - n must be a positive integer.

    """
    order = "all"

    # input sorting order
    if algorithm in ["astar", "greedy", "hillclimber"] and subject == "algorithm":
        order = input("Sorting order: ")

        while order not in ["basic", "random", "reverse","long","least-connections","most-connections","sum-lowest","sum-highest","outside","intra-quadrant","manhattan", "short", "middle", "inter-quadrant","x","y","x-rev","y,rev", "weighted"]:
            order = input("Please choose one of the following orders: \nbasic, random, reverse, long, least-connections, most-connections, sum-lowest, sum-highest, outside, intra-quadrant, manhattan, short, middle, inter-quadrant, x, y, x-rev, y, rev, weighted\n")

    # choose if all netlists or just one
    if number_netlist == "all":

        netlists = ["1","2","3","4","5","6","7","8","9"]

        # for every netlist
        for number_netlist in netlists:

            # make new test object
            testing = Testing(subject, algorithm, number_netlist, order_choice, order)
            
            # delete old csv
            testing.delete_csv()

            # start testing
            print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
            choose_test(testing, n, order)

    # just one
    else:
        # make new test object
        testing = Testing(subject, algorithm, number_netlist, order_choice, order)
        
        # delete old csv
        testing.delete_csv()

        # start testing
        print(f"---chip: {testing.chip_id} and netlist: {number_netlist}-------------------")
        choose_test(testing, n, order)

# function to choose the test
def choose_test(testing, n, order):
    """
    Choose the appropriate test based on the algorithm and subject.

    Args:
        testing (Testing): The Testing object.
        n (int): The number of times the test should be run.
        order (str): The sorting order to be used.

    Preconditions:
        - testing must be a valid Testing object.
        - n must be a positive integer.
        - order must be a valid sorting order name.

    """
    # define algorithm
    algorithm = testing.algorithm

    # change order to random if order_choice is random
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

        # print info to find output
        print(f"\nFind output in output/{testing.subject}")
    
    # test algorithms
    else:

        # test the algorithms that dont give the same answer
        # random
        if algorithm == "random2D":
            testing.average(n,"random2D")

            # output histogram
            filepath = testing.get_filepath(testing.title) + ".csv"
            make_histogram(filepath, algorithm, n, order)

        # random2D
        elif algorithm == "random":
            testing.average(n,"random")

            # output histogram
            filepath = testing.get_filepath(testing.title) + ".csv"
            make_histogram(filepath, algorithm, n, order)
        
        # hillclimber
        elif algorithm == "hillclimber":
            testing.hillclimber(n,"hillclimber")

        # annealing
        elif algorithm == "annealing":
            testing.hillclimber(n,"annealing")

        # test the algorithms that do give the same answer
        # astar
        elif algorithm == "astar":
            testing.only_once("astar", order)

        # greedy
        elif algorithm == "greedy":
            testing.only_once("greedy", order)

        # else inform that function does not exist
        else:
            print("function not available")

        # print info for output
        print(f"Find output in output/{testing.subject}/{algorithm}")