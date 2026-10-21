from Particle import Particle

class Sand(Particle):
    """
Decides where the sand particle should move next

sand tries to fall straight down. If blocked it first tries to move left-down then right down if open.

returns a tuple (x,y) with the new position, or None if the sand can't move
    """
    def physics(self):
        """
        Sets the physics of the sand particles
        """
        # check if below is open
        if self.is_move_ok(self.x, self.y + 1):
            return self.x, self.y + 1

        # if not check if corners are open and make sure the adjacent block is open
        # left corner
        if self.is_move_ok(self.x - 1, self.y) and self.is_move_ok(self.x - 1, self.y + 1):
            return self.x - 1, self.y + 1

        # right corner
        if self.is_move_ok(self.x + 1, self.y) and self.is_move_ok(self.x + 1, self.y + 1):
            return self.x + 1, self.y + 1

        return None

    def is_move_ok(self, x, y):
        """
        check if in the bounds of grid
        takes an x and y values
        returns if those values are in the bounds of the grid
        """
        if not self.grid.in_bounds(x, y):
            return False

        if self.grid.get(x, y) is not None:
            return False

        return True


class Rock(Particle):
    """
    takes in a particle object uses a null physics method
    returns None
    """
    def physics(self):
        """
        returns None
        """
        return None


class Bubble(Particle):
    """
Creates a bubble particle
Then decided where the bubble should move next
The bubble moves up if not blocked
if it is blocked it tries to move right then down or left then down if open.
Returns a tuple with the new position or None if the bubble can't move
        """
    def physics(self):
        """
        Sets the physics of the Bubble particles
        """
        # check if above is open
        if self.is_move_ok(self.x, self.y - 1):
            return self.x, self.y - 1

        # if not check if corners are open and make sure the adjacent block is open
        # right corner
        if self.is_move_ok(self.x + 1, self.y) and self.is_move_ok(self.x + 1, self.y - 1):
            return self.x + 1, self.y - 1

        # left corner
        if self.is_move_ok(self.x - 1, self.y) and self.is_move_ok(self.x - 1, self.y - 1):
            return self.x - 1, self.y - 1

        return None

    def is_move_ok(self, x, y):
        """
        Checks if it is okay to move up
        takes in x and y values
        returns if those values are in the bounds of the grid

        """
        # check if in the bounds of grid
        if not self.grid.in_bounds(x, y):
            return False

        if self.grid.get(x, y) is not None:
            return False

        return True