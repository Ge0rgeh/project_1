from byu_pytest_utils import with_import, tier
from functools import cache


core = tier('Core', 1)
advanced = tier('Advanced', 2)
excellent = tier('Excellent', 3)


@cache
def make_wrapper_class(Object):
    class ObjectWrapper(Object):
        def __eq__(self, other):
            if isinstance(other, (ObjectWrapper)):
                return str(self) == str(other)
            else:
                return False

    return ObjectWrapper


def build_grid(Grid, Sand, Rock, Bubble, lst):
    SandWrapper = make_wrapper_class(Sand)
    RockWrapper = make_wrapper_class(Rock)
    BubbleWrapper = make_wrapper_class(Bubble)

    grid = Grid.build(lst)
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get(x, y) == "s":
                grid.set(x, y, SandWrapper(grid, x, y))
            elif grid.get(x, y) == "r":
                grid.set(x, y, RockWrapper(grid, x, y))
            elif grid.get(x, y) == "b":
                grid.set(x, y, BubbleWrapper(grid, x, y))

    def fancy_grid_toString(self):

        def get_particle_string(obj):
            if isinstance(obj, (Sand, SandWrapper)):
                return "s"
            elif isinstance(obj, (Rock, RockWrapper)):
                return "r"
            elif isinstance(obj, (Bubble, BubbleWrapper)):
                return "b"
            elif obj is None:
                return " "
            else:
                return "?"

        assert isinstance(self, Grid), "Either you did this on purpose, or something went horribly wrong"
        s = "\n"  # We lead with a newline to get off a possibly indented line
        for y in range(self.height):
            for x in range(self.width):
                s += "|" + get_particle_string(self.get(x, y))
            s += "|\n"
        return s

    Grid.__str__ = fancy_grid_toString

    return grid


def construct_all_objects_list(Sand, Rock, Bubble, grid):
    all_grid_objects = []
    for y in range(grid.height):
        for x in range(grid.width):
            space = grid.get(x, y)
            if isinstance(space, (Sand, Rock, Bubble)):
                all_grid_objects.append(space)
    return all_grid_objects


def wrap_all_grid_objects(all_grid_objects, grid, Sand, Rock, Bubble):
    Sandwrapper = make_wrapper_class(Sand)
    Rockwrapper = make_wrapper_class(Rock)
    Bubblewrapper = make_wrapper_class(Bubble)
    new_all_grid_objects = []
    for object in all_grid_objects:
        if isinstance(object, Sand):
            grid.set(object.x, object.y, Sandwrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Sandwrapper(object.grid, object.x, object.y))
        elif isinstance(object, Rock):
            grid.set(object.x, object.y, Rockwrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Rockwrapper(object.grid, object.x, object.y))
        elif isinstance(object, Bubble):
            grid.set(object.x, object.y, Bubblewrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Bubblewrapper(object.grid, object.x, object.y))
    return new_all_grid_objects


def make_core_grid(Grid, Rock):
    class CoreGrid(Grid):
        def __str__(self):
            def get_particle_string(obj):
                if isinstance(obj, Rock):
                    return "r"
                elif obj is None:
                    return " "
                else:
                    return "?"
            s = "\n"
            for y in range(self.height):
                for x in range(self.width):
                    s += "|" + get_particle_string(self.get(x, y))
                s += "|\n"
            return s
    return CoreGrid


def build_core_grid(Grid, Rock, lst):
    CoreGrid = make_core_grid(Grid, Rock)
    RockWrapper = make_wrapper_class(Rock)
    grid = CoreGrid.build(lst)
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get(x, y) == "r":
                grid.set(x, y, RockWrapper(grid, x, y))
    return grid


def construct_core_all_objects_list(Rock, grid):
    all_grid_objects = []
    for y in range(grid.height):
        for x in range(grid.width):
            space = grid.get(x, y)
            if isinstance(space, (Rock)):
                all_grid_objects.append(space)
    return all_grid_objects


