# created a wire between two gates
class Wire:

    def __init__(self, gateA, gateB):
        self.gateA = gateA
        self.gateB = gateB
        self.wires = []

    def add_wire_part(self, from_location, to_location):
        self.wires.append(WireUnit(from_location, to_location))

    def remove_wire_part(self):
        return self.wires.pop()
    
    def check_is_connected(self):
        #TODO check if there is a completed wire between gateA and gateB and return true if there is
        if (self.wires[len(self.wires - 1)].to_location):
            return True
    
    def get_wire_length(self):
        return len(self.wires)

# create a wire, keeping track of length and the dd
class WireUnit:

    def __init__(self, from_location, to_location):
        self.from_location = from_location
        self.to_location = to_location