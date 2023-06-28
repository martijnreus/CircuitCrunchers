import random

def change_netlist_order(chip, order_choice):
    """
    Function calling the sorting functions chosen by the user.

    Returns:
        wire_connections : the sorted connections between the gates for this chip.
    """
    # set the reverse variable for opposite sorting methods using the same function
    reverse = True
    if order_choice in ["short", "least-connections", "sum-lowest", "middle", "intra-quadrant", "x", "y", "weighted"]:
        reverse = False

    if order_choice == "random":
        wire_connections = change_order_random(chip)

    elif order_choice == "reverse":
        wire_connections = change_order_reverse(chip)

    elif order_choice in ["short", "long"]:
        wire_connections = change_order_distance(chip, reverse=reverse)

    elif order_choice in ["least-connections", "most-connections"]:
        sum = False
        wire_connections = change_order_number_of_connections(chip, reverse=reverse, sum=sum)

    elif order_choice in ["sum-lowest", "sum-highest"]:
        sum = True
        wire_connections = change_order_number_of_connections(chip, reverse=reverse, sum=sum)

    elif order_choice in ["middle", "outside"]:
        wire_connections = change_order_middle_to_outside(chip, reverse=reverse)

    elif order_choice in ["intra-quadrant", "inter-quadrant"]:
        wire_connections = change_order_quadrant(chip, reverse=reverse)

    elif order_choice == "manhattan":
        wire_connections = change_order_manhattan(chip)

    elif order_choice in ["x", "x-rev"]:
        wire_connections = change_order_xy(chip, "x", reverse=reverse)

    elif order_choice in ["y", "y-rev"]:
        wire_connections = change_order_xy(chip, "y", reverse=reverse)

    elif order_choice in ["weighted", "weighted-rev"]:
        wire_connections = change_order_weighted_average(chip, reverse=reverse)

    # if none of these applied, just use the basic sorting (not sorting)
    else:
        wire_connections = chip.wire_connections

    return wire_connections


def change_order_random(chip):
    """
    Function that sorts the wire connections randomly.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """

    wire_connections = chip.wire_connections
    random.shuffle(wire_connections)

    return wire_connections


def change_order_reverse(chip):
    """
    Function that sorts the wire connections in reverse order.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.reverse()

    return wire_connections


def change_order_distance(chip, reverse):
    """
    Function that sorts the wire connections based on their inter gate distance.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.sort(key=lambda connection: calculate_distance(connection, chip), reverse=reverse)

    return wire_connections


def calculate_distance(connection, chip):
    """
    Function to calculate the distance between the two given gates for the connection.

    Args:
        connection (wire_connection): the connection between the two gates
        chip (chip): the current chip that we are working on

    Returns:
        distance: distance from gate a to gate b
    """

    # get the first gate's location
    gate_a_id = connection[0]
    gate_a = chip.gates[gate_a_id]
    a_location = gate_a.location

    # get the second gate's location
    gate_b_id = connection[1]
    gate_b = chip.gates[gate_b_id]
    b_location = gate_b.location

    # calculate the distance between the two gates
    distance = calculate_distance_between_points(a_location.x, a_location.y, b_location.x, b_location.y)

    return distance


def change_order_number_of_connections(chip, reverse, sum):
    """
    Function that sorts the wire connections based on the amount of connections one of the two (highest) gates has with other gates.
    In case reverse == False, it will sort from most to least connections, if reverse == True, the reverse is true.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Create a dictionary to store the connection count for each gate
    connection_count = {}

    # Count the connections for each gate
    for connection in wire_connections:
        gate_a_id, gate_b_id = connection

        # Count connections for gate A
        connection_count[gate_a_id] = connection_count.get(gate_a_id, 0) + 1

        # Count connections for gate B
        connection_count[gate_b_id] = connection_count.get(gate_b_id, 0) + 1

    if sum == False:

        # Sort wire_connections based on the number of connections for the gate with the most connections
        wire_connections.sort(key=lambda connection: max(connection_count[connection[0]], connection_count[connection[1]]), reverse=reverse)

    else:

        # Sort wire_connections based on the sum of connection counts for both gates in reverse order
        wire_connections.sort(key=lambda connection: connection_count[connection[0]] + connection_count[connection[1]], reverse=reverse)

    return wire_connections


def change_order_middle_to_outside(chip, reverse):
    """
    Function that sorts the wire connections based on their proximity to the middle of the chip,
    from closest to the middle to the most outside in case reverse is False, and from outside to the middle in case it is True.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    # get the connections
    wire_connections = chip.wire_connections

    # Calculate the coordinates of the middle of the chip
    middle_x = chip.grid.width / 2
    middle_y = chip.grid.height / 2

    # Sort wire_connections based on the distance from the middle to each gate involved in the connection
    wire_connections.sort(key=lambda connection: calculate_distance_to_specific_point(connection, chip, middle_x, middle_y), reverse=reverse)

    return wire_connections


