import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
 
import sys
sys.path.append("../Classes")
from gate import *
from location import *

def visualize(gates, grid, wires):
    # Create gate points from the CSV file
    gate_points = gates

    # Extract x, y, and z coordinates from gate points
    x = [point.location.x for point in gate_points]
    y = [point.location.y for point in gate_points]
    z = [point.location.z for point in gate_points]

    # Create a 3D plot
    fig = plt.figure(figsize=(grid.width, grid.height))
    ax = fig.add_subplot(111, projection='3d')

    # creating a range of width and height
    X = np.arange(grid.height +1)
    Y =X = np.arange(grid.width +1)
    
    # Creating a mesh grid of X and Y
    X, Y = np.meshgrid(X, Y)
    
    # set z to 0, because baseline 
    Z = X*0+Y*0
    ax.plot_wireframe(X, Y, Z, color='grey', alpha=0.5)

    # Plot the gate points
    ax.scatter(x, y, z, c='b', marker='o')

    # lines
    for wire in wires:
        for wirepart in wires[wire].wires:
            ax.plot([wirepart.from_location.x, wirepart.to_location.x], 
                    [wirepart.from_location.y, wirepart.to_location.y], 
                    [wirepart.from_location.z, wirepart.to_location.z], 
                    linestyle='solid', linewidth=2,color = 'r')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gate Points')

    # Show the plot
    plt.show()
    plt.savefig("./Visualization/plot")