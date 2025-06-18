import pygame
import config
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, control_type, color_or_path):
        super().__init__()
        self.control_type = control_type
        self.speed = config.PLAYER_SPEED
        self.rect = pygame.Rect(x, y, 28, 28)
        self.freeze_until = 0
        self.slowed_until = 0

        self.uses_sprites = isinstance(color_or_path, str)
        if self.uses_sprites:
            self.sprite_folder = color_or_path
            self.direction = "down"
            self.current_animation = "idle"
            self.load_sprites()
            self.animation_index = 0
            self.last_animation_update = pygame.time.get_ticks()
            self.image = self.sprites["idle_down"][0]
        else:
            self.image = pygame.Surface((28, 28))
            self.image.fill(color_or_path)

        self.rect = self.image.get_rect(topleft=(x, y))

    def load_sprites(self):
        self.sprites = {}
        for state in ["idle", "run"]:
            for direction in ["down", "up", "left", "right"]:
                frames = []
                for i in range(4):  # zakładamy idle_down_0.png ... idle_down_3.png
                    filename = f"{self.sprite_folder}/{state}_{direction}_{i}.png"
                    if os.path.isfile(filename):
                        img = pygame.image.load(filename).convert_alpha()
                        img = pygame.transform.scale(img, (35, 35)) # rozmiar sprite'a
                        frames.append(img)
                self.sprites[f"{state}_{direction}"] = frames

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > 150:  # zmień klatkę co 150ms
            self.animation_index = (self.animation_index + 1) % len(
                self.sprites[f"{self.current_animation}_{self.direction}"])
            self.last_animation_update = now
        self.image = self.sprites[f"{self.current_animation}_{self.direction}"][self.animation_index]

    def update(self, keys, collision_mask):
        now = pygame.time.get_ticks()
        if now < self.freeze_until:
            return
        if now > self.slowed_until:
            self.speed = config.PLAYER_SPEED

        dx, dy = 0, 0

        if self.control_type == config.CONTROL_TYPE_WSAD:
            if keys[pygame.K_w]:
                dy -= self.speed
                self.direction = "up"
            if keys[pygame.K_s]:
                dy += self.speed
                self.direction = "down"
            if keys[pygame.K_a]:
                dx -= self.speed
                self.direction = "left"
            if keys[pygame.K_d]:
                dx += self.speed
                self.direction = "right"
        elif self.control_type == config.CONTROL_TYPE_ARROWS:
            if keys[pygame.K_UP]:
                dy -= self.speed
                if self.uses_sprites:
                    self.direction = "up"
            if keys[pygame.K_DOWN]:
                dy += self.speed
                if self.uses_sprites:
                    self.direction = "down"
            if keys[pygame.K_LEFT]:
                dx -= self.speed
                if self.uses_sprites:
                    self.direction = "left"
            if keys[pygame.K_RIGHT]:
                dx += self.speed
                if self.uses_sprites:
                    self.direction = "right"

        new_rect = self.rect.move(dx, dy)
        valid = all(
            0 <= x < collision_mask.get_size()[0] and
            0 <= y < collision_mask.get_size()[1] and
            collision_mask.get_at((x, y))
            for x, y in [
                new_rect.topleft,
                new_rect.topright,
                new_rect.bottomleft,
                new_rect.bottomright,
                new_rect.center
            ]
        )

        if valid:
            self.rect = new_rect
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.uses_sprites:
            self.update_animation()

    def freeze(self, duration_ms):
        self.freeze_until = pygame.time.get_ticks() + duration_ms

    def slow_until(self, duration_ms):
        self.slowed_until = pygame.time.get_ticks() + duration_ms

    def update_player_position(self, x, y):
        self.rect.topleft = (x, y)
