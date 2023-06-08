# created a wire between two gates
class Wire:

    def __init__(self, gateA: object, gateB: object)-> None:
        self.gateA = gateA
        self.gateB = gateB
        self.wires = []

    def add_wire_part(self, direction: object)-> None:
        self.wires.append(WireUnit(self.get_wire_part_start()), self.get_wire_part_end(direction))
        
    def get_wire_part_start(self):
        # Add wire to gateA if there is no wire yet
        if (self.get_wire_length() == 0):
            return self.gateA.location
        # add wire to the last wire part if there is not
        else:
            return self.wires[self.get_wire_length() - 1]
        
    def get_wire_part_end(self, direction):
        # add the direction to the begin_position
        to_x = self.get_wire_part_start().x + direction.x
        to_y = self.get_wire_part_start().y + direction.y
        to_z = self.get_wire_part_start().z + direction.z

        to_location = direction(to_x, to_y, to_z)
        return to_location

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

# create a wireUnit, where its location of the start and end is tracked
class WireUnit:

    def __init__(self, from_location: object, to_location: object):
        self.from_location = from_location
        self.to_location = to_location

