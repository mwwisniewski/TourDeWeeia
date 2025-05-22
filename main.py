import pygame
import sys
from sprites import *
from config import *
from menu import *
from gamelogic import RaceManager


class Game:
    def __init__(self):
        pygame.init()

        temp_screen = pygame.display.set_mode((1, 1))

        self.bg_image = pygame.image.load("img/wejscie weeia i parter.png").convert()
        self.collision_mask_image = pygame.image.load("img/wejscie weeia i parter_maska.png").convert()
        self.collision_mask_image.set_colorkey((255, 255, 255))
        self.collision_mask = pygame.mask.from_threshold(
            self.collision_mask_image,
            (0, 0, 0),
            (50, 50, 50) #pol czarny pol nie bo cos sie buguje xdd
        )
        #mapa
        self.MAP_WIDTH, self.MAP_HEIGHT = self.bg_image.get_size()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tour de Weeia")

        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = pygame.Vector2(0, 0)
        self.all_sprites = pygame.sprite.Group()
        #zoom
        self.zoom = 2

        #game logic
        self.player1=Player(0,0,CONTROL_TYPE_WSAD)#spawnpointy losowac
        self.player2=Player(0,0,CONTROL_TYPE_ARROWS)
        #self.all_sprites.add(self.player1) dorobic sprite
        #self.all_sprites.add(self.player2)
        goal_rect = pygame.Rect(0,0,0,0)  # miejsce do którego trzeba dotrzeć
        self.race = RaceManager(self.player1, self.player2, goal_rect)
        self.race.start_round()



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
        ########
        keys = pygame.key.get_pressed()
        # Gracz 1: W, S, A, D
        self.player1.update(keys, self.collision_mask,
                            up=pygame.K_w,down=pygame.K_s, left=pygame.K_a,right=pygame.K_d)
        # Gracz 2: strzałki
        self.player2.update(keys, self.collision_mask,
                            up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT,right=pygame.K_RIGHT)


        self.camera_offset.x = self.player1.rect.centerx - self.WIDTH // 2
        self.camera_offset.y = self.player1.rect.centery - self.HEIGHT // 2

        self.race.update()

    def draw(self):
        self.screen.fill((255, 255, 255))

        scaled_bg = pygame.transform.smoothscale(
            self.bg_image,
            (int(self.MAP_WIDTH * self.zoom), int(self.MAP_HEIGHT * self.zoom))
        )

        player_center = self.player.rect.center
        self.camera_offset.x = player_center[0] * self.zoom - self.WIDTH // 2
        self.camera_offset.y = player_center[1] * self.zoom - self.HEIGHT // 2
        self.screen.blit(scaled_bg, (-self.camera_offset.x, -self.camera_offset.y))

        for sprite in self.all_sprites:
            scaled_pos = pygame.Vector2(sprite.rect.topleft) * self.zoom - self.camera_offset
            scaled_img = pygame.transform.smoothscale(
                sprite.image,
                (int(sprite.rect.width * self.zoom), int(sprite.rect.height * self.zoom))
            )
            self.screen.blit(scaled_img, scaled_pos)

        pygame.display.flip()

    def intro_screen(self):
        intro = True

        def start_game():
            nonlocal intro
            self.all_sprites = pygame.sprite.Group()
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
