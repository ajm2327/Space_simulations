import pygame
import math
import random
from pygame.math import Vector3

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1920, 1080
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Solar System Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Camera settings
camera_pos = Vector3(0, 0, -500)
camera_rotation = Vector3(0, 0, 0)

# Planet data: name, radius, orbit_radius, orbit_speed, color, pattern
planets = [
    ("Sun", 50, 0, 0, (255, 255, 0), "sun"),
    ("Mercury", 10, 100, 0.02, (169, 169, 169), "rocky"),
    ("Venus", 15, 150, 0.015, (255, 198, 73), "cloudy"),
    ("Earth", 16, 200, 0.01, (100, 149, 237), "earth"),
    ("Mars", 12, 250, 0.008, (255, 69, 0), "rocky"),
    ("Jupiter", 35, 350, 0.005, (255, 165, 0), "gas_giant"),
    ("Saturn", 30, 450, 0.004, (210, 180, 140), "ringed"),
    ("Uranus", 25, 550, 0.003, (173, 216, 230), "ice_giant"),
    ("Neptune", 24, 650, 0.002, (0, 0, 255), "ice_giant")
]

# Kuiper Belt
kuiper_belt_objects = [(random.uniform(700, 1000), random.uniform(0, 2*math.pi), random.uniform(5, 10), random.uniform(0.0005, 0.002), random.uniform(0,2*math.pi)) for _ in range(1000)]


def rotate_point(point, rotation):
    x, y, z = point
    rx, ry, rz = rotation
    
    # Rotate around X-axis
    y = y * math.cos(rx) - z * math.sin(rx)
    z = y * math.sin(rx) + z * math.cos(rx)
    
    # Rotate around Y-axis
    x = x * math.cos(ry) + z * math.sin(ry)
    z = -x * math.sin(ry) + z * math.cos(ry)
    
    # Rotate around Z-axis
    x = x * math.cos(rz) - y * math.sin(rz)
    y = x * math.sin(rz) + y * math.cos(rz)
    
    return Vector3(x, y, z)

def project_point(point):
    x, y, z = point - camera_pos
    factor = 200 / (z + 200)
    x, y = x * factor, y * factor
    return int(width/2 + x), int(height/2 - y)

def draw_sphere(surface, center, radius, color, pattern):
    x, y = center
    
    if pattern == "sun":
        pygame.draw.circle(surface, color, (x, y), radius)
        for _ in range(20):
            angle = random.uniform(0, 2*math.pi)
            length = random.uniform(radius*0.8, radius*1.2)
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)
#            pygame.draw.line(surface, (255, 165, 0), (x, y), (end_x, end_y), 2)
    
    elif pattern == "rocky":
        pygame.draw.circle(surface, color, (x, y), radius)
        for _ in range(10):
            crater_x = x + random.uniform(-radius*0.7, radius*0.7)
            crater_y = y + random.uniform(-radius*0.7, radius*0.7)
            crater_radius = random.uniform(radius*0.1, radius*0.3)
            pygame.draw.circle(surface, (color[0]*0.8, color[1]*0.8, color[2]*0.8), (crater_x, crater_y), crater_radius)
    
    elif pattern == "cloudy":
        pygame.draw.circle(surface, color, (x, y), radius)
        for _ in range(5):
            cloud_x = x + random.uniform(-radius*0.7, radius*0.7)
            cloud_y = y + random.uniform(-radius*0.7, radius*0.7)
            cloud_radius = random.uniform(radius*0.2, radius*0.4)
            pygame.draw.circle(surface, (255, 255, 255), (cloud_x, cloud_y), cloud_radius)
    
    elif pattern == "earth":
        pygame.draw.circle(surface, color, (x, y), radius)
        for _ in range(3):
            continent_x = x + random.uniform(-radius*0.7, radius*0.7)
            continent_y = y + random.uniform(-radius*0.7, radius*0.7)
            continent_radius = random.uniform(radius*0.3, radius*0.5)
            pygame.draw.circle(surface, (0, 128, 0), (continent_x, continent_y), continent_radius)
    
    elif pattern == "gas_giant":
        pygame.draw.circle(surface, color, (x, y), radius)
        for i in range(5):
            band_y = y - radius + (2 * radius * i) // 5
            band_height = radius // 3
            pygame.draw.ellipse(surface, (color[0]*0.8, color[1]*0.8, color[2]*0.8), (x-radius, band_y, 2*radius, band_height))
    
    elif pattern == "ringed":
        pygame.draw.circle(surface, color, (x, y), radius)
        pygame.draw.ellipse(surface, (210, 180, 140), (x-radius*1.5, y-radius//4, 3*radius, radius//2))
        pygame.draw.ellipse(surface, BLACK, (x-radius*1.5, y-radius//4, 3*radius, radius//2), 1)
    
    elif pattern == "ice_giant":
        pygame.draw.circle(surface, color, (x, y), radius)
        for _ in range(20):
            streak_x = x + random.uniform(-radius, radius)
            streak_y = y + random.uniform(-radius, radius)
            streak_length = random.uniform(radius*0.5, radius*1.5)
            streak_angle = random.uniform(0, 2*math.pi)
            end_x = streak_x + streak_length * math.cos(streak_angle)
            end_y = streak_y + streak_length * math.sin(streak_angle)
#            pygame.draw.line(surface, (255, 255, 255), (streak_x, streak_y), (end_x, end_y), 1)

# Main game loop
clock = pygame.time.Clock()
running = True
time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    display.fill(BLACK)
    
    # Update camera rotation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_rotation.y -= 0.02
    if keys[pygame.K_RIGHT]:
        camera_rotation.y += 0.02
    if keys[pygame.K_UP]:
        camera_rotation.x -= 0.02
    if keys[pygame.K_DOWN]:
        camera_rotation.x += 0.02
    
    # Draw planets
    for name, radius, orbit_radius, orbit_speed, color, pattern in planets:
        angle = time * orbit_speed
        position = Vector3(
            orbit_radius * math.cos(angle),
            0,
            orbit_radius * math.sin(angle)
        )
        rotated_position = rotate_point(position, camera_rotation)
        projected_position = project_point(rotated_position)
        
        # Calculate size based on distance from camera
        distance = rotated_position.magnitude()
        size = int(radius * 400 / (distance + 400))
        
        draw_sphere(display, projected_position, size, color, pattern)
    
    # Draw Kuiper Belt objects
    for orbit_radius, initial_angle, size, orbit_speed, vertical_offset in kuiper_belt_objects:
        angle = initial_angle + time * orbit_speed
        vertical_position = math.sin(time + vertical_offset) * 1
        position = Vector3(
            orbit_radius * math.cos(angle),
            vertical_position * 3,
            orbit_radius * math.sin(angle)
        )
        rotated_position = rotate_point(position, camera_rotation)
        projected_position = project_point(rotated_position)
        
        pygame.draw.circle(display, (169, 169, 169), projected_position , 1)
     
    
    # Update display
    pygame.display.flip()
    
    # Increment time
    time += 0.1
    
    # Control frame rate
    clock.tick(60)

pygame.quit()
