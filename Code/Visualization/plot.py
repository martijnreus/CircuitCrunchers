import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys
sys.path.append("../Classes")
from gate import *
from location import *

def visualize(gates, grid):
    # Create gate points from the CSV file
    gate_points = gates

    # Extract x, y, and z coordinates from gate points
    x = [point.location.x for point in gate_points]
    y = [point.location.y for point in gate_points]
    z = [point.location.z for point in gate_points]

    # Create a 3D plot
    fig = plt.figure(figsize=(grid.width, grid.height))
    ax = fig.add_subplot(111, projection='3d')

    # lines
    # ax.plot([1, 6], [11, 11], [0, 0], linestyle='solid', linewidth=2,color = 'r')
    ax.plot([1, 6], [11, 11], [0, 0], linestyle='solid', linewidth=2,color = 'r')
    # Plot the gate points
    ax.scatter(x, y, z, c='b', marker='o')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gate Points')

    # Show the plot
    plt.show()
    plt.savefig("./Visualization/plot")