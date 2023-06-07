class Network:

    def __init__(self):
        self.network = {}

    def create_new_wire(self, gateA, gateB):
        self.network[f"{gateA}-{gateB}"] = []

    def add_wire_part(self, gateA, gateB, location, direction):
        self.network[f"{gateA}-{gateB}"].append(Wire(location, direction, 1))

    def remove_wire_part(self, gateA, gateB):
        return self.network[f"{gateA}-{gateB}"].pop()
    
    def check_is_connected(self, gateA, gateB):
        #TODO check if there is a completed wire between gateA and gateB and return true if there is
        return True

# create a wire, keeping track of length and the dd
class Wire:

    def __init__(self, from_location, to_location, length):
        self.from_location = from_location
        self.to_location = to_location
        self.length = length