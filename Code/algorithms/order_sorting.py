import random
from math import sqrt


def change_netlist_order(chip, order_choice):
    """
    Function changing the order of the connections that have to be made by the algorithm.

    Returns:
        wire_connections : the sorted connections between the gates for this chip.
    """
    if order_choice == "random":
        wire_connections = change_order_random(chip)
        return wire_connections

    elif order_choice == "reverse":
        wire_connections = change_order_reverse(chip)
        return wire_connections

    elif order_choice == "short":
        wire_connections = change_order_shortest_first(chip)
        return wire_connections

    elif order_choice == "long":
        wire_connections = change_order_longest_first(chip)
        return wire_connections

    elif order_choice == "most-connections":
        wire_connections = change_order_most_connections(chip)
        return wire_connections

    elif order_choice == "least-connections":
        wire_connections = change_order_least_connections(chip)
        return wire_connections

    elif order_choice == "sum-lowest":
        wire_connections = change_order_sum_lowest(chip)
        return wire_connections

    elif order_choice == "sum-highest":
        wire_connections = change_order_sum_highest(chip)
        return wire_connections

    # if none of these applied, just use the basic sorting (not sorting)
    else:
        wire_connections = chip.wire_connections
        return wire_connections


def change_order_random(chip):
    """
    Function that sorts the wire connections randomly

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


def change_order_shortest_first(chip):
    """
    Function that sorts the wire connections from the shortest to longest distance between the two gates.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.sort(key=lambda connection: calculate_distance(connection, chip))

    return wire_connections


def calculate_distance(connection, chip):
    """
    function to calculate the distance between the two given gates for the wire connection

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

    distance = sqrt((a_location.x - b_location.x) ** 2 + (a_location.y - b_location.y) ** 2)

    return distance


def change_order_longest_first(chip):
    """
    Function that sorts the wire connections from the longest to shortest distance between the two gates.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.sort(key=lambda connection: calculate_distance(connection, chip), reverse=True)

    return wire_connections


def change_order_most_connections(chip):
    """
    Function that sorts the wire connections based on the amount of connections one of the two (highest) gates has with other gates.
    In this case from most to least connections.

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

    # Sort wire_connections based on the number of connections for the gates
    wire_connections.sort(key=lambda connection: max(connection_count[connection[0]], connection_count[connection[1]]), reverse=True)

    return wire_connections


def change_order_least_connections(chip):
    """
    Function that sorts the wire connections based on the amount of connections one of the two (highest) gates has with other gates.
    In this case from least to most connections.

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

    # Sort wire_connections based on the number of connections for the gates
    wire_connections.sort(key=lambda connection: min(connection_count[connection[0]], connection_count[connection[1]]))

    return wire_connections


def change_order_sum_highest(chip):
    """
    Function that sorts the wire connections based on the amount of connections both of the gates have combined.
    In this case from most to least connections.

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

    # Sort wire_connections based on the sum of connection counts for both gates in reverse order
    wire_connections.sort(key=lambda connection: connection_count[connection[0]] + connection_count[connection[1]], reverse=True)

    return wire_connections


def change_order_sum_lowest(chip):
    """
    Function that sorts the wire connections based on the amount of connections both of the gates have combined.
    In this case from least to most connections.

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

    # Sort wire_connections based on the sum of connection counts for both gates
    wire_connections.sort(key=lambda connection: connection_count[connection[0]] + connection_count[connection[1]])

    return wire_connections