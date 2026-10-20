from Particle import Particle

class Sand(Particle):
    def physics(self):
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
        # check if in the bounds of grid
        if not self.grid.in_bounds(x, y):
            return False

        if self.grid.get(x, y) is not None:
            return False

        return True


class Rock(Particle):
    def physics(self):
        return None


class Bubble(Particle):
    def physics(self):
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
        # check if in the bounds of grid
        if not self.grid.in_bounds(x, y):
            return False

        if self.grid.get(x, y) is not None:
            return False

        return True