def calculate_distance_to_specific_point(connection, chip, point_x, point_y):
    """
    Function to calculate the distance between a specific point of the chip and the gates involved in the wire connection.

    Args:
        connection (wire_connection): the connection between two gates
        chip (chip): the current chip that we are working on
        point_x (float): the x-coordinate of the point
        point_x (float): the y-coordinate of the point

    Returns:
        float: the distance from the point of the chip to the gates involved in the connection
    """
    gate_a_id, gate_b_id = connection

    gate_a = chip.gates[gate_a_id]
    gate_b = chip.gates[gate_b_id]

    distance_a = calculate_distance_between_points(gate_a.location.x, gate_a.location.y, point_x, point_y)
    distance_b = calculate_distance_between_points(gate_b.location.x, gate_b.location.y, point_x, point_y)

    return min(distance_a, distance_b)


def calculate_distance_between_points(x1, y1, x2, y2):
    """
    Function to calculate the distance between two points in a 2D space.

    Args:
        x1 (float): x-coordinate of the first point
        y1 (float): y-coordinate of the first point
        x2 (float): x-coordinate of the second point
        y2 (float): y-coordinate of the second point

    Returns:
        float: the distance between the two points
    """

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def change_order_quadrant(chip, reverse):
    """
    Function that sorts the wire connections by dividing the chip into quadrants and sorting connections within the same
    quadrant first, followed by connections between gates in different quadrants.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Divide the chip into quadrants based on the center point
    center_x = chip.grid.width / 2
    center_y = chip.grid.height / 2

    same_quadrant_connections = []
    different_quadrant_connections = []

    for connection in wire_connections:
        if is_same_quadrant(connection, chip, center_x, center_y):
            same_quadrant_connections.append(connection)
        else:
            different_quadrant_connections.append(connection)

    # Sort wire connections within the same quadrant by distance from shortest to longest
    same_quadrant_connections.sort(key=lambda connection: calculate_distance(connection, chip))

    # Sort wire connections between different quadrants by distance from shortest to longest
    different_quadrant_connections.sort(key=lambda connection: calculate_distance(connection, chip))

    return same_quadrant_connections + different_quadrant_connections


def is_same_quadrant(connection, chip, center_x, center_y):
    """
    Function to check if the gates in a connection belong to the same quadrant.

    Args:
        connection (wire_connection): the connection between two gates
        chip (chip): the current chip that we are working on
        center_x (float): the x-coordinate of the center point
        center_y (float): the y-coordinate of the center point

    Returns:
        bool: True if the gates are in the same quadrant, False otherwise
    """
    gate_a_id, gate_b_id = connection

    # Get the quadrant indices for the gates
    quadrant_a = get_quadrant_index(chip.gates[gate_a_id].location, center_x, center_y)
    quadrant_b = get_quadrant_index(chip.gates[gate_b_id].location, center_x, center_y)

    return quadrant_a == quadrant_b


def get_quadrant_index(location, center_x, center_y):
    """
    Function to determine the quadrant index for a given location based on the center point.

    Args:
        location (Location): the location of a gate
        center_x (float): the x-coordinate of the center point
        center_y (float): the y-coordinate of the center point

    Returns:
        int: the quadrant index (0, 1, 2, 3) based on the location
    """
    x = location.x
    y = location.y

    # Quadrant 1
    if x <= center_x and y <= center_y:
        return 0

    # Quadrant 2
    elif x > center_x and y <= center_y:
        return 1

    # Quadrant 3
    elif x <= center_x and y > center_y:
        return 2

    # Quadrant 4
    else:
        return 3


def change_order_manhattan(chip):
    """
    changes the order based on the manhattan distance, the difference between the x and y coordinates of the two gates

    Args:
        chip (object): the current chip

    Returns:
        _type_: _description_
    """
    wire_connections = chip.wire_connections

    sorted_connections = sorted(wire_connections, key=lambda connection: calculate_manhattan_distance(chip, connection))

    return sorted_connections


def calculate_manhattan_distance(chip, connection):
    """
    The calculation fo the manhattan distance.

    Args:
        chip (_type_): _description_
        connection (_type_): _description_

    Returns:
        manhattan_distance: the manhattan distance
    """
    # get the gate id's
    gate_a_id, gate_b_id = connection

    # get the gate objects
    gate_a = chip.gates[gate_a_id]
    gate_b = chip.gates[gate_b_id]

    # calculate the distances
    x_distance = abs(gate_a.location.x - gate_b.location.x)
    y_distance = abs(gate_a.location.y - gate_b.location.y)

    return x_distance + y_distance


def change_order_xy(chip, xy, reverse):
    """
    Function that sorts the wire connections based on the x-coordinate or y-coordinate of one of the two gates involved.

    Args:
        chip (chip): The current chip that we are working on.
        xy (str): The coordinate ('x' or 'y') to be used for sorting.
        reverse (bool): Whether to sort in reverse order or not.

    Returns:
        wire_connections (list): The sorted wire connections between the gates on this chip.
    """
    wire_connections = chip.wire_connections

    # Get the index (0 or 1) based on the given coordinate ('x' or 'y')
    gate_index = 0 if xy == 'x' else 1

    wire_connections.sort(key=lambda connection: chip.gates[connection[gate_index]].location.x if xy == 'x' else chip.gates[connection[gate_index]].location.y, reverse=reverse)

    return wire_connections


def change_order_weighted_average(chip, reverse):
    """
    Function to sort the wire connections based on their proximity to the weighted average coordinates.
    The weighted average in this case being a number as an average of all the gates on the chip, weighted by the connections for that gate.

    Args:
        chip (Chip): The current chip that we are working on.
        reverse (bool): If True, sort the connections in reverse order (farthest to nearest).

    Returns:
        wire_connections (list): The sorted wire connections based on proximity to the weighted average coordinates.
    """
    # get the weighted average gate point
    weighted_x, weighted_y = calculate_weighted_point(chip, reverse)

    wire_connections = chip.wire_connections

    wire_connections.sort(
        key=lambda connection: calculate_distance_to_specific_point(connection, chip, weighted_x, weighted_y),
        reverse=reverse
    )

    return wire_connections


def calculate_weighted_point(chip, reverse):
    """
    Function to calculate the weighted average coordinates.

    Args:
        chip (Chip): The current chip that we are working on.
        reverse (bool): If True, sort the connections in reverse order (farthest to nearest).

    Returns:
        x, y: the coordinate of the weighted average of all the gates.
    """

    wire_connections = chip.wire_connections

    # set the variables to 0
    weighted_x = 0
    weighted_y = 0

    total_connections = 0

    # go over all the gates on our chip
    for gate in chip.gates.values():

        # get the gate's x and y
        gate_x = gate.location.x
        gate_y = gate.location.y

        connections_per_gate = 0

        # go over all the connections and add a connnection count if it is for our current gate
        for connection in wire_connections:

            if connection[0] == gate.id_num or connection[1] == gate.id_num:
                connections_per_gate += 1

        # calculate the weight of this particular gate
        weighted_x += connections_per_gate * gate_x
        weighted_y += connections_per_gate * gate_y

        # add a global weight tracker (to devide with later)
        total_connections += connections_per_gate

    # calculate the weighted actual x and y coordinates
    true_x = weighted_x / total_connections
    true_y = weighted_y / total_connections

    return true_x, true_y
