class Particle:
    def __init__(self, grid, x=0, y=0):
        self.grid = grid
        self.x = x
        self.y = y

    def move(self):
        """
        Moves an object to a new location based on the physics function and then sets the object's coordinates to the new location.
        """

        new_coords = self.physics()

        if new_coords is None:
            return

        self.grid.set(self.x, self.y, None)
        self.x, self.y = new_coords
        self.grid.set(self.x, self.y, self)




    def __str__(self) -> str:
        """
        Returns a string with the output of the function
        """
        return f'{type(self).__name__}({self.x},{self.y})'