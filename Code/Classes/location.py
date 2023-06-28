###################################################
# initializes Location class 
###################################################

# create a 3D space and keep track of all the locations in this space.
class Location:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    # defining "="
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # defining "+"
    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y, self.z + other.z)

    # defining "-"
    def __sub__(self, other):
        return Location(self.x - other.x, self.y - other.y, self.z - other.z)

    # defining representation
    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    # defining ">"
    def __ge__(self, other):
        return self.x > other.x or self.y > other.y or self.z > other.z

    # defining "<"
    def __le__(self, other):
        return abs(self.x )< abs(other.x) or abs(self.y) < abs(other.y) or abs(self.z) < abs(other.z)