# create a 3D space and keep track of all the locations in this space.
class Location:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    
    # if compared, it compares the whole location with their respective x y and z 
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y, self.z + other.z)