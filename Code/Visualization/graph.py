###################################################
# make a graph from data 
###################################################
# import from libraries
import matplotlib.pyplot as plt
from histogram import get_info
import numpy as np

# make graph
def graph(x,cost_list, title):
    
    # data
    x = list(range(x))
    y = cost_list
    plt.plot(x,y)

    # ouput
    plt.ylabel('cost')
    plt.savefig(f"./Visualization/{title}")
    plt.show()

