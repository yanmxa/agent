import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 50
MAX_SPEED = 8  # Increased speed for faster movement
MAX_FORCE = 0.1
NUM_BOIDS = 100


class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = MAX_SPEED
        self.max_force = MAX_FORCE
        self.color = (255, 255, 255)

    def edges(self):
        """Wrap around the screen edges"""
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def update(self):
        """Update position and velocity"""
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration

    def apply_force(self, force):
        """Apply force to boid"""
        self.acceleration += force

    def limit(self, vector, max_value):
        """Limit a vector's magnitude"""
        if vector.length() > max_value:
            vector.scale_to_length(max_value)
        return vector

    def seek(self, target):
        """Seek the target position"""
        desired = target - self.position
        desired = self.limit(desired, self.max_speed)
        steer = desired - self.velocity
        steer = self.limit(steer, self.max_force)
        return steer

    def separation(self, boids):
        """Steer to avoid crowding local boids."""
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if distance < RADIUS and distance > 0:  # Avoid division by zero
                diff = self.position - boid.position
                diff /= distance  # Weight by distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
        if steering.length() > 0:
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def alignment(self, boids):
        """Steer towards the average velocity of local boids"""
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if self.position.distance_to(boid.position) < RADIUS:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = self.limit(steering, self.max_speed)
            steering -= self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def cohesion(self, boids):
        """Steer towards the average position of local boids"""
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if self.position.distance_to(boid.position) < RADIUS:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering = self.limit(steering, self.max_speed)
            steering -= self.velocity
            steering = self.limit(steering, self.max_force)
        return steering

    def flock(self, boids):
        """Update boid behavior based on flocking rules"""
        separation = self.separation(boids)
        alignment = self.alignment(boids)
        cohesion = self.cohesion(boids)

        # Apply forces
        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(cohesion)

    def draw(self, screen):
        """Draw boid on the screen as a triangle (bird-like)"""
        angle = math.atan2(self.velocity.y, self.velocity.x)
        points = [
            self.position
            + pygame.Vector2(0, -5).rotate(angle),  # Top of triangle (bird's head)
            self.position
            + pygame.Vector2(-5, 5).rotate(angle),  # Left side of triangle
            self.position
            + pygame.Vector2(5, 5).rotate(angle),  # Right side of triangle
        ]
        pygame.draw.polygon(screen, self.color, points)


def draw_gradient_background(screen):
    """Draw a gradient background that simulates a sky effect."""
    for i in range(HEIGHT):
        # Gradually changing from dark blue at the top to lighter blue at the bottom
        r = min(max(100 + (i // 5), 0), 255)  # Red channel (starting darker at the top)
        g = min(max(140 + (i // 8), 0), 255)  # Green channel (slowly increasing)
        b = min(
            max(255 - (i // 3), 0), 255
        )  # Blue channel (lighter blue at the bottom)

        # Optional: add a hint of orange near the bottom to simulate sunset/dawn
        if i > HEIGHT * 0.7:
            r = min(max(255 - (i // 3), 0), 255)  # Add some red near the bottom
            g = min(
                max(140 + (i // 10), 0), 255
            )  # Slightly more yellowish near the bottom
            b = min(max(220 - (i // 6), 0), 255)  # A bit less blue to simulate sunset

        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")

    boids = [
        Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        for _ in range(NUM_BOIDS)
    ]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black (gradient will cover this)
        draw_gradient_background(screen)  # Add gradient background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update boid behaviors
        for boid in boids:
            boid.flock(boids)  # Update boid behavior based on flocking rules
            boid.update()
            boid.edges()  # Handle screen wrapping
            boid.draw(screen)  # Draw boid on screen

        pygame.display.flip()  # Update screen
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
