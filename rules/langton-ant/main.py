import pygame
import sys

# Directions: 0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]  # (dy, dx) corresponding to (up, right, down, left)


class LangtonsAnt:
    def __init__(self, grid_size=150, max_steps=11000, cell_size=8):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = [
            [True] * grid_size for _ in range(grid_size)
        ]  # True for white, False for black
        self.x = grid_size // 2  # Start at the center of the grid
        self.y = grid_size // 2
        self.direction = (
            0  # Start facing up (0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left)
        )
        self.steps = 0
        self.max_steps = max_steps

    def turn(self, clockwise=True):
        """Turn the ant 90 degrees clockwise or counterclockwise."""
        if clockwise:
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4

    def move(self):
        """Move the ant forward one step."""
        dy, dx = DIRECTIONS[self.direction]
        self.x += dx
        self.y += dy

    def simulate(self):
        """Simulate Langton's Ant for a given number of steps."""
        if self.steps < self.max_steps:
            if self.grid[self.y][self.x]:  # White square
                self.turn(clockwise=True)
                self.grid[self.y][self.x] = False  # Flip the square to black
            else:  # Black square
                self.turn(clockwise=False)
                self.grid[self.y][self.x] = True  # Flip the square to white

            self.move()  # Move the ant
            self.steps += 1
            return True
        return False

    def get_state(self):
        """Return the current state of the simulation."""
        return {
            "position": (self.x, self.y),
            "direction": self.direction,
            "steps": self.steps,
            "grid": self.grid,
        }


def draw_grid(screen, ant, grid_size, cell_size):
    """Draw the grid on the Pygame window without borders."""
    for row in range(grid_size):
        for col in range(grid_size):
            color = (
                (255, 255, 255) if ant.grid[row][col] else (0, 0, 0)
            )  # White for True, Black for False
            pygame.draw.rect(
                screen, color, (col * cell_size, row * cell_size, cell_size, cell_size)
            )


def draw_ant(screen, ant, cell_size):
    """Draw the ant on the Pygame window with a more refined design."""
    ant_x, ant_y = ant.x, ant.y
    # Draw a circle for the ant
    pygame.draw.circle(
        screen,
        (255, 0, 0),  # Red color
        (ant_x * cell_size + cell_size // 2, ant_y * cell_size + cell_size // 2),
        cell_size // 3,
    )


def run_simulation():
    """Run the Langton's Ant simulation using Pygame."""
    pygame.init()

    # Define window size that fits well on a Mac screen
    grid_size = 150  # Size of the grid (larger grid to make it wider)
    cell_size = 8  # Size of each cell (a bit larger for better visuals)
    max_steps = 15000  # Number of steps for the simulation

    # Calculate screen size based on grid size and cell size
    screen_width = grid_size * cell_size
    screen_height = grid_size * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Langton's Ant Simulation")

    # Set up fonts for displaying stats
    font = pygame.font.SysFont("Arial", 24)

    ant = LangtonsAnt(grid_size, max_steps, cell_size)

    clock = pygame.time.Clock()
    running = True
    simulation_running = True

    while running:
        screen.fill((220, 220, 220))  # Light grey background for a refined look

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = (
                        not simulation_running
                    )  # Pause/Resume simulation

        # Draw the grid and the ant
        draw_grid(screen, ant, grid_size, cell_size)
        draw_ant(screen, ant, cell_size)

        # Simulate one step if the simulation is running
        if simulation_running:
            if not ant.simulate():  # Stop if max steps are reached
                simulation_running = False

        # Display simulation stats (steps)
        steps_text = font.render(f"Steps: {ant.steps}", True, (0, 0, 0))
        screen.blit(steps_text, (10, 10))

        # Update the screen and control the simulation speed
        pygame.display.flip()
        clock.tick(30)  # Control the simulation speed (30 FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_simulation()
