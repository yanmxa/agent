import pygame
import random
import os
from context import Context
from wolf import Wolf
from rabbit import Rabbit
from grass import Grass

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 40  # Increase cell size for better visibility
ROWS, COLS = 20, 30  # Larger grid
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
RED = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)

# Paths for Icons
script_dir = os.path.dirname(os.path.abspath(__file__))
wolf_icon = pygame.image.load(os.path.join(script_dir, "images", "wolf_icon.png"))
rabbit_icon = pygame.image.load(os.path.join(script_dir, "images", "rabbit_icon.png"))
grass_icon = pygame.image.load(os.path.join(script_dir, "images", "pasture_icon.png"))
barren_icon = pygame.image.load(os.path.join(script_dir, "images", "barren_icon.png"))

# Resize Icons
wolf_icon = pygame.transform.scale(wolf_icon, (CELL_SIZE, CELL_SIZE))
rabbit_icon = pygame.transform.scale(rabbit_icon, (CELL_SIZE, CELL_SIZE))
grass_icon = pygame.transform.scale(grass_icon, (CELL_SIZE, CELL_SIZE))
barren_icon = pygame.transform.scale(barren_icon, (CELL_SIZE, CELL_SIZE))

# Initialize font
font = pygame.font.SysFont("Arial", 20)


grid_map = [[None for _ in range(COLS)] for _ in range(ROWS)]

ctx = Context(grid=grid_map, col_num=COLS, row_num=ROWS)

# Simulation Time (in months)
month = 0


# Helper functions
def place_entities():
    # wolves  0.1: 0 ~ 0.05
    # rabbits 0.2: 0.1 ~ 0.3
    # grass   0.3: 0.3 ~ 0.6

    for row in range(ROWS):
        for col in range(COLS):
            val = random.random()
            if val < 0.05:
                grid_map[row][col] = Wolf(position=(row, col), ctx=ctx)
            elif val < 0.3:
                grid_map[row][col] = Rabbit(position=(row, col), ctx=ctx)
            elif val < 0.6:
                grid_map[row][col] = Grass(position=(row, col), ctx=ctx)


def draw_window():
    global month
    screen.fill(WHITE)

    wolves = []
    rabbits = []
    grasses = []

    # Draw the entities
    for row in range(ROWS):
        for col in range(COLS):
            cell = grid_map[row][col]
            if isinstance(cell, Wolf):
                screen.blit(wolf_icon, (col * CELL_SIZE, row * CELL_SIZE))
                wolves.append(cell)
            elif isinstance(cell, Rabbit):
                screen.blit(rabbit_icon, (col * CELL_SIZE, row * CELL_SIZE))
                rabbits.append(cell)
            elif isinstance(cell, Grass):
                screen.blit(grass_icon, (col * CELL_SIZE, row * CELL_SIZE))
                grasses.append(cell)
            elif cell is None:
                screen.blit(barren_icon, (col * CELL_SIZE, row * CELL_SIZE))

    # Display month and object sizes
    month_text = font.render(f"Month: {month}", True, TEXT_COLOR)
    screen.blit(month_text, (10, HEIGHT - 40))

    wolves_text = font.render(f"Wolves: {len(wolves)}", True, TEXT_COLOR)
    screen.blit(wolves_text, (10, HEIGHT - 70))

    rabbits_text = font.render(f"Rabbits: {len(rabbits)}", True, TEXT_COLOR)
    screen.blit(rabbits_text, (10, HEIGHT - 100))

    grass_text = font.render(f"Grass Patches: {len(grasses)}", True, TEXT_COLOR)
    screen.blit(grass_text, (10, HEIGHT - 130))

    pygame.display.update()

    return (wolves, rabbits, grasses)


# Main game loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wolf, Rabbit, and Grass Simulation")

place_entities()

wolves, rabbits, grasses = draw_window()
# Game loop
running = True
while running:
    import time

    time.sleep(1)
    month += 1  # Increment the month each cycle
    pygame.time.Clock().tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for g in grasses:
        g.reproduce()

    for r in rabbits:
        r.grow()
        r.move()
        r.breed()

    for w in wolves:
        w.grow()
        w.move()
        w.breed()

    wolves, rabbits, grasses = draw_window()

pygame.quit()
