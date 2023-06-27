import matplotlib.pyplot as plt
import csv
import numpy as np



def make_histogram(filepath, algorithm, n, order):
    cost_list = get_info(filepath)
    title = f"{algorithm}_{n}times"
    histogram(cost_list, title, algorithm)

def get_info(filepath):    
    cost_list = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cost_list.append(int(row["cost"].strip()))
    return cost_list

def histogram(cost_list, title, algorithm):
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

def mean(x):
    total = 0
    n = 0
    for cost in x:
        total += cost
        n += 1
    return total / n

