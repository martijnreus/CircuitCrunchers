# create a 3D space and keep track of all the locations in this space.
class location:

    def __init__(self, x, y, z, gatenum):
        self.x = x
        self.y = y
        self.z = z

# create a grid, with a width, heigth and a amount of layers
class grid:

    def __init__(self, width, heigth, layers):
        self.width = width
        self.heigth = heigth
        self.layers = layers

# create a gate, identified by id number. and location
class gate:

    def __init__(self, id_num, location):
        self.id_num = id_num
        self.location = location

# create a wire, keeping track of length and the dd
class wire:

    def __init__(self, from_location, to_location, length):
        self.from_location = from_location
        self.to_location = to_location
        self.length = length


