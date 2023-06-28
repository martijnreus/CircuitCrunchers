import matplotlib.pyplot as plt
from histogram import get_info
import numpy as np

def graph(x,cost_list, title):
        
    x = list(range(x))
    y = cost_list
    plt.plot(x,y)

    plt.ylabel('cost')
    plt.savefig(f"./Visualization/{title}")
    plt.show()

