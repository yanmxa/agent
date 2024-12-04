import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600  # Screen size
BACKGROUND_COLOR = (173, 216, 230)  # Light blue background
POINT_COLOR = (0, 255, 0)  # Green point (agent)
LINE_COLOR = (0, 0, 0)  # Black for function line
DERIVATIVE_COLOR = (255, 0, 0)  # Red for the derivative line
TEXT_COLOR = (0, 0, 0)  # Text color
AXIS_COLOR = (0, 0, 0)  # Axis color
LIGHT_GREEN = (144, 238, 144)  # Light green for x-value on the axis
GRAY_COLOR = (169, 169, 169)  # Gray color for connecting line

# Gradient Descent parameters
LEARNING_RATE = 0.1  # Learning rate (alpha)
START_X = 5  # Starting point of the gradient descent
MAX_ITER = 50  # Maximum iterations

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gradient Descent with Iteration Control")
clock = pygame.time.Clock()


# Function and its derivative
def f(x):
    return x**2 + 2 * x + 1  # f(x) = x^2 + 2x + 1


def df(x):
    return 2 * x + 2  # f'(x) = 2x + 2


# Plotting the quadratic function
def draw_function():
    points = []
    for x in np.linspace(-WIDTH // 2, WIDTH // 2, WIDTH):
        y = f(x / 50)  # Scale x for better display
        y = HEIGHT // 2 - y * 50  # Scale y to fit on screen and center it
        points.append((x + WIDTH // 2, y))

    pygame.draw.lines(screen, LINE_COLOR, False, points, 2)


# Plotting the derivative (slope) line
def draw_derivative(x):
    # Calculate the derivative (slope) at point x
    slope = df(x)

    # Draw the derivative line from the point (x, f(x)) in the direction of the slope
    x1 = x * 50 + WIDTH // 2  # Map the x coordinate to screen space
    y1 = HEIGHT // 2 - f(x) * 50  # Map the y coordinate to screen space

    # Calculate another point on the line based on the slope
    x2 = x1 + 100  # Move 100 pixels to the right
    y2 = y1 - slope * 100  # Calculate the corresponding y value based on the slope

    pygame.draw.line(screen, DERIVATIVE_COLOR, (x1, y1), (x2, y2), 2)


# Draw the point
def draw_point(x, y):
    pygame.draw.circle(
        screen, POINT_COLOR, (int(x + WIDTH // 2), int(HEIGHT // 2 - y * 50)), 5
    )


# Draw the coordinate axes
def draw_axes():
    # Draw x-axis and y-axis
    pygame.draw.line(
        screen, AXIS_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT)
    )  # y-axis
    pygame.draw.line(
        screen, AXIS_COLOR, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2)
    )  # x-axis

    # Mark the points on the axes
    font = pygame.font.Font(None, 24)
    for i in range(-10, 11):
        pygame.draw.circle(screen, AXIS_COLOR, (WIDTH // 2 + i * 50, HEIGHT // 2), 3)
        text = font.render(str(i), True, AXIS_COLOR)
        screen.blit(text, (WIDTH // 2 + i * 50 - 10, HEIGHT // 2 + 10))


# Gradient Descent Algorithm
def gradient_descent():
    x = START_X  # Starting point
    path = [x]

    for i in range(MAX_ITER):
        gradient = df(x)
        x = x - LEARNING_RATE * gradient  # Update rule for gradient descent
        path.append(x)

    return path


# Main loop
def main():
    running = True
    path = gradient_descent()  # Run gradient descent and get the path
    iteration = 0  # Start at the first iteration
    offset_y = 0  # To move the view downwards

    while running:
        screen.fill(BACKGROUND_COLOR)  # Light blue background

        # Draw coordinate axes
        draw_axes()

        draw_function()  # Draw the function graph

        if iteration < len(path):
            # Draw the current point
            draw_point(path[iteration], f(path[iteration]))

            # Draw the derivative line at the current position
            draw_derivative(path[iteration])

            # Draw a gray line connecting the current point's x with the x-axis
            pygame.draw.line(
                screen,
                GRAY_COLOR,
                (WIDTH // 2 + int(path[iteration] * 50), HEIGHT // 2),
                (
                    WIDTH // 2 + int(path[iteration] * 50),
                    HEIGHT // 2 - int(f(path[iteration]) * 50),
                ),
                2,
            )

        # Draw iteration number
        font = pygame.font.Font(None, 36)
        iteration_text = font.render(f"Iteration: {iteration + 1}", True, TEXT_COLOR)
        screen.blit(iteration_text, (10, 10))

        # Draw the values of x, y, and derivative below the iteration label
        small_font = pygame.font.Font(None, 24)

        # x value
        x_text = small_font.render(f"x: {path[iteration]:.4f}", True, TEXT_COLOR)
        screen.blit(x_text, (10, HEIGHT - 60))

        # y value
        y_text = small_font.render(f"y: {f(path[iteration]):.4f}", True, TEXT_COLOR)
        screen.blit(y_text, (10, HEIGHT - 40))

        # Derivative value
        derivative_text = small_font.render(
            f"f'(x): {df(path[iteration]):.4f}", True, TEXT_COLOR
        )
        screen.blit(derivative_text, (10, HEIGHT - 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Move to the next iteration when spacebar is pressed
                    if iteration < len(path) - 1:
                        iteration += 1

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Set the speed of the loop (frames per second)

    pygame.quit()


if __name__ == "__main__":
    main()
