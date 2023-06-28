###################################################
# make a bar graph from data
###################################################
import matplotlib.pyplot as plt

# make bar graph
def bargraph(cost_library, variables):
    # for all netlists
    for netlist in cost_library:
        cost = []
        
        # label
        plt.xlabel("x")
        plt.ylabel("cost")
        plt.title('Cost')

        # make plot
        cost = cost_library[netlist]
        plt.bar(variables,cost)
        plt.savefig(f"./Visualization/bargraph_{netlist}")