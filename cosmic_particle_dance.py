import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cosmic Particle Dance")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Particle class
class Particle:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.randint(1, 3)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        if self.x < 0 or self.x > width:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > height:
            self.angle = -self.angle

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create particles
particles = [Particle() for _ in range(200)]

# Wormhole parameters
wormhole_center = (width // 2, height // 2)
wormhole_radius = 100
wormhole_strength = 0.5

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Update and draw particles
    for particle in particles:
        # Apply wormhole effect
        dx = wormhole_center[0] - particle.x
        dy = wormhole_center[1] - particle.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < wormhole_radius:
            force = (wormhole_radius - distance) / wormhole_radius * wormhole_strength
            particle.x += dx * force
            particle.y += dy * force
        
        particle.move()
        particle.draw()

    # Draw wormhole
    pygame.draw.circle(screen, (50, 50, 50), wormhole_center, wormhole_radius)
    
    # Create spiral effect
    for i in range(0, 360, 10):
        angle = math.radians(i)
        x = wormhole_center[0] + int(math.cos(angle) * wormhole_radius)
        y = wormhole_center[1] + int(math.sin(angle) * wormhole_radius)
        color = (min(255, 100 + i // 2), min(255, 100 + i // 2), min(255, 100 + i // 2))
        pygame.draw.line(screen, color, wormhole_center, (x, y), 2)

    # Draw pulsating rings
    for i in range(3):
        radius = wormhole_radius + 20 * i + int(math.sin(pygame.time.get_ticks() * 0.005 + i) * 10)
        pygame.draw.circle(screen, (100, 100, 100), wormhole_center, radius, 1)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
