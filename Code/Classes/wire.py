# create a network that keeps track of all the wires
class Network:

    def __init__(self):
        self.network = {}

    def create_new_wire(self, gateA, gateB):
        self.network[f"{gateA}-{gateB}"] = []

    def add_wire_part(self, gateA, gateB, location, direction):
        self.network[f"{gateA}-{gateB}"].append(WireUnit(location, direction))

    def remove_wire_part(self, gateA, gateB):
        return self.network[f"{gateA}-{gateB}"].pop()
    
    def check_is_connected(self, gateA, gateB):
        #TODO check if there is a completed wire between gateA and gateB and return true if there is
        return True
    
# created a wire between two gates
class Wire:

    def __init__(self, gateA, gateB):
        self.gateA = gateA
        self.gaetB = gateB
        self.wires = []

    def add_wire_part(self, from_location, to_location):
        self.wires.append(WireUnit(from_location, to_location))

    def remove_wire_part(self):
        return self.wires.pop()
    
    def check_is_connected(self):
        #TODO check if there is a completed wire between gateA and gateB and return true if there is
        return True

# create a wire, keeping track of length and the dd
class WireUnit:

    def __init__(self, from_location, to_location):
        self.from_location = from_location
        self.to_location = to_location