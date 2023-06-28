###################################################
# initializes wire and wireunit class 
###################################################
# import from classes
from location import *

# created a wire between two gates
class Wire:
    """
    Represents a wire connecting two gates.

    Attributes:
        gateA (object): The starting gate of the wire.
        gateB (object): The ending gate of the wire.
        wireparts (list): List of wire parts connecting gateA to gateB.
    """
    def __init__(self, gateA: object, gateB: object)-> None:
        """
        Initialize a Wire object.

        Args:
            gateA (object): The starting gate of the wire.
            gateB (object): The ending gate of the wire.
        """
        self.gateA = gateA
        self.gateB = gateB
        self.wireparts = []

    def add_wire_part(self, direction: object)-> None:
        """
        Add a wire part to the wire.

        Args:
            direction (object): The direction of the wire part to be added.
        """
        self.wireparts.append(WireUnit(self.get_wire_part_start(),self.get_wire_part_end(direction)))

    def get_wire_part_start(self):
        """
        Get the starting location of a wire part.

        Returns:
            object: The starting location of the wire part.
        """
        # Add wire to gateA if there is no wire yet
        if (self.get_wire_length() == 0):
            return self.gateA.location
        # add wire to the last wire part if there is not
        else:
            return self.wireparts[self.get_wire_length() - 1].to_location

    def get_wire_part_end(self, direction):
        """
        Get the ending location of a wire part based on the direction.

        Args:
            direction (object): The direction of the wire part.

        Returns:
            object: The ending location of the wire part.
        """
        # add the direction to the begin_position
        to_x = self.get_wire_part_start().x + direction.x
        to_y = self.get_wire_part_start().y + direction.y
        to_z = self.get_wire_part_start().z + direction.z

        to_location = Location(to_x, to_y, to_z)
        return to_location

    def remove_wire_part(self)-> int:
        """
        Remove the last wire part from the wire.

        Returns:
            int: The removed wire part.
        """
        return self.wireparts.pop()

    def check_is_connected(self)-> bool:
        """
        Check if the wire is connected to gateB.

        Returns:
            bool: True if the wire is connected to gateB, False otherwise.
        """
        # checks if the location of the last wire matches the location of gateB
        if self.wireparts[len(self.wireparts) -1].to_location.x == self.gateB.location.x:
            if self.wireparts[len(self.wireparts)- 1].to_location.y == self.gateB.location.y:
                if self.wireparts[len(self.wireparts)- 1].to_location.z == self.gateB.location.z:
                    return True
        return False

    def get_wire_length(self)-> list[int]:
        """
        Get the length of the wire in terms of the number of wire parts.

        Returns:
            int: The length of the wire.
        """
        return len(self.wireparts)

    def clear_wire(self):
        """
        Clear the wire by removing all wire parts.
        """
        self.wireparts = []

# create a wireUnit, where its location of the start and end is tracked
class WireUnit:
    """
    Represents a single wire part connecting two locations.

    Attributes:
        from_location (object): The starting location of the wire part.
        to_location (object): The ending location of the wire part.
    """

    def __init__(self, from_location: object, to_location: object):
        """
        Initialize a WireUnit object.

        Args:
            from_location (object): The starting location of the wire part.
            to_location (object): The ending location of the wire part.
        """
        self.from_location = from_location
        self.to_location = to_location

    # if compared with each other, it compares where the cable lies 
    def __eq__(self, other):
        """
        Compare two WireUnit objects.

        Args:
            other (object): The other WireUnit object to compare.

        Returns:
            bool: True if the wire parts have the same ending location, False otherwise.
        """
        return self.to_location == other.to_location 
