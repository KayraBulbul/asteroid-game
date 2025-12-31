import player
import pygame
import time
from constants import COLLIDE_COOLDOWN


last_collide = 0


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        if distance <= self.radius + other.radius:
            return True
        return False

    def collides_with_player(self, other):
        global last_collide
        current_time = time.time()
        distance = self.position.distance_to(other.position)
        if distance <= self.radius + other.radius:
            if current_time - last_collide >= COLLIDE_COOLDOWN:
                last_collide = current_time
                return True
            else:
                remaining_time = COLLIDE_COOLDOWN - (current_time - last_collide)
                print(f"Time remaining for immunity: {remaining_time}")
                return False
        return False
