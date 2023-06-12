# create a grid, with a width, heigth and a amount of layers
class Grid:

    def __init__(self, width: int, height: int, layers: int)-> None:
        self.width = width
        self.height = height
        self.layers = layers

    def get_max_locations(self):
        max_x = self.width - 1
        max_y = self.height - 1
        max_z = self.layers - 1
        xyz = [max_x, max_y, max_z]
        return xyz