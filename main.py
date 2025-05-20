import sys
from sprites import *
from config import *
from menu import *
from map_config import MapConfig


class Game:
    def __init__(self):
        self.MAP_HEIGHT = None
        self.MAP_WIDTH = None
        pygame.init()

        pygame.display.set_mode((1, 1))

        self.map_config = MapConfig()
        self.current_map = None
        self.bg_image = None
        self.collision_mask = None

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tour de Weeia")

        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = pygame.Vector2(0, 0)
        self.all_sprites = pygame.sprite.Group()

    def load_map(self, map_obj):
        self.bg_image, self.collision_mask = map_obj.load()
        self.MAP_WIDTH, self.MAP_HEIGHT = self.bg_image.get_size()
        self.current_map = map_obj

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
        self.camera_offset.x = self.player.rect.centerx - self.WIDTH // 2
        self.camera_offset.y = self.player.rect.centery - self.HEIGHT // 2

    def draw(self):
        # czyszczenie tla po zalaczeniu gierki
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.bg_image, (-self.camera_offset.x, -self.camera_offset.y))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft - self.camera_offset)
        pygame.display.flip()

    def intro_screen(self):
        intro = True

        def start_game():
            nonlocal intro
            self.all_sprites = pygame.sprite.Group()
            wejscie_mapa = next(m for m in self.map_config.maps if m.name=="Korytarz na parterze")
            self.load_map(wejscie_mapa)
            self.player = Player(120, 100)
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
