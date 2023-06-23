import matplotlib.pyplot as plt

def graph(cost_list):
        
    fig = plt.figure(figsize=(10, 10))
    x = []
    y = []
    for index in range(len(cost_list)): 
        
        for number in range(2):
            x.append(number)
            y.append(cost_list[index])

        plt.plot(x, y)

    plt.ylabel('cost')
    plt.savefig("./Visualization/graph")
    plt.show()
