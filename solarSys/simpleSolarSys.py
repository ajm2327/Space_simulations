import pygame
import math
from pygame.math import Vector2
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 800
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Accurate Solar System Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Scaling factors
DISTANCE_SCALE = 250 / 30  # 250 pixels = 30 AU
SIZE_SCALE = 5  # Exaggerate size for visibility

# Celestial body data: name, distance from Sun (AU), radius (km), orbital period (years)
bodies = [
    ("Sun", 0, 696340, 0),
    ("Mercury", 0.39, 2440, 0.24),
    ("Venus", 0.72, 6052, 0.62),
    ("Earth", 1, 6371, 1),
    ("Mars", 1.52, 3390, 1.88),
    ("Jupiter", 5.20, 69911, 11.86),
    ("Saturn", 9.54, 58232, 29.46),
    ("Uranus", 19.19, 25362, 84.01),
    ("Neptune", 30.07, 24622, 164.79)
]

# Kuiper Belt
kuiper_belt_objects = [
    (random.uniform(30, 50), random.uniform(0, 2*math.pi), random.uniform(0.001, 0.1))
    for _ in range(1000)
]

def draw_body(surface, position, radius, color):
    pygame.draw.circle(surface, color, position, max(int(radius), 1))

def calculate_position(distance, angle):
    x = width / 2 + distance * math.cos(angle)
    y = height / 2 + distance * math.sin(angle)
    return Vector2(x, y)

# Main simulation loop
clock = pygame.time.Clock()
running = True
simulation_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    display.fill(BLACK)

    # Draw celestial bodies
    for name, distance, radius, period in bodies:
        if period == 0:  # Sun
            position = Vector2(width / 2, height / 2)
        else:
            angle = (simulation_time / period) * 2 * math.pi
            distance_pixels = distance * DISTANCE_SCALE
            position = calculate_position(distance_pixels, angle)

        radius_pixels = (radius / 69911) * SIZE_SCALE  # Scale relative to Jupiter
        color = YELLOW if name == "Sun" else WHITE
        draw_body(display, position, radius_pixels, color)

    # Draw Kuiper Belt objects
    for distance, initial_angle, size in kuiper_belt_objects:
        angle = initial_angle + (simulation_time / 200) * 2 * math.pi
        distance_pixels = distance * DISTANCE_SCALE
        position = calculate_position(distance_pixels, angle)
        draw_body(display, position, 1, WHITE)

    # Update display
    pygame.display.flip()

    # Increment simulation time (each frame represents 0.1 Earth years)
    simulation_time += 0.1

    # Control frame rate
    clock.tick(60)

pygame.quit()
