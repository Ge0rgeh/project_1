"""
code taken from a project at Stanford CS106A
"""

from Grid import Grid
from Grid_Objects import Bubble, Rock, Sand # imports all Grid objects

all_grid_objects = []


def add_object(grid, object_type, x, y):
    """
    Attempt to add an object to grid

    The steps are as follows:

    (1) Verify that the position specified by the x & y coordinates is empty in the grid. If not, exit.
    (2) Create a new object of type 'object_type' and set its position to the supplied x and y coordinates.
    (3) Add the new object to the all_grid_objects list.
    (4) Store a reference to the new object in the correct grid position
    :param grid: a grid to store grid objects
    :param object_type: the class of the new object to create
    :param x: the x coordinate to add the object to
    :param y: the y coordinate to add the object to
    """
    if grid.get(x,y) is not None:
        return
    object = object_type(grid,x,y)
    all_grid_objects.append(object)
    grid.set(x,y,object)




def remove_object(grid, x, y):
    """
    Attempt to remove an object from grid

    The steps are as follows:

    (1) Verify that there is a particle of some kind in the specified position. If not, exit.
    (2) Remove the reference to the object from the grid.
    (3) Remove the object from the all_grid_objects list.
    :param grid: a grid to store grid objects
    :param x: the x coordinate to remove the object from
    :param y: the y coordinate to remove the object from
    """

    object = grid.get(x,y)

    if object is None:
        return

    grid.set(x, y, None)

    all_grid_objects.remove(object)


def do_whole_grid():
    """
    Do one round of gravity over the whole grid.

    The steps are as follows:

    (1) run the `move()` function of all `Bubble` objects in the grid (use your `all_grid_objects` list)
    (2) reverse the order of the list with the `<list>.reverse()` function
    (3) run the `move()` function of all `Sand` objects in the grid
    (4) reverse the order of the list one last time because it will make sorting the list next time just that much easier
    """
    all_grid_objects.sort(key=lambda particle: (particle.y, particle.x))
    """*** YOUR CODE HERE ***"""
    for obj in all_grid_objects:
        if isinstance(obj, Bubble):
            obj.move()
    all_grid_objects.reverse()
    for obj in all_grid_objects:
        if isinstance(obj, Sand):
            obj.move()
    all_grid_objects.reverse()




#########################################################
'''
Down here is not especially pretty code to set up the GUI,
handle the controls, and draw the grid to the screen.

Don't write any code below here.
'''

# Set up some constants
HEADER_THICKNESS = 40 # thickness of header menu bar in pixels
WIDTH, HEIGHT = 500, 500 + HEADER_THICKNESS # 500 x 500 for simulation, 40 pixel header for buttons
SCALE = 10 # pixels per particle
FPS = 60
INPUT_SAMPLE_RATE = 180
BIG_ERASE_RADIUS = 5

BLACK = (0, 0, 0)
YELLOW = (224, 177, 22)
LIGHT_BLUE = (56, 141, 207)
PURPLE = (128, 0, 128)
DARK_GRAY = (33, 33, 33)
LIGHT_GRAY = (240, 240, 240)

FONT = None
B_GRAVITY = None
B_BRUSH = None
B_ERASE = None

def mainloop(grid, window, clock):
    # Game loop
    running = True
    updates_per_frame = INPUT_SAMPLE_RATE/FPS
    frame = 0
    do_gravity = True
    brush_mode = 's'
    erase_mode = 's'

    # Button surfaces
    global B_GRAVITY, B_BRUSH, B_ERASE
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] < HEADER_THICKNESS: # menu button press
                if 0 <= event.pos[0] < 121:
                    do_gravity = not do_gravity
                elif 121 <= event.pos[0] < 292:
                    if brush_mode == 's':
                        brush_mode = 'r'
                    elif brush_mode == 'r':
                        brush_mode = 'b'
                    else:
                        brush_mode = 's'
                elif 292 <= event.pos[0] < 500:
                    if erase_mode == 's':
                        erase_mode = 'b'
                    else:
                        erase_mode = 's'
                update_buttons(do_gravity, brush_mode, erase_mode)


        if pygame.mouse.get_pressed()[0]: # Get the state of left click
            x, y = pygame.mouse.get_pos()
            if y >= HEADER_THICKNESS: # check for menu bar presses
                x //= SCALE
                y = (y - HEADER_THICKNESS) // SCALE
                if grid.in_bounds(x, y):
                    if brush_mode == 's':
                        if grid.get(x, y) is not None:
                            remove_object(grid, x, y)
                        add_object(grid, Sand, x, y)
                    elif brush_mode == 'r':
                        if grid.get(x, y) is not None:
                            remove_object(grid, x, y)
                        add_object(grid, Rock, x, y)
                    elif brush_mode == 'b':
                        if grid.get(x, y) is not None:
                            remove_object(grid, x, y)
                        add_object(grid, Bubble, x, y)

        elif pygame.mouse.get_pressed()[2]: # check right click
            x, y = pygame.mouse.get_pos()
            if y >= HEADER_THICKNESS: # check for menu bar presses
                x //= SCALE
                y = (y - HEADER_THICKNESS) // SCALE
                if grid.in_bounds(x, y):
                    if erase_mode == 's':
                        remove_object(grid, x, y)
                    elif erase_mode == 'b':
                        big_erase(grid, x, y)


        if frame == updates_per_frame:
            frame = 0
            draw_simulation(window, grid)
            draw_header(window)
            if do_gravity:
                do_whole_grid()
            pygame.display.flip()
        frame += 1

        # Cap the frame rate
        clock.tick(INPUT_SAMPLE_RATE)

