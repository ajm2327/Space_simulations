import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vibrant Galaxy Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 100, 100), (255, 150, 100), (255, 200, 100),  # Reds and oranges
    (100, 255, 100), (100, 255, 150), (100, 255, 200),  # Greens
    (100, 100, 255), (150, 100, 255), (200, 100, 255),  # Blues and purples
    (255, 255, 100), (255, 100, 255), (100, 255, 255),   # Bright yellows and magentas
    (255, 255, 255), (200, 200, 200), (230, 230, 245)
]

# Star class
class Star:
    def __init__(self, distance, angle, speed, size, color, brightness, z):
        self.distance = distance
        self.angle = angle
        self.speed = speed
        self.size = size
        self.color = color
        self.brightness = brightness
        self.z = z  # For 3D effect
        self.update_position()

    @classmethod
    def create_random_star(cls):
        distance = random.uniform(0, 800)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.0005, 0.002) * (1 - distance / 500)  
        size = random.uniform(0.5, 2.5)
        color = random.choice(COLORS)
        brightness = random.uniform(0.5, 1.0)
        z = random.uniform(-50, 50)  
        return cls(distance, angle, speed, size, color, brightness, z)
        
 
    def update_position(self):
        # Elliptical orbit params
        a = 8000  # Semi-major axis
        b = 500  # Semi-minor axis
        x = math.cos(self.angle) * a * (self.distance / 400)
        y = math.sin(self.angle) * b * (self.distance / 400)       
 
        # Apply perspective transformation
        perspective = 1000 / (1000 + self.z)
        self.x = x * perspective + SCREEN_WIDTH / 2
        self.y = y * perspective + SCREEN_HEIGHT / 2

    def move(self):
        self.angle += self.speed
        self.angle %= 2 * math.pi  # Improvement: Using modulo to wrap around the angle
        self.update_position()

    def draw(self):
        # Adjust color based on distance from center
        color = [int(c * self.brightness * (1 - self.distance / 800)) for c in self.color]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size * (1 - self.distance / 800)))
 

# Galactic Core class (new feature)
class GalacticCore:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.update_position()
        
    @classmethod
    def create_default_core(cls):
        return cls(10, [255, 255, 200])
        
    def update_position(self, center_x=SCREEN_WIDTH//2, center_y=SCREEN_HEIGHT//2):
        self.center = (center_x, center_y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
        
    def pulse(self):  # New method to add a pulsing effect to the core
        self.radius = 10 + 5 * math.sin(pygame.time.get_ticks() * 0.001)
        self.update_position()
 

# Create stars
stars = [Star.create_random_star() for _ in range(30000)]

# Create the Galactic Core (new instance)
galactic_core = GalacticCore.create_default_core()

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

    # Draw the galactic core (using the new class)
    galactic_core.draw()
    galactic_core.pulse()  # Call the new method to add pulsing effect


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()