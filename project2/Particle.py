class Particle:
    def __init__(self, grid, x=0, y=0):
        self.grid = grid
        self.x = x
        self.y = y

    def move(self):

        new_coords = self.physics()

        if new_coords is None:
            return

        self.grid.set(self.x, self.y, None)
        self.x, self.y = new_coords
        self.grid.set(self.x, self.y, self)




    def __str__(self) -> str:
        return f'{type(self).__name__}({self.x},{self.y})'