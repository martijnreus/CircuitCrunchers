import matplotlib.pyplot as plt
import numpy as np

def histogram(cost_library, title):
    plt.title(title)
    plt.xlabel('cost')
    x = []
    for index in cost_library:
        x = cost_library[index]
    plt.hist(x)
    plt.savefig(f"./Visualization/histogram{title}")
    plt.show() 