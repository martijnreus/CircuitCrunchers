# created a wire between two gates
class Wire:

    def __init__(self, gateA: object, gateB: object)-> None:
        self.gateA = gateA
        self.gateB = gateB
        self.wires = []

    def add_wire_part(self, from_location: object, to_location: object)-> None:
        self.wires.append(WireUnit(from_location, to_location))

    def remove_wire_part(self)-> int:
        return self.wires.pop()
    
    def check_is_connected(self)-> bool:
        # checks if the location of the last wire matches the location of gateB
        if (self.wires[len(self.wires - 1)].to_location.x == self.gateB.location.x):
            if (self.wires[len(self.wires - 1)].to_location.y == self.gateB.location.y):
                if (self.wires[len(self.wires - 1)].to_location.z == self.gateB.location.z):
                    return True
                
        return False
    
    def get_wire_length(self)-> list[int]:
        return len(self.wires)

# create a wire, keeping track of length and the dd
class WireUnit:

    def __init__(self, from_location: object, to_location: object):
        self.from_location = from_location
        self.to_location = to_location