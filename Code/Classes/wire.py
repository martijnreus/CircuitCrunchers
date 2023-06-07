# create a wire, keeping track of length and the dd
class wire:

    def __init__(self, from_location, to_location, length):
        self.from_location = from_location
        self.to_location = to_location
        self.length = length