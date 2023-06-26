import matplotlib.pyplot as plt



def bargraph(cost_library, variables):
    for netlist in cost_library:
        cost = []
        # print(netlist)
        plt.xlabel("x")
        plt.ylabel("cost")
        plt.title('Cost')

        cost = cost_library[netlist]
        # print(cost)
        plt.bar(variables,cost)
        plt.savefig(f"./Visualization/bargraph_{netlist}")
        # plt.show()