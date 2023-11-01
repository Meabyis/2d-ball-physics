import pygame
import sys
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
GRAVITY = 0.01
BOUNCE_FACTOR = -0.8
MIN_DISTANCE = 15  # Minimum distance between particles
SPRING_CONSTANT = 0.1  # Spring constant for the constraints

# Define a basic particle class
class Particle:
    def __init__(self, x, y, radius, mass):
        self.x, self.y = x, y
        self.radius = radius
        self.velocity = [0, 0]
        self.mass = mass

    def apply_force(self, force):
        acceleration = [force[0] / self.mass, force[1] / self.mass]
        self.velocity[0] += acceleration[0]
        self.velocity[1] += acceleration[1]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

# Calculate the distance between two particles
def distance(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx*dx + dy*dy)

# Apply spring-like forces to maintain minimum distance
def apply_constraints(particles):
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            dist = distance(particles[i], particles[j])
            if dist < MIN_DISTANCE:
                overlap = MIN_DISTANCE - dist
                angle = math.atan2(particles[j].y - particles[i].y, particles[j].x - particles[i].x)
                force = [overlap * SPRING_CONSTANT * math.cos(angle), overlap * SPRING_CONSTANT * math.sin(angle)]
                particles[i].apply_force(force)
                particles[j].apply_force([-force[0], -force[1]])

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Water Balloon")

# Create a list of particles (small balls)
particles = [
    Particle(400 + math.cos(angle) * 50, 300 + math.sin(angle) * 50, 10, 0.1)
    for angle in [i * (2 * math.pi / 12) for i in range(12)]  # Create 12 particles
]

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Apply gravity to all particles
    for particle in particles:
        particle.apply_force([0, GRAVITY])

    # Update the positions of all particles
    for particle in particles:
        particle.update()

    # Check for collisions with the ground
    for particle in particles:
        if particle.y + particle.radius > SCREEN_HEIGHT:
            # Bounce off the ground
            particle.y = SCREEN_HEIGHT - particle.radius
            particle.velocity[1] *= BOUNCE_FACTOR

    # Apply spring-like constraints to maintain minimum distance
    apply_constraints(particles)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw lines connecting particles
    for i in range(len(particles)):
        pygame.draw.aaline(screen, (0, 0, 255), (int(particles[i].x), int(particles[i].y)),
                         (int(particles[(i + 1) % len(particles)].x), int(particles[(i + 1) % len(particles)].y)))

    # Draw the particles (small balls)
    for particle in particles:
        pygame.draw.aaline(screen, (0, 0, 255), (int(particles[i].x), int(particles[i].y)), (int(particles[(i + 1) % len(particles)].x), int(particles[(i + 1) % len(particles)].y)))


    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS
