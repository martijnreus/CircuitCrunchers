# create a gate, identified by id number. and location
class Gate:
    """
    Represents a gate on a chip.
    """

    def __init__(self, id_num: int, location: object):
        """
        Initialize a Gate object with the given ID number and location.

        Post-conditions:
            - Initializes a Gate object with the provided ID number and location.
        """
        self.id_num = id_num
        self.location = location