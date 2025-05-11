import pygame
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = PLAYER_SPEED

    def update(self, keys, collision_mask):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        new_rect = self.rect.move(dx, dy)

        points_to_check = [
            new_rect.topleft,
            new_rect.topright,
            new_rect.bottomleft,
            new_rect.bottomright,
            new_rect.center,
        ]

        valid = True
        for point in points_to_check:
            x, y = point
            if not (0 <= x < collision_mask.get_size()[0] and 0 <= y < collision_mask.get_size()[1]):
                valid = False
                break
            if not collision_mask.get_at((x, y)):
                valid = False
                break

        if valid:
            self.rect = new_rect
