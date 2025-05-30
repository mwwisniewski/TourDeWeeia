import random
import sys
import pygame
import map_config
from sprites import *
from config import *
from menu import *
from gamelogic import RaceManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        self.MAP_HEIGHT = None
        self.MAP_WIDTH = None

        self.game_map = map_config.create_main_map()
        self.current_target_room = None
        self.is_current_target_room= False
        self.bg_image, self.collision_mask = self.game_map.load()
        self.MAP_WIDTH, self.MAP_HEIGHT = self.bg_image.get_size()

        self.zoom = ZOOM
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
        self.player1 = None  # Zeby pozbyc sie Unresolved reference
        self.player2 = None
        self.debug_mode = DEBUG  # DO TESTOW POTEM ZMIENIC NA FALSE LUB NONE!! (POKAZUJE STREFY PRZEJSC, STREFY SAL ORAZ FPSY)
        self.printed_destination = True
        if self.debug_mode:
            self.printed_arrived = False
        #self.all_sprites.add(self.player1) dorobic sprite
        #self.all_sprites.add(self.player2)


    def intro_screen(self):
        intro = True

        def start_game():
            nonlocal intro
            self.all_sprites = pygame.sprite.Group()
            spawn_x1, spawn_y1 = self.game_map.get_random_spawn_point()
            spawn_x2, spawn_y2 = self.game_map.get_random_spawn_point()
            self.current_target_room = random.choice(self.game_map.target_rooms)
            self.is_current_target_room = True
            self.player1 = Player(spawn_x1, spawn_y1, CONTROL_TYPE_WSAD,RED)
            self.player2 = Player(spawn_x1, spawn_y1,CONTROL_TYPE_ARROWS,GREEN)
            self.all_sprites.add(self.player1)
            self.all_sprites.add(self.player2)
            self.race = RaceManager(self.player1, self.player2)


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

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            if not self.race.round_active and not self.race.game_over:
                if not self.is_current_target_room:
                    self.current_target_room = random.choice(self.game_map.target_rooms)
                    spawn_x1, spawn_y1 = self.game_map.get_random_spawn_point()
                    spawn_x2, spawn_y2 = self.game_map.get_random_spawn_point()
                    self.player1.random_spawn_point(spawn_x1, spawn_y1)
                    self.player2.random_spawn_point(spawn_x1, spawn_y1)

                self.is_current_target_room = False
                print(f"WYLOSOWANA SALA: {self.current_target_room.name}")
                self.race.start_round(self.current_target_room.rect)
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        # Gracz 1: W, S, A, D
        self.player1.update(keys, self.collision_mask)
        # Gracz 2: strzałki
        self.player2.update(keys, self.collision_mask)


        self.camera_offset.x = self.player1.rect.centerx - self.WIDTH // 2
        self.camera_offset.y = self.player1.rect.centery - self.HEIGHT // 2
        
        for zone in self.game_map.transition_zones:
            if zone.rect.colliderect(self.player1.rect):
                if self.debug_mode:
                    print(f"[PRZEJSCIE TEST] {zone.name} -> {zone.target_position}")
                self.player1.rect.topleft = zone.target_position
                break
        if self.debug_mode:
            if self.printed_arrived is False:
                if self.current_target_room.rect.colliderect(self.player1.rect):
                    print(f"TRAFILES DO SALI: {self.current_target_room.name}")
                    self.printed_arrived = True

        for zone in self.game_map.transition_zones:
            if zone.rect.colliderect(self.player2.rect):
                if self.debug_mode:
                    print(f"[PRZEJSCIE TEST] {zone.name} -> {zone.target_position}")
                self.player2.rect.topleft = zone.target_position
                break
        if self.debug_mode:
            if self.printed_arrived is False:
                if self.current_target_room.rect.colliderect(self.player2.rect):
                    print(f"TRAFILES DO SALI: {self.current_target_room.name}")
                    self.printed_arrived = True

                    
        self.race.update()
        

    def draw(self):
        self.screen.fill((255, 255, 255))

        player_center = self.player1.rect.center
        self.camera_offset.x = player_center[0] * self.zoom - self.WIDTH // 2
        self.camera_offset.y = player_center[1] * self.zoom - self.HEIGHT // 2
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
            for room in self.game_map.target_rooms:
                debug_rect = room.rect.copy()
                debug_rect.x *= self.zoom
                debug_rect.y *= self.zoom
                debug_rect.width *= self.zoom
                debug_rect.height *= self.zoom
                if room == self.current_target_room:
                    pygame.draw.rect(self.screen, (0, 255, 0), debug_rect.move(-self.camera_offset), 2)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 255), debug_rect.move(-self.camera_offset), 2)

            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

        pygame.display.flip()




if __name__ == "__main__":
    game = Game()
    game.intro_screen()
    game.run()
