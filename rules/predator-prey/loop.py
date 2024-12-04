import pygame
import random
import os
import time
from context import Context
from wolf import Wolf
from rabbit import Rabbit
from grass import Grass

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 26  # Smaller cell size for better fitting
ROWS, COLS = 30, 60  # Smaller grid size
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
LINE_COLOR_WOLF = (255, 0, 0)  # Red for wolves
LINE_COLOR_RABBIT = (0, 255, 255)  # Cyan for grass
LINE_COLOR_GRASS = (0, 255, 0)  # Green for rabbits
LINE_COLOR_BORDER = (169, 169, 169)  # Gray for border

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

# History to track counts for line chart (month, wolves, rabbits, grass)
history = []


# Helper functions
def place_entities():
    for row in range(ROWS):
        for col in range(COLS):
            val = random.random()
            if val < 0.02:
                grid_map[row][col] = Wolf(position=(row, col), ctx=ctx)
            elif val < 0.3:
                grid_map[row][col] = Rabbit(position=(row, col), ctx=ctx)
            elif val < 0.6:
                grid_map[row][col] = Grass(position=(row, col), ctx=ctx)


def draw_window(chat_height=150):
    global month
    screen.fill(WHITE)

    wolves = []
    rabbits = []
    grasses = []

    # Draw the entities in the main grid (Left Panel)
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

    # Add counts to the history
    history.append((month, len(wolves), len(rabbits), len(grasses)))

    # Draw the chart and month title
    draw_line_chart(month, chat_height)

    pygame.display.update()

    return (wolves, rabbits, grasses)


def draw_line_chart(month, chart_height):
    """Draw a more visually appealing line chart at the bottom with the history of counts."""
    chart_width = WIDTH
    chart_bottom = HEIGHT + chart_height

    # Background gradient for the chart
    gradient_start = (245, 245, 245)  # Light gray
    gradient_end = (255, 255, 255)  # White
    for i in range(chart_height):
        color = (
            int(
                gradient_start[0]
                + (gradient_end[0] - gradient_start[0]) * (i / chart_height)
            ),
            int(
                gradient_start[1]
                + (gradient_end[1] - gradient_start[1]) * (i / chart_height)
            ),
            int(
                gradient_start[2]
                + (gradient_end[2] - gradient_start[2]) * (i / chart_height)
            ),
        )
        pygame.draw.line(
            screen,
            color,
            (0, chart_bottom - chart_height + i),
            (chart_width, chart_bottom - chart_height + i),
        )

    # Draw chart title with the current month
    title_text = font.render(
        f"Month: {month}", True, (50, 50, 50)
    )  # Darker gray for better contrast
    screen.blit(
        title_text,
        (
            chart_width // 2 - title_text.get_width() // 2,
            chart_bottom - chart_height + 10,
        ),
    )

    # Set up scales and axes
    max_y_value = max(
        [
            max(history, key=lambda x: x[1])[1],
            max(history, key=lambda x: x[2])[2],
            max(history, key=lambda x: x[3])[3],
            1,
        ]
    )
    x_scale = (chart_width - 20) / len(history)  # Scale for months
    y_scale = (chart_height - 40) / max_y_value  # Scale for population count

    # Draw axes with softer colors
    axis_color = (150, 150, 150)  # Soft gray for axes
    pygame.draw.line(
        screen,
        axis_color,
        (10, chart_bottom - 20),
        (chart_width - 10, chart_bottom - 20),
        2,
    )  # X-axis
    pygame.draw.line(
        screen,
        axis_color,
        (10, chart_bottom - 20),
        (10, chart_bottom - chart_height + 20),
        2,
    )  # Y-axis

    # Draw labels on X-axis and Y-axis with appropriate spacing
    for i, (month, wolves_count, rabbits_count, grass_count) in enumerate(history):
        # X-axis: Month labels
        pygame.draw.line(
            screen,
            axis_color,
            (int(10 + i * x_scale), chart_bottom - 20),
            (int(10 + i * x_scale), chart_bottom - 25),
            2,
        )

    # Draw the lines for each entity type (Wolves, Rabbits, Grass) with smooth colors
    last_wolf_pos = None
    last_rabbit_pos = None
    last_grass_pos = None
    for i, (month, wolves_count, rabbits_count, grass_count) in enumerate(history):
        # Scale the values to fit into the chart area
        wolf_pos = (
            int(10 + i * x_scale),
            chart_bottom - 20 - int(wolves_count * y_scale),
        )
        rabbit_pos = (
            int(10 + i * x_scale),
            chart_bottom - 20 - int(rabbits_count * y_scale),
        )
        grass_pos = (
            int(10 + i * x_scale),
            chart_bottom - 20 - int(grass_count * y_scale),
        )

        # Draw the lines with smoother and more suitable colors
        if last_wolf_pos:
            pygame.draw.line(
                screen, LINE_COLOR_WOLF, last_wolf_pos, wolf_pos, 3
            )  # Orange-red for Wolves
        last_wolf_pos = wolf_pos

        if last_rabbit_pos:
            pygame.draw.line(
                screen, LINE_COLOR_RABBIT, last_rabbit_pos, rabbit_pos, 3
            )  # Light green for Rabbits
        last_rabbit_pos = rabbit_pos

        if last_grass_pos:
            pygame.draw.line(
                screen, LINE_COLOR_GRASS, last_grass_pos, grass_pos, 3
            )  # Cyan for Grass
        last_grass_pos = grass_pos

    # Display chart labels with improved readability
    wolf_label = font.render("Wolves", True, LINE_COLOR_WOLF)  # Orange-red for Wolves
    screen.blit(wolf_label, (chart_width - 90, chart_bottom - 40))
    rabbit_label = font.render(
        "Rabbits", True, LINE_COLOR_RABBIT
    )  # Light green for Rabbits
    screen.blit(rabbit_label, (chart_width - 90, chart_bottom - 60))
    grass_label = font.render("Grass", True, LINE_COLOR_GRASS)  # Cyan for Grass
    screen.blit(grass_label, (chart_width - 90, chart_bottom - 80))


# Main game loop
chart_height = 150
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT + chart_height)  # Account for the mini-panel width and chart height
)
pygame.display.set_caption("Wolf, Rabbit, and Grass Simulation")

place_entities()

wolves, rabbits, grasses = draw_window(chart_height)

# Game loop
running = True
while running:
    time.sleep(1)  # Pause for 1 second to simulate the passage of time
    month += 1  # Increment the month
    wolves, rabbits, grasses = draw_window(chart_height)

    # Process all Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

pygame.quit()
