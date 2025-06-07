import random
import sys
import pygame
import os
import map_config
from sprites import *
from config import *
from menu import *
from gamelogic import RaceManager
from menu import character_selection_screen
import debug_config


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_mode((1, 1))

        self.MAP_HEIGHT = None
        self.MAP_WIDTH = None

        self.game_map = map_config.create_main_map()
        self.current_target_room = None
        self.is_current_target_room = False
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
        self.camera_left_offset = pygame.Vector2(0, 0)
        self.camera_right_offset = pygame.Vector2(0, 0)
        self.left_view = pygame.Surface((self.WIDTH // 2, self.HEIGHT))
        self.right_view = pygame.Surface((self.WIDTH // 2, self.HEIGHT))
        self.all_sprites = pygame.sprite.Group()
        self.player1 = None  # Zeby pozbyc sie Unresolved reference
        self.player2 = None
        self.debug_mode = DEBUG  # DO TESTOW POTEM ZMIENIC NA FALSE LUB NONE!! (POKAZUJE STREFY PRZEJSC, STREFY SAL ORAZ FPSY)
        self.printed_destination = True
        if self.debug_mode:
            self.printed_arrived = False

        self.default_zone_name = "Nieznany obszar"
        self.player1_current_zone_name = self.default_zone_name
        self.player2_current_zone_name = self.default_zone_name
        self.zone_font = pygame.font.SysFont("arial", 20)
        self.zone_text_color = BLACK
        self.zone_text_bg = None

    def intro_screen(self):
        intro = True

        def start_game():
            nonlocal intro
            self.all_sprites = pygame.sprite.Group()

            selected_p1, selected_p2 = character_selection_screen(self.screen, self.WIDTH, self.clock)

            spawn_x1, spawn_y1 = self.game_map.get_random_spawn_point()
            spawn_x2, spawn_y2 = self.game_map.get_random_spawn_point()
            self.current_target_room = random.choice(self.game_map.target_rooms)
            self.is_current_target_room = True
            self.player1 = Player(spawn_x1, spawn_y1, CONTROL_TYPE_WSAD, selected_p1)
            self.player2 = Player(spawn_x2, spawn_y2, CONTROL_TYPE_ARROWS, selected_p2)
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
                    if self.player1: self.player1.random_spawn_point(spawn_x1, spawn_y1)
                    if self.player2: self.player2.random_spawn_point(spawn_x2, spawn_y2)
                    if self.debug_mode:
                        self.printed_arrived = False

                self.draw()
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
        if self.player1:
            self.player1.update(keys, self.collision_mask)
        if self.player2:
            self.player2.update(keys, self.collision_mask)

        if self.player1:
            for zone in self.game_map.transition_zones:
                if zone.rect.colliderect(self.player1.rect):
                    new_pos = zone.target_position
                    self.player1.rect.topleft = new_pos
                    if self.debug_mode:
                        debug_config.log_player_transition("Gracz 1", zone.name, new_pos)
                    break

        if self.player2:
            for zone in self.game_map.transition_zones:
                if zone.rect.colliderect(self.player2.rect):
                    new_pos = zone.target_position
                    self.player2.rect.topleft = new_pos
                    if self.debug_mode:
                        debug_config.log_player_transition("Gracz 2", zone.name, new_pos)
                    break

        if self.debug_mode:
            debug_config.log_player_goal_arrival(self, self.player1, "Gracz 1")
            debug_config.log_player_goal_arrival(self, self.player2, "Gracz 2")

        if self.player1:
            for named_zone in self.game_map.named_zones:
                if named_zone.rect.colliderect(self.player1.rect):
                    self.player1_current_zone_name = named_zone.name

        if self.player2:
            for named_zone in self.game_map.named_zones:
                if named_zone.rect.colliderect(self.player2.rect):
                    self.player2_current_zone_name = named_zone.name

        if self.race:
            self.race.update()

    def draw(self):
        self.left_view.fill(GAME_BACKGROUND_COLOR)
        self.right_view.fill(GAME_BACKGROUND_COLOR)

        if not self.player1:
            pygame.display.flip()
            return

        player1_center_map_coords = pygame.Vector2(self.player1.rect.center)
        player2_center_map_coords = pygame.Vector2(
            self.player2.rect.center) if self.player2 else player1_center_map_coords

        self.camera_left_offset.x = player1_center_map_coords.x * self.zoom - (self.WIDTH // 4)
        self.camera_left_offset.y = player1_center_map_coords.y * self.zoom - (self.HEIGHT // 2)
        self.camera_right_offset.x = player2_center_map_coords.x * self.zoom - (self.WIDTH // 4)
        self.camera_right_offset.y = player2_center_map_coords.y * self.zoom - (self.HEIGHT // 2)

        self.left_view.blit(self.scaled_bg, (-self.camera_left_offset.x, -self.camera_left_offset.y))
        if self.player2:
            self.right_view.blit(self.scaled_bg, (-self.camera_right_offset.x, -self.camera_right_offset.y))

        for sprite in self.all_sprites:
            scaled_img = pygame.transform.smoothscale(
                sprite.image,
                (int(sprite.rect.width * self.zoom), int(sprite.rect.height * self.zoom))
            )

            scaled_pos_left = (pygame.Vector2(sprite.rect.topleft) * self.zoom) - self.camera_left_offset
            self.left_view.blit(scaled_img, scaled_pos_left)

            if self.player2:
                scaled_pos_right = (pygame.Vector2(sprite.rect.topleft) * self.zoom) - self.camera_right_offset
                self.right_view.blit(scaled_img, scaled_pos_right)

        text_surf_p1 = self.zone_font.render(self.player1_current_zone_name, True, self.zone_text_color,
                                             self.zone_text_bg)
        text_rect_p1 = text_surf_p1.get_rect(topleft=(10, 10))
        self.left_view.blit(text_surf_p1, text_rect_p1)

        if self.player2:
            text_surf_p2 = self.zone_font.render(self.player2_current_zone_name, True, self.zone_text_color,
                                                 self.zone_text_bg)
            text_rect_p2 = text_surf_p2.get_rect(topleft=(10, 10))
            self.right_view.blit(text_surf_p2, text_rect_p2)

        if self.debug_mode:
            debug_config.draw_debug_visuals(
                self.left_view,
                self.game_map,
                self.current_target_room,
                self.camera_left_offset,
                self.zoom
            )
            debug_config.draw_debug_visuals(
                self.right_view,
                self.game_map,
                self.current_target_room,
                self.camera_right_offset,
                self.zoom
            )

        self.screen.blit(self.left_view, (0, 0))
        if self.player2:
            self.screen.blit(self.right_view, (self.WIDTH // 2, 0))
            pygame.draw.line(self.screen, BLACK, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT), 2)

        if self.debug_mode:
            pygame.display.set_caption(
                f"FPS: {self.clock.get_fps():.2f}")

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.intro_screen()
    game.run()
