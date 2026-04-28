import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import (
    LINE_WIDTH, 
    ASTEROID_MIN_RADIUS, 
    SCREEN_WIDTH,
    SCREEN_HEIGHT
    )

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

        # Check left wall
        if self.position.x - self.radius < 0:
            self.velocity.x *= -1
            self.position.x = self.radius # Teleports asteroid safely inside boundary
        
        # Check right wall
        elif self.position.x + self.radius > SCREEN_WIDTH:
            self.velocity.x *= -1
            self.position.x = SCREEN_WIDTH - self.radius
        
        # Check top wall
        if self.position.y - self.radius < 0:
            self.velocity.y *= -1
            self.position.y = self.radius
        
        # Check bottom wall
        elif self.position.y + self.radius > SCREEN_HEIGHT:
            self.velocity.y *= -1
            self.position.y = SCREEN_HEIGHT - self.radius

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        positive = self.velocity.rotate(angle)
        negative = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = positive * 1.2
        asteroid2.velocity = negative * 1.2