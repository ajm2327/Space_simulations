import pygame
import math
import random
import colorsys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vibrant Galaxy with Glowing Core")

# Colors
BLACK = (0, 0, 0)

# Function to create a radial gradient surface
def create_radial_gradient(size, color1, color2):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 2
    for y in range(size[1]):
        for x in range(size[0]):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            if distance < radius:
                ratio = distance / radius
                color = [int(c1 * (1 - ratio) + c2 * ratio) for c1, c2 in zip(color1, color2)]
                surface.set_at((x, y), color)
    return surface

# Star class
class Star:
    def __init__(self):
        self.distance = random.uniform(0, 400)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 0.001 * (1 - self.distance / 500)**0.5  # Slower at the edges, smoother transition
        self.size = random.uniform(0.5, 2.5)
        self.hue = random.uniform(0, 1)  # Use HSV color space for smoother color transitions
        self.brightness = random.uniform(0.5, 1.0)
        self.z = random.uniform(-50, 50)  # For 3D effect
        self.update_position()

    def update_position(self):
        # Elliptical orbit
        a = 400  # Semi-major axis
        b = 300  # Semi-minor axis
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
        # Calculate color based on distance from center
        saturation = 1 - (self.distance / 800)**2  # More saturated in the center
        value = self.brightness * (1 - (self.distance / 800)**2)  # Brighter in the center
        rgb = colorsys.hsv_to_rgb(self.hue, saturation, value)
        color = [int(255 * c) for c in rgb]
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size * (1 - self.distance / 800)**0.5))

# Create stars
stars = [Star() for _ in range(15000)]

# Create the glowing core gradient
core_radius = 150
core_surface = create_radial_gradient((core_radius*2, core_radius*2), (255, 255, 200, 255), (255, 255, 200, 0))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the glowing core
    screen.blit(core_surface, (width//2 - core_radius, height//2 - core_radius), special_flags=pygame.BLEND_ADD)

    # Sort stars by z-index for proper layering
    stars.sort(key=lambda star: star.z, reverse=True)

    # Update and draw stars
    for star in stars:
        star.move()
        star.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
