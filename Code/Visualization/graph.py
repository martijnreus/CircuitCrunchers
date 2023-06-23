import matplotlib.pyplot as plt

def graph(cost_list):
        
    
    x = []
    y = []
    for index in range(len(cost_list)): 
        fig = plt.figure(figsize=(10, 10))
        for number in range(len(cost_list[index])):
            x.append(number)
            y.append(cost_list[index])

        plt.plot(x, y)

    plt.ylabel('cost')
    plt.savefig("./Visualization/graph")
    plt.show()
