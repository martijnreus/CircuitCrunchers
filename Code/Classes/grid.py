###################################################
# initializes grid class 
###################################################

# create a grid, with a width, heigth and an amount of layers
class Grid:
    """
    Represents a grid on a chip.
    """
    def __init__(self, width: int, height: int, layers: int)-> None:
        """
        Initialize a Grid object with the given width, height, and number of layers.

        Pre-conditions:
            - `width`, `height`, and `layers` are valid positive integers.

        Post-conditions:
            - Initializes a Grid object with the provided width, height, and layers.
        """
        self.width = width
        self.height = height
        self.layers = layers

    def get_max_locations(self):
        """
        Get the maximum coordinates (x, y, z) of the grid.

        Pre-conditions:
            - The Grid object has been initialized with valid width, height, and layers.

        Post-conditions:
            - Returns a list [max_x, max_y, max_z] representing the maximum coordinates of the grid.
        """
        max_x = self.width
        max_y = self.height
        max_z = self.layers
        xyz = [max_x, max_y, max_z]

        return xyz