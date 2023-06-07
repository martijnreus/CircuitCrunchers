import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Classes.gate import gate as Gate
from Classes.location import location as Location

def create_gate_points_from_csv(csv_file):
    gate_points = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            chip = int(row['chip'])
            x = float(row['x'])
            y = float(row['y'])
            z = 0.0  # Default z coordinate
            location = Location(x, y, z, chip)
            gate = Gate(chip, location)
            gate_points.append(gate)
    return gate_points


def main(csv_file):
    # Create gate points from the CSV file
    gate_points = create_gate_points_from_csv(csv_file)

    # Extract x, y, and z coordinates from gate points
    x = [point.location.x for point in gate_points]
    y = [point.location.y for point in gate_points]
    z = [point.location.z for point in gate_points]

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the gate points
    ax.scatter(x, y, z, c='b', marker='o')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gate Points')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    chip_num = input("What chip do we want to create?")
    csv_file = "../../Code/gates&netlists/chip_" + chip_num + "/print_" + chip_num + ".csv"

    main(csv_file)