def wrap_core_all_grid_objects(all_grid_objects, grid, Rock):
    RockWrapper = make_wrapper_class(Rock)
    new_all_grid_objects = []
    for object in all_grid_objects:
        if isinstance(object, Rock):
            grid.set(object.x, object.y, RockWrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(RockWrapper(object.grid, object.x, object.y))
    return new_all_grid_objects


@cache
def make_particle_wrapper_class(Particle):
    class ParticleWrapper(Particle):
        def __eq__(self, other):
            if isinstance(other, (ParticleWrapper)):
                return str(self) == str(other)
            else:
                return False

    return ParticleWrapper


@cache
def make_air_test_particle_move_class(Particle):
    ParticleWrapper = make_particle_wrapper_class(Particle)
    class Air(ParticleWrapper):
        def physics(self):
            import random
            x_movement = random.randint(-4, 4)
            y_movement = random.randint(-4, 4)
            if self.grid.in_bounds(self.x + x_movement, self.y + y_movement):
                return self.x + x_movement, self.y + y_movement
    return Air


@core
@with_import('Particle', 'Particle')
@with_import('Grid', 'Grid')
def test_CORE_particle_str(Grid, Particle):
    grid = Grid(6, 6)
    assert str(Particle(grid, 1, 2)) == 'Particle(1,2)'
    assert str(Particle(grid, 5, 3)) == 'Particle(5,3)'


@core
@with_import('Particle', 'Particle')
@with_import('Grid', 'Grid')
def test_CORE_particle_move(Grid, Particle):
    import random
    random.seed('air')
    ParticleWrapper = make_particle_wrapper_class(Particle)
    Air = make_air_test_particle_move_class(ParticleWrapper)
    grid = Grid(6, 5)
    air1 = Air(grid)
    grid.set(0, 0, air1)
    air2 = Air(grid, 3, 1)
    grid.set(3, 1, air2)

    air1.move()
    assert air1.x == 0
    assert air1.y == 0
    assert grid.array == [[air1, None, None, None, None, None],
                        [None, None, None, air2, None, None],
                        [None, None, None, None, None, None],
                        [None, None, None, None, None, None],
                        [None, None, None, None, None, None]]

    air2.move()
    assert air2.x == 5
    assert air2.y == 0
    assert grid.array == [[air1, None, None, None, None, air2],
                        [None, None, None, None, None, None],
                        [None, None, None, None, None, None],
                        [None, None, None, None, None, None],
                        [None, None, None, None, None, None]]


@core
@with_import('Grid_Objects', 'Rock')
@with_import('Grid', 'Grid')
def test_CORE_rock_str(Grid, Rock):
    grid = Grid(6, 6)
    assert str(Rock(grid, 1, 2)) == 'Rock(1,2)'
    assert str(Rock(grid, 5, 3)) == 'Rock(5,3)'


@core
@with_import('Grid_Objects', 'Rock')
@with_import('Grid', 'Grid')
def test_CORE_rock_physics(Grid, Rock):
    grid = build_core_grid(Grid, Rock,
                      [[None, None, None],
                       [None, 'r', None],
                       [None, None, None]])
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@core
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'add_object')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid', 'Grid')
def test_CORE_add_objects(Grid, Rock, add_object, all_grid_objects):
    key_grid = build_core_grid(
        Grid, Rock,
        [[None, 'r', 'r'],
         [None, 'r', None],
         [None, None, 'r']]
    )
    key_all_grid_objects = construct_core_all_objects_list(Rock, key_grid)

    grid = build_core_grid(
        Grid, Rock,
        [[None, None, None],
         [None, None, None],
         [None, None, None]])
    add_object(grid, Rock, 1, 0)
    assert isinstance(grid.get(1, 0), Rock)
    add_object(grid, Rock, 2, 0)
    assert isinstance(grid.get(2, 0), Rock)
    add_object(grid, Rock, 1, 1)
    assert isinstance(grid.get(1, 1), Rock)
    add_object(grid, Rock, 2, 2)
    assert isinstance(grid.get(2, 2), Rock)

    all_grid_objects = wrap_core_all_grid_objects(all_grid_objects, grid, Rock)

    assert grid.array == key_grid.array, f"grid does not match key\ngrid:{grid}\nkey:{key_grid}"
    # have to sort lists before comparison in case order of objects is different
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects, "all_grid_objects list does not match key"

    add_object(grid, Rock, 1, 0)
    assert len(all_grid_objects) == 4  # the add should have failed


@core
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'remove_object')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid', 'Grid')
def test_CORE_remove_objects(Grid, Rock, remove_object, all_grid_objects):
    key_grid = build_core_grid(
        Grid, Rock,
        [[None, 'r', None],
         ['r', None, None],
         [None, 'r', 'r']]
    )
    key_all_grid_objects = construct_core_all_objects_list(Rock, key_grid)

    grid = build_core_grid(
        Grid, Rock,
        [['r', 'r', 'r'],
         ['r', 'r', 'r'],
         ['r', 'r', 'r']]
    )
    all_grid_objects[:] = construct_core_all_objects_list(Rock, grid)

    remove_object(grid, 0, 0)
    remove_object(grid, 2, 0)
    remove_object(grid, 1, 1)
    remove_object(grid, 2, 1)
    remove_object(grid, 0, 2)


    assert grid.array == key_grid.array, f"grid does not match key\ngrid:{grid}\nkey:{key_grid}. Make sure you are accessing existing sand objects using grid.get()"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects

    remove_object(grid, 0, 2)
    remove_object(grid, 2, 1)
    remove_object(grid, 1, 1)

    # the three removes should have failed
    assert len(all_grid_objects) == 4
    assert grid.get(0, 2) == None
    assert isinstance(grid.get(1, 2), Rock)


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_rock_physics(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble,
                      [[None, None, None],
                       [None, 'r', None],
                       [None, None, None]])
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_and_bubble_classes(Grid, Sand, Bubble):
    # Test that Sand is inheriting from Particle
    grid = Grid(6, 6)
    sand = Sand(grid, 1, 2)
    assert hasattr(sand, 'move'), "Sand class should have a move method (inherited from Particle)"
    assert hasattr(sand, 'grid'), "Sand class should have a grid attribute"
    assert hasattr(sand, 'x'), "Sand class should have an x attribute"
    assert hasattr(sand, 'y'), "Sand class should have a y attribute"

    # Test that Bubble is inheriting from Particle
    bubble = Bubble(grid, 3, 4)
    assert hasattr(bubble, 'move'), "Bubble class should have a move method (inherited from Particle)"
    assert hasattr(bubble, 'grid'), "Bubble class should have a grid attribute"
    assert hasattr(bubble, 'x'), "Bubble class should have an x attribute"
    assert hasattr(bubble, 'y'), "Bubble class should have a y attribute"


