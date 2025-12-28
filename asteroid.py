import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)

        new_asteroid_velocity1 = self.velocity.rotate(angle)
        new_asteroid_velocity2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
        new_asteroid2 = Asteroid(self.position[0], self.position[1], new_radius)

        new_asteroid1.velocity = new_asteroid_velocity1 * 1.2
        new_asteroid2.velocity = new_asteroid_velocity2 * 1.2
