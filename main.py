import sys
import map_config
from sprites import *
from config import *
from menu import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        self.MAP_HEIGHT = None
        self.MAP_WIDTH = None

        self.game_map = map_config.create_main_map()
        self.bg_image, self.collision_mask = self.game_map.load()
        self.MAP_WIDTH, self.MAP_HEIGHT = self.bg_image.get_size()

        self.zoom = 2
        self.scaled_bg = pygame.transform.smoothscale(self.bg_image, (int(self.MAP_WIDTH * self.zoom),
                                                                      int(self.MAP_HEIGHT * self.zoom)))

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Tour de Weeia")

        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = pygame.Vector2(0, 0)
        self.all_sprites = pygame.sprite.Group()
        self.player = None  # Zeby pozbyc sie Unresolved reference
        self.debug_mode = True  # DO TESTOW POTEM ZMIENIC NA FALSE!! (POKAZUJE STREFY PRZEJSC,FPSY I INNE)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.collision_mask)
        self.camera_offset.x = (self.player.rect.centerx * self.zoom) - self.WIDTH // 2
        self.camera_offset.y = (self.player.rect.centery * self.zoom) - self.HEIGHT // 2

        for zone in self.game_map.transition_zones:
            if zone.rect.colliderect(self.player.rect):
                if self.debug_mode:
                    print(f"[PRZEJSCIE TEST] {zone.name} -> {zone.target_position}")
                self.player.rect.topleft = zone.target_position
                break

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.scaled_bg, (-self.camera_offset.x, -self.camera_offset.y))

        for sprite in self.all_sprites:
            scaled_pos = pygame.Vector2(sprite.rect.topleft) * self.zoom - self.camera_offset
            scaled_img = pygame.transform.smoothscale(
                sprite.image,
                (int(sprite.rect.width * self.zoom), int(sprite.rect.height * self.zoom))
            )
            self.screen.blit(scaled_img, scaled_pos)

        if self.debug_mode:
            for zone in self.game_map.transition_zones:
                debug_rect = zone.rect.copy()
                debug_rect.x *= self.zoom
                debug_rect.y *= self.zoom
                debug_rect.width *= self.zoom
                debug_rect.height *= self.zoom
                pygame.draw.rect(self.screen, (255, 0, 0), debug_rect.move(-self.camera_offset), 2)
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

        pygame.display.flip()

    def intro_screen(self):
        intro = True

        def start_game():
            nonlocal intro
            self.all_sprites = pygame.sprite.Group()
            spawn_x, spawn_y = self.game_map.get_random_spawn_point()
            self.player = Player(spawn_x, spawn_y)
            self.all_sprites.add(self.player)
            intro = False

        def open_settings():
            print("TODO")

        def quit_game():
            pygame.quit()
            sys.exit()

        menu_bg = pygame.image.load("img/logo.png").convert()
        menu_bg = pygame.transform.scale(menu_bg, (self.WIDTH, self.HEIGHT))

        button_width = 160
        button_height = 40
        button_x = self.WIDTH // 2 - button_width // 2
        button_y_start = self.HEIGHT // 2 + 100
        button_spacing = 60

        buttons = [
            Button("Start", button_x, button_y_start + 0 * button_spacing, button_width, button_height, start_game),
            Button("Ustawienia", button_x, button_y_start + 1 * button_spacing, button_width, button_height,
                   open_settings),
            Button("Wyjście", button_x, button_y_start + 2 * button_spacing, button_width, button_height, quit_game),
        ]

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                for button in buttons:
                    button.handle_event(event)

            self.screen.blit(menu_bg, (0, 0))
            for button in buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.intro_screen()
    game.run()
