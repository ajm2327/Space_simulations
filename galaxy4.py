import pygame
import math
import random
import colorsys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vibrant Galaxy with Seamless Glowing Core")

# Colors
BLACK = (0, 0, 0)

# Function to create a smoother radial gradient surface with extended fade
def create_smooth_radial_gradient(size, inner_color, outer_color):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 2

    for y in range(size[1]):
        for x in range(size[0]):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            if distance < radius:
                # Use a custom easing function for even smoother transition
                ratio = (distance / radius) ** 1.5  # Adjusted power for smoother fade
                color = [int(ic * (1 - ratio) + oc * ratio) for ic, oc in zip(inner_color, outer_color)]
                
                # Additional fade to black at the edges
                edge_fade = max(0, min(1, (radius - distance) / (radius * 0.2)))
                color = [int(c * edge_fade) for c in color]
                
                surface.set_at((x, y), color)

    return surface

# Star class (unchanged from previous version)
class Star:
    def __init__(self):
        self.distance = random.uniform(0, 400)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 0.001 * (1 - self.distance / 500)**0.5
        self.size = random.uniform(0.5, 2.5)
        self.hue = random.uniform(0, 1)
        self.brightness = random.uniform(0.5, 1.0)
        self.z = random.uniform(-50, 50)
        self.update_position()

    def update_position(self):
        a = 1000
        b = 12000
        x = math.cos(self.angle) * a * (self.distance / 400)
        y = math.sin(self.angle) * b * (self.distance / 400)
        perspective = 1000 / (1000 + self.z)
        self.x = x * perspective + width / 2
        self.y = y * perspective + height / 2

    def move(self):
        self.angle += self.speed
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        self.update_position()

    def draw(self):
        saturation = 1 - (self.distance / 800)**2
        value = self.brightness * (1 - (self.distance / 800)**2)
        rgb = colorsys.hsv_to_rgb(self.hue, saturation, value)
        color = [int(255 * c) for c in rgb]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size * (1 - self.distance / 800)**0.5))

# Create stars
stars = [Star() for _ in range(25000)]

# Create the glowing core gradient
core_radius = 250  # Increased radius for more gradual fade
core_surface = create_smooth_radial_gradient(
    (core_radius*2, core_radius*2),
    (255, 255, 200, 255),  # Inner color (bright, slightly yellow)
    (20, 20, 40, 0)        # Outer color (very dark blue, fully transparent)
)

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

    # Sort and draw stars
    stars.sort(key=lambda star: star.z, reverse=True)
    for star in stars:
        star.move()
        star.draw()

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
