import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1800, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galactic Black Hole")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Star class
class Star:
    def __init__(self, x, y, size, speed, angle, spiral):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = angle
        self.spiral = spiral
        self.distance = math.sqrt((x - width/2)**2 + (y - height/2)**2)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))

    def move(self):
        # Move the star in a spiral pattern
        self.angle += self.speed
        self.distance -= self.speed / 10

        if self.distance < 5:
            self.reset()

        self.x = width/2 + math.cos(self.angle + self.spiral) * self.distance
        self.y = height/2 + math.sin(self.angle + self.spiral) * self.distance

    def reset(self):
        # Reset the star to the edge of the screen
        self.distance = math.sqrt((width/2)**2 + (height/2)**2)
        self.angle = random.uniform(0, 2*math.pi)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create stars
stars = []
for _ in range(500):
    x = random.randint(0, width)
    y = random.randint(0, height)
    size = random.randint(1, 3)
    speed = random.uniform(0.0001, 0.005)
    angle = random.uniform(0, 2*math.pi)
    spiral = random.choice([0, 2*math.pi/3, 4*math.pi/3])  # Three spiral arms
    stars.append(Star(x, y, size, speed, angle, spiral))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Update and draw stars
    for star in stars:
        star.move()
        star.draw()

    # Draw the black hole
    pygame.draw.circle(screen, (20, 20, 20), (width//2, height//2), 50)
    pygame.draw.circle(screen, (40, 40, 40), (width//2, height//2), 30)
    pygame.draw.circle(screen, (60, 60, 60), (width//2, height//2), 15)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