@advanced
def test_ADVANCED_sand_class():
    test_ADVANCED_sand_str()
    test_ADVANCED_sand_physics_out_of_bounds()
    test_ADVANCED_sand_physics_cant_move()
    test_ADVANCED_sand_physics_straight_down()
    test_ADVANCED_sand_physics_down_left()
    test_ADVANCED_sand_physics_down_right()
    test_ADVANCED_sand_physics_corner_rule()
    test_ADVANCED_sand_move_out_of_bounds()
    test_ADVANCED_sand_move_cant_move()
    test_ADVANCED_sand_move_straight_down()
    test_ADVANCED_sand_move_down_left()
    test_ADVANCED_sand_move_down_right()
    test_ADVANCED_sand_move_corner_rule()


@advanced
def test_ADVANCED_bubble_class():
    test_ADVANCED_bubble_str()
    test_ADVANCED_bubble_physics_out_of_bounds()
    test_ADVANCED_bubble_physics_cant_move()
    test_ADVANCED_bubble_physics_straight_up()
    test_ADVANCED_bubble_physics_up_right()
    test_ADVANCED_bubble_physics_up_left()
    test_ADVANCED_bubble_physics_corner_rule()
    test_ADVANCED_bubble_move_out_of_bounds()
    test_ADVANCED_bubble_move_cant_move()
    test_ADVANCED_bubble_move_straight_up()
    test_ADVANCED_bubble_move_up_right()
    test_ADVANCED_bubble_move_up_left()
    test_ADVANCED_bubble_move_corner_rule()


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_str(Grid, Sand):
    grid = Grid(6, 6)
    assert str(Sand(grid, 1, 2)) == 'Sand(1,2)'
    assert str(Sand(grid, 5, 3)) == 'Sand(5,3)'


