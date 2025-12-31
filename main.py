from math import log
import pygame
import os
import json
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0

    HIGHSCORE = "highscore.json"

    def load_highscore():
        if os.path.exists(HIGHSCORE):
            with open(HIGHSCORE, "r") as highscore:
                data = json.load(highscore)
                return data.get("score", 0)
        return 0

    def save_highscore(score):
        with open(HIGHSCORE, "w") as highscore:
            json.dump({"score": score}, highscore)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroidfield = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        highscore = load_highscore()

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    log_event("Score increase")
                    score += 10
                    if highscore < score:
                        save_highscore(score)
                    shot.kill()
                    asteroid.split()
        for obj in asteroids:
            if obj.collides_with(player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        screen.fill("black")
        score_surface = font.render(f"Score: {score}", True, "white")
        highscore_surface = font.render(f"Highscore: {highscore}", True, "white")
        screen.blit(score_surface, (10, 10))
        screen.blit(highscore_surface, (10, 50))

        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
