###################################################
# make a histogram to show average distribution
###################################################
# import from libraries
import matplotlib.pyplot as plt
import csv

# make the histogram
def make_histogram(filepath, algorithm, n, order):
    """
    Generate a histogram based on the cost values stored in a CSV file.

    Args:
        filepath (str): The path to the CSV file.
        algorithm (str): The name of the algorithm.
        n (int): The number of times the algorithm was executed.
        order (str): The order used for the algorithm.
    """
    cost_list = get_info(filepath)
    title = f"{algorithm}_{n}times"
    histogram(cost_list, title, algorithm)

# get info from csv file
def get_info(filepath):   
    """
    Read the cost values from a CSV file and return them as a list.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        list: The cost values extracted from the CSV file.
    """ 
    cost_list = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cost_list.append(int(row["cost"].strip()))
    return cost_list

# make histogram
def histogram(cost_list, title, algorithm):
    """
    Generate a histogram based on the provided cost values.

    Args:
        cost_list (list): The list of cost values.
        title (str): The title for the histogram.
        algorithm (str): The name of the algorithm.

    Returns:
        None
    """
    x = cost_list
    plt.title(title)
    plt.xlabel('cost')

    plt.axvline(mean(x), color='k', linestyle='dashed', linewidth=1)

    min_ylim, max_ylim = plt.ylim()
    plt.text(mean(x)*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean(x)))
    filepath = f"./Visualization/histogram/{algorithm}/{title}"
    plt.hist(x, bins=30,color='c', alpha=0.65)
    plt.savefig(filepath)
    plt.show() 
    print(f"Find Histogram in Visualisation/histogram/{algorithm}")

# calculate mean
def mean(x):
    """
    Calculate the mean of a list of values.

    Args:
        x (list): The list of values.

    Returns:
        float: The mean of the values.
    """
    total = 0
    n = 0
    for cost in x:
        total += cost
        n += 1
    return total / n

