import time

import pygame
from config import *



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = PLAYER_SPEED
        self.posX, self.posY = x, y
        self.freeze_until = 0
        self.control =True
        self.auto_target = None
        self.broken_leg = False
        self.on_reach_target = None
        self.current_goal = None

        #self.currentEvent



    def update(self, keys, collision_mask):
        if pygame.time.get_ticks() < self.freeze_until:
            return #mozna zrobic tak ze gracz nie chodzi ale zmienia sie kierunek sprite

        if not self.control and self.auto_target:
            direction = self.auto_target - pygame.Vector2(self.rect.center)
            distance = direction.length()
            if distance < self.speed:
                self.rect.center = self.auto_target
                self.auto_target = None
                self.control = True
                if self.on_reach_target:
                    self.on_reach_target()
                    self.on_reach_target = None
            else:
                direction = direction.normalize()
                dx = direction.x * self.speed
                dy = direction.y * self.speed
                new_rect = self.rect.move(dx, dy)

                # kolizje – te same co przy normalnym ruchu
                points_to_check = [
                    new_rect.topleft,
                    new_rect.topright,
                    new_rect.bottomleft,
                    new_rect.bottomright,
                    new_rect.center,
                ]

                valid = all(
                    0 <= x < collision_mask.get_size()[0] and
                    0 <= y < collision_mask.get_size()[1] and
                    collision_mask.get_at((x, y))
                    for x, y in points_to_check
                )
                if valid:
                    self.rect = new_rect
            return

        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed
        self.posX += dx
        self.posY += dy

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

    def freeze(self, duration_ms):
        self.freeze_until = pygame.time.get_ticks() + duration_ms

    def forceMove(self,x,y):
        self.auto_target = pygame.Vector2(x, y)
        self.control = False  # wylącz kontrole gracza


