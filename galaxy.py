import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vibrant Galaxy Animation")

# Colors
BLACK = (0, 0, 0)
COLORS = [
    (255, 100, 100), (255, 150, 100), (255, 200, 100),  # Reds and oranges
    (100, 255, 100), (100, 255, 150), (100, 255, 200),  # Greens
    (100, 100, 255), (150, 100, 255), (200, 100, 255),  # Blues and purples
    (255, 255, 100), (255, 100, 255), (100, 255, 255),   # Bright yellows and magentas
    (255, 255, 255), (200, 200, 200), (230, 230, 245)
]

# Star class
class Star:
    def __init__(self):
        self.distance = random.uniform(0, 800)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.0005, 0.002) * (1 - self.distance / 500)  # Slower at the edges
        self.size = random.uniform(0.5, 2.5)
        self.color = random.choice(COLORS)
        self.brightness = random.uniform(0.5, 1.0)
        self.z = random.uniform(-50, 50)  # For 3D effect
        self.update_position()

    def update_position(self):
        # Elliptical orbit
        a = 8000  # Semi-major axis
        b = 500  # Semi-minor axis
        x = math.cos(self.angle) * a * (self.distance / 400)
        y = math.sin(self.angle) * b * (self.distance / 400)
        
        # Apply perspective transformation
        perspective = 1000 / (1000 + self.z)
        self.x = x * perspective + width / 2
        self.y = y * perspective + height / 2

    def move(self):
        self.angle += self.speed
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        self.update_position()

    def draw(self):
        # Adjust color based on distance from center (brighter in center)
        color = [int(c * self.brightness * (1 - self.distance / 800)) for c in self.color]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size * (1 - self.distance / 800)))

# Create stars
stars = [Star() for _ in range(30000)]

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Sort stars by z-index for proper layering
    stars.sort(key=lambda star: star.z, reverse=True)

    # Update and draw stars
    for star in stars:
        star.move()
        star.draw()

    # Draw the galactic core
    pygame.draw.circle(screen, (255, 255, 200), (width // 2, height // 2), 20)
    pygame.draw.circle(screen, (255, 255, 150), (width // 2, height // 2), 15)
    pygame.draw.circle(screen, (255, 255, 100), (width // 2, height // 2), 10)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
