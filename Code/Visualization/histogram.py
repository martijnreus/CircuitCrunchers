import matplotlib.pyplot as plt
import numpy as np

def histogram(cost_list, title):
    x = cost_list
    plt.title(title)
    plt.xlabel('cost')
    plt.axvline(mean(x), color='k', linestyle='dashed', linewidth=1)

    min_ylim, max_ylim = plt.ylim()
    plt.text(mean(x)*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean(x)))
    
    

    plt.hist(x, bins=30,color='c', alpha=0.65)
    plt.savefig(f"./Visualization/histogram_{title}")
    plt.show() 

def mean(x):
    total = 0
    n = 0
    for cost in x:
        total += cost
        n += 1
    return total / n