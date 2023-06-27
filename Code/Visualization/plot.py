import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
 
import sys
sys.path.append("../Classes")
from gate import *
from location import *

def visualize(chip, title):

    # GENERAL PLOT
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 10))
    # ax = plt.axes(projection='3d')
    
    ax = fig.add_subplot(111, projection='3d')
    ax.text2D(0.45, 0.95, f"cost: {chip.calculate_cost()}", transform=ax.transAxes)


    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"{title}")

    # GATES
    # Create gate points from the CSV file

    gate_points = chip.gate_list

    # Extract x, y, and z coordinates from gate points
    x = [point.location.x for point in gate_points]
    y = [point.location.y for point in gate_points]
    z = [point.location.z for point in gate_points]

    # Plot the gate points
    ax.scatter(x, y, z, c='b', marker='o')

    # PLATFORM IN THE MIDDLE
    # creating a range of width and height
    grid = chip.grid
    X = np.arange(grid.width+1)
    Y = np.arange(grid.height+1)
    ax.set_xticks(X)
    ax.set_xlim(0,grid.width +1)
    ax.set_yticks(Y)
    ax.set_ylim(0,grid.height +1)
    ax.set_zticks([-3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_zlim(-3, 4)
    # Creating a mesh grid of X and Y
    X, Y = np.meshgrid(X, Y)
    
    # set z to 0, because baseline 
    Z = X*0+Y*0
    ax.plot_wireframe(X, Y, Z, color='grey', alpha=0.5)

    # WIRES
    # lines
    for wire in chip.wires:
        for wirepart in chip.wires[wire].wireparts:
            ax.plot([wirepart.from_location.x, wirepart.to_location.x], 
                    [wirepart.from_location.y, wirepart.to_location.y], 
                    [wirepart.from_location.z, wirepart.to_location.z], 
                    linestyle='solid', linewidth=2,color = 'r')
            
    
    # Show the plot
    plt.show()
    plt.savefig(f"./Visualization/plots/3D_plot_{title}")