def draw_simulation(window, grid):
    # Draw everything
    window.fill(LIGHT_GRAY)
    for y in range(grid.height):
        for x in range(grid.width):
            val = grid.get(x, y)
            if val:
                if isinstance(val, Rock):
                    color = DARK_GRAY
                elif isinstance(val, Sand):
                    color = YELLOW
                elif isinstance(val, Bubble):
                    color = LIGHT_BLUE
                else:
                    color = PURPLE
                pygame.draw.rect(window, color, pygame.Rect(x * SCALE, HEADER_THICKNESS + y * SCALE, SCALE, SCALE))
    pygame.draw.rect(window, BLACK, pygame.Rect(0, HEADER_THICKNESS, WIDTH, HEIGHT-HEADER_THICKNESS), 1)


def draw_header(window):
    pygame.draw.rect(window, BLACK, pygame.Rect(0, 0, 122, HEADER_THICKNESS+1), 1)
    pygame.draw.rect(window, BLACK, pygame.Rect(121, 0, 172, HEADER_THICKNESS+1), 1)
    pygame.draw.rect(window, BLACK, pygame.Rect(292, 0, 208, HEADER_THICKNESS+1), 1)
    window.blit(B_GRAVITY, (9, 10))
    window.blit(B_BRUSH, (130, 10))
    window.blit(B_ERASE, (301, 10))


def big_erase(grid:Grid, x, y):
    for j in range(-BIG_ERASE_RADIUS, BIG_ERASE_RADIUS+1):
        for i in range(-BIG_ERASE_RADIUS, BIG_ERASE_RADIUS+1):
            if grid.in_bounds(x + i, y + j):
                remove_object(grid, x + i, y + j)

def update_buttons(do_gravity, brush_mode, erase_mode):
    global B_GRAVITY, B_BRUSH, B_ERASE
    if do_gravity:
        B_GRAVITY = FONT.render("Gravity: On", True, BLACK, LIGHT_GRAY)
    else:
        B_GRAVITY = FONT.render("Gravity: Off", True, BLACK, LIGHT_GRAY)

    if brush_mode == 's':
        B_BRUSH = FONT.render("Left Click: Sand", True, BLACK, LIGHT_GRAY)
    elif brush_mode == 'r':
        B_BRUSH = FONT.render("Left Click: Rock", True, BLACK, LIGHT_GRAY)
    elif brush_mode == 'b':
        B_BRUSH = FONT.render("Left Click: Bubble", True, BLACK, LIGHT_GRAY)

    if erase_mode == 's':
        B_ERASE = FONT.render("Right Click: Erase", True, BLACK, LIGHT_GRAY)
    elif erase_mode == 'b':
        B_ERASE = FONT.render("Right Click: Big Erase", True, BLACK, LIGHT_GRAY)

def update_fps_counter(window, fps):
    window.blit(B_ERASE, (263, 10))

def main():
    global pygame
    import pygame
    # Initialize Pygame
    pygame.init()
    pygame.font.init()

    global FONT
    FONT = pygame.font.SysFont("Arial", 20)
    update_buttons(True, 's', 's')

    # Create the window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Simulation")

    # Set up the clock for managing frame rate
    clock = pygame.time.Clock()

    # Set up the grid
    grid = Grid(WIDTH // SCALE, (HEIGHT - HEADER_THICKNESS) // SCALE)

    mainloop(grid, window, clock)

if __name__ == "__main__":
    main()
