import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 200  # Size of the grid
CELL_SIZE = 6  # Pixel size of each cell
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE  # Window size
FPS = 10  # Frames per second, controls the speed of the simulation

# Colors (Black and White)
ALIVE_COLOR = (0, 0, 0)  # Black for alive cells
DEAD_COLOR = (255, 255, 255)  # White for dead cells

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cellular Automaton")

# Initialize the grid
grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.8, 0.2])


def update_grid(grid):
    new_grid = grid.copy()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Get the sum of the neighbors
            total = (
                grid[i, (j - 1) % GRID_SIZE]
                + grid[i, (j + 1) % GRID_SIZE]
                + grid[(i - 1) % GRID_SIZE, j]
                + grid[(i + 1) % GRID_SIZE, j]
                + grid[(i - 1) % GRID_SIZE, (j - 1) % GRID_SIZE]
                + grid[(i - 1) % GRID_SIZE, (j + 1) % GRID_SIZE]
                + grid[(i + 1) % GRID_SIZE, (j - 1) % GRID_SIZE]
                + grid[(i + 1) % GRID_SIZE, (j + 1) % GRID_SIZE]
            )

            # Apply the Game of Life rules
            if grid[i, j] == 1:  # Cell is currently alive
                if total < 2 or total > 3:
                    new_grid[i, j] = 0  # Cell dies
            else:  # Cell is currently dead
                if total == 3:
                    new_grid[i, j] = 1  # Cell becomes alive

    return new_grid


def draw_grid(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = ALIVE_COLOR if grid[i, j] == 1 else DEAD_COLOR
            pygame.draw.rect(
                screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )


def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(DEAD_COLOR)  # Fill the screen with white (background)

        # Handle events (close the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the grid based on the Game of Life rules
        grid[:] = update_grid(grid)

        # Draw the grid
        draw_grid(grid)

        # Update the screen
        pygame.display.flip()

        # Control the speed of the simulation
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
