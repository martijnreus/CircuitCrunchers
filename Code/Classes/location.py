###################################################
# initializes Location class 
###################################################

# create a 3D space and keep track of all the locations in this space.
class Location:
    """
    Represents a 3D location in space.
    """
    def __init__(self, x: int, y: int, z: int):
        """
        Initialize a Location object.

        Args:
            x (int): The x-coordinate of the location.
            y (int): The y-coordinate of the location.
            z (int): The z-coordinate of the location.
        """
        self.x = x
        self.y = y
        self.z = z

    # defining "="
    def __eq__(self, other):
        """
        Compare two Location objects for equality.

        Args:
            other (object): The other Location object to compare.

        Returns:
            bool: True if the locations have the same coordinates, False otherwise.
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    # defining "+"
    def __add__(self, other):
        """
        Perform addition of two Location objects.

        Args:
            other (object): The other Location object to add.

        Returns:
            Location: A new Location object representing the sum of the coordinates.
        """
        return Location(self.x + other.x, self.y + other.y, self.z + other.z)

    # defining "-"
    def __sub__(self, other):
        """
        Perform subtraction of two Location objects.

        Args:
            other (object): The other Location object to subtract.

        Returns:
            Location: A new Location object representing the difference of the coordinates.
        """
        return Location(self.x - other.x, self.y - other.y, self.z - other.z)

    # defining representation
    def __repr__(self) -> str:
        """
        Get the string representation of the Location object.

        Returns:
            str: The string representation of the Location object.
        """
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    # defining ">"
    def __ge__(self, other):
        """
        Compare if the current Location is greater than or equal to the other Location.

        Args:
            other (object): The other Location object to compare.

        Returns:
            bool: True if the current Location is greater than the other Location, False otherwise.
        """
        return self.x > other.x or self.y > other.y or self.z > other.z

    # defining "<"
    def __le__(self, other):
        """
        Compare if the current Location is less than or equal to the other Location.

        Args:
            other (object): The other Location object to compare.

        Returns:
            bool: True if the current Location is less than the other Location, False otherwise.
        """
        return abs(self.x )< abs(other.x) or abs(self.y) < abs(other.y) or abs(self.z) < abs(other.z)