@advanced
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_str(Grid, Bubble):
    grid = Grid(6, 6)
    assert str(Bubble(grid, 1, 2)) == 'Bubble(1,2)'
    assert str(Bubble(grid, 5, 3)) == 'Bubble(5,3)'


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_out_of_bounds(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    assert (actual := grid.get(0, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_out_of_bounds(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    assert (actual := grid.get(0, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_cant_move(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_cant_move(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_straight_down(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         [None, None, None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (1, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_straight_up(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, None, None],
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (1, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_down_left(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         [None, 'r', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (0, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_up_right(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None],
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (2, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_down_right(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['r', 's', None],
         ['r', 's', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (2, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_up_left(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'b', 'r'],
         [None, 'b', 'r']]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (0, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_physics_corner_rule(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['r', 's', 'r'],
        [None, 'r', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"

@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_physics_corner_rule(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None],
        ['r', 'b', 's']]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_out_of_bounds(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    grid = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    sand = grid.get(0, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_out_of_bounds(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    grid = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    bubble = grid.get(0, 0)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_cant_move(Grid, Bubble, Rock, Sand):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_cant_move(Grid, Bubble, Rock, Sand):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_straight_down(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
        [[None, None, None],
         [None, 's', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         [None, None, None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_straight_up(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
        [[None, 'b', None],
         [None, None, None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
        [[None, None, None],
         [None, 'b', None]])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_down_left(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, None, None],
     ['s', 'r', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 's', None],
     [None, 'r', None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_up_right(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', 'b'],
     [None, None, None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None],
     [None, 'b', None]])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_down_right(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['r', None, None],
     [None, None, None],
     ['r', 's', 's']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [['r', None, None],
     [None, 's', None],
     ['r', 's', None]])
    sand = grid.get(1, 1)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_up_left(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['b', 'b', 'r'],
     [None, None, None],
     [None, None, 'r']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'b', 'r'],
     [None, 'b', None],
     [None, None, 'r']])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_sand_move_corner_rule(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['r', 's', 'r'],
     [None, 'r', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [['r', 's', 'r'],
     [None, 'r', None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_bubble_move_corner_rule(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None],
     ['r', 'b', 's']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None],
     ['r', 'b', 's']])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@advanced
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_ADVANCED_move_falling_example(Grid, Bubble, Rock, Sand):
    keys = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'r', None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, None, 'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, 's',  None, None, 'b',  None],
             [None, 's',  None, None, None, None],
             ['s',  's',  None, None, 'r',  None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, 'b',  'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, None, None, None, None, None],
             [None, 's',  None, None, None, None],
             ['s',  's',  's',  None, 'r',  None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, 'b',  'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, None, None, None, None, None],
             [None, 's',  None, None, None, None],
             ['s',  's',  's',  None, 'r',  None]]
        )
    ]
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'r', None]]
    )
    assert grid == keys[0], f"Test setups do not match. There's probably something wrong with the tests. Let your TAs know."
    for key in keys[1:]:
        for y in (range(grid.height)):
            for x in range(grid.width):
                elem = grid.get(x, y)
                if isinstance(elem, Bubble):
                    elem.move()
        for y in reversed(range(grid.height)):
            for x in range(grid.width):
                elem = grid.get(x, y)
                if isinstance(elem, (Sand, Rock)):
                    elem.move()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@excellent
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_do_whole_grid_all_falling_rules(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None, None, None, None, None, None, None],
         ['r',  's', 'r',  's' , 'r',  None, 's',  'r',  's'],
         [None, 'r', None, None, None, None, 'r',  None, None],
         ['r',  'b', 'r',  None, 'r',  'b' , 'b',  'b', 'r'],
         [None, 'b', None, None, None, None, None, None, None]]
    )
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None, None, 's',  None, 's',  's',  None],
         ['r',  's', 'r',  None, 'r',  None, None, 'r',  None],
         [None, 'r', None, None, None, None, 'r',  None, None],
         ['r',  'b', 'r',  None, 'r',  None, None, None, 'r'],
         [None, 'b', None, None, 'b',  None, 'b',  None, 'b']]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects


@excellent
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_sand_falls_together(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(Grid, Sand, Rock, Bubble, [[None], ['s'], ['s'], ['s'], ['s']])
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(Grid, Sand, Rock, Bubble, [['s'], ['s'], ['s'], ['s'], [None]])
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects


@excellent
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_bubbles_rise_together(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(Grid, Sand, Rock, Bubble, [['b'], ['b'], ['b'], ['b'], [None]])
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(Grid, Sand, Rock, Bubble, [[None], ['b'], ['b'], ['b'], ['b']])
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects


@excellent
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_do_whole_grid_until_sand_settles(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key_grids = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             ['s', 's', None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, 's', None],
             ['s', 's', None],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             ['s', 's', 's'],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             ['s', 's', 's'],
             ['s', 's', 's']]
        )
    ]

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None]]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    for key in key_grids:
        key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

        do_whole_grid()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
        all_grid_objects.sort(key=lambda object:(object.x, object.y))
        key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
        assert all_grid_objects == key_all_grid_objects


@excellent
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_do_whole_grid_until_bubbles_settle(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key_grids = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'b',  'b'],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b', None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             [None, 'b',  'b'],
             [None, 'b',  None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             ['b',  'b',  'b'],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             ['b',  'b',  'b'],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        )
    ]

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None]]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    for key in key_grids:
        key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

        do_whole_grid()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
        all_grid_objects.sort(key=lambda object:(object.x, object.y))
        key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
        assert all_grid_objects == key_all_grid_objects


def class_docstring_test(cls):
    owner = getattr(cls, '__module__', None) or getattr(cls, '__name__', None)
    for func in dir(cls):
        attr = getattr(cls, func)
        if callable(attr) and getattr(attr, '__module__', None) == owner:
            if func.startswith('__') or func == 'main':
                continue
            assert getattr(cls, func).__doc__ is not None, f"{func}() is missing a docstring"


@excellent
@with_import('Particle', 'Particle')
@with_import('sand_simulation', 'remove_object')
@with_import('sand_simulation', 'add_object')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_EXCELLENT_docstring(Grid, Sand, Rock, Bubble, do_whole_grid, add_object, remove_object, Particle):
    class_docstring_test(Particle)
    class_docstring_test(Grid)
    class_docstring_test(Sand)
    class_docstring_test(Rock)
    class_docstring_test(Bubble)
    assert do_whole_grid.__doc__ is not None, "do_whole_grid() is missing a docstring"
    assert add_object.__doc__ is not None, "add_object() is missing a docstring"
    assert remove_object.__doc__ is not None, "remove_object() is missing a docstring"
