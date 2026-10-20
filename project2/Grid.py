from copy import deepcopy

class Grid:
    width = 0
    height = 0
    array = 0

    def __init__(self, width, height):
        """
        Create grid `array` width by height. Create a Grid object with
        a width, height, and array. Initially all locations hold None.
        >>> grid = Grid(2, 2)
        >>> grid.array
        [[None, None], [None, None]]
        """
        self.width = width
        self.height = height
        self.array = [[None for _ in range(width)] for _ in range(height)]

    def get(self, x, y):
        """
        Gets the value stored value at (x, y).
        (x, y) should be in bounds.
        >>> grid = Grid(2, 2)
        >>> grid.array = [[1, 2], [4, 5]]
        >>> grid.get(0, 1)
        4
        >>> grid.get(1, 0)
        2
        """
        if self.in_bounds(x, y):
            return self.array[y][x]
        else:
            raise IndexError('Coordinates are out of bounds.')

    def set(self, x, y, val):
        """
        Sets a new value into the grid at (x, y).
        (x, y) should be in bounds.
        >>> grid = Grid(2, 2)
        >>> grid.set(1, 1, "Milk")
        >>> grid.set(1, 0, "Dud")
        >>> grid.array
        [[None, 'Dud'], [None, 'Milk']]
        """
        if self.in_bounds(x, y):
            self.array[y][x] = val
            return None
        else:
            raise IndexError('Coordinates are out of bounds.')

    def in_bounds(self, x, y):
        """
        Returns True if (x, y) is in bounds
        >>> grid = Grid(3, 4)
        >>> grid.in_bounds(0, 0)
        True
        >>> grid.in_bounds(2, 3)
        True
        >>> grid.in_bounds(-1, -1)
        False
        >>> grid.in_bounds(3, 4)
        False
        """
        return self.width > x > -1 and self.height > y > -1

    @staticmethod
    def build(lst):
        """
        Given a list that represents a 2D nested Grid construct a Grid object.
        Grid.build([[1, 2, 3], [4, 5 6]])
        >>> Grid.build([[1, 2, 3], [4, 5, 6]]).array
        [[1, 2, 3], [4, 5, 6]]
        """
        Grid.check_list_malformed(lst)
        width = len(lst[0])
        height = len(lst)
        grid = Grid(width, height)
        grid.array = deepcopy(lst)

        return grid

    def copy(self):
        """
        Creates a deep copy of a grid
        """
        return deepcopy(self)

    @staticmethod
    def check_list_malformed(lst):
        """
        Given a list that represents a 2D nested Grid, check that it has the
        right shape. Raise a ValueError if it is malformed.
        >>> Grid.check_list_malformed([[1, 2], [4, 5]])
        >>> Grid.check_list_malformed(1)
        Traceback (most recent call last):
        ...
        ValueError: Input must be a non-empty list of lists.
        >>> Grid.check_list_malformed([[1, 2], [4, 5, 6]])
        Traceback (most recent call last):
        ...
        ValueError: All items in list must be lists of the same length.
        >>> Grid.check_list_malformed([[1, 2], 3])
        Traceback (most recent call last):
        ...
        ValueError: Input must be a list of lists.
        """
        if type(lst) is not list:
            raise ValueError('Input must be a non-empty list of lists.')

        if len(lst) == 0:
            raise ValueError('Input must be a non-empty list of lists.')

        if type(lst[0]) is not list:
            raise ValueError('Input must be a non-empty list of lists.')

        default_length = len(lst[0])

        for value in lst:
            if type(value) is not list:
                raise ValueError('Input must be a list of lists.')
            if len(value) is not default_length:
                raise ValueError('All items in list must be lists of the same length.')


    def __str__(self) -> str:
        """
        >>> print(Grid(6, 2))
        Grid(6, 2, first = None)
        """
        return f'Grid({self.width}, {self.height}, first = {self.array[0][0]})'

    def __repr__(self) -> str:
        """
        >>> repr(Grid.build([[5, 5], [3, 2]]))
        'Grid.build([[5, 5], [3, 2]])'
        """
        return f'Grid.build({self.array})'

    def __eq__(self, other: object, /) -> bool:
        """
        >>> grid1 = Grid.build([[1, 1, 1], [2, 3, 5]])
        >>> grid2 = Grid.build([[1, 1, 1], [2, 3, 5]])
        >>> grid_lst = [[1, 1, 1], [2, 3, 5]]
        >>> grid1 == grid2
        True
        >>> grid1 == grid_lst
        True
        """
        if isinstance(other, Grid):
            if self.array == other.array:
                return True
        return self.array == other