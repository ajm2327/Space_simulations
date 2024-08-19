import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Saturn")

# Colors
BLACK = (0, 0, 0)
SATURN_BASE = (240, 180, 40)
SATURN_DARK = (200, 140, 20)
SATURN_LIGHT = (255, 220, 100)

# Saturn's properties
saturn_radius = 300 #larger radius
saturn_pos = (width // 2, height // 2)

def create_saturn_surface(radius):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for y in range(radius * 2+100): #changed here
        for x in range(radius * 2+100): #changed here
            distance = math.sqrt((x - radius) ** 2 + (y - radius) ** 2)
            if distance < radius:
                # Calculate the angle for shading
                angle = math.atan2(y - radius, x - radius)
                shade = (math.cos(angle) + 1) / 2  # Value between 0 and 1

                # Create base color with shading
                base_color = [
                    int(SATURN_DARK[i] + (SATURN_LIGHT[i] - SATURN_DARK[i]) * shade)
                    for i in range(3)
                ]

                # Add stripes
                stripe = math.sin(y / radius * 10) * 30
                color = [max(0, min(255, c + stripe)) for c in base_color]

                # Add alpha for a gradual fade-out near the edges
                alpha = int(255 * (1 - distance / radius) ** 0.5)
                surface.set_at((x, y), color + [alpha])

    return surface

# Create Saturn surface
saturn_surface = create_saturn_surface(saturn_radius)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw Saturn
    screen.blit(saturn_surface, (saturn_pos[0] - saturn_radius, saturn_pos[1] - saturn_radius))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
