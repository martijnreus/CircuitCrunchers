import matplotlib.pyplot as plt

def graph(cost_library):
    for index in cost_library:
        plt.plot(cost_library[index])
    plt.ylabel('cost')
    plt.savefig("./Visualization/graph")
    plt.show()