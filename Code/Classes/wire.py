class network:

    def __init__(self):
        self.wires = []

    def addWire(self, location, direction):
        self.wires.append(wire(location, direction, 1))

    def removeWire(self):
        return self.wires.pop()

# create a wire, keeping track of length and the dd
class wire:

    def __init__(self, from_location, to_location, length):
        self.from_location = from_location
        self.to_location = to_location
        self.length = length