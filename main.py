import pygame.image

import map_config
from map_config import *
from sprites import *
from menu import *
from game_logic import RaceManager
from menu import character_selection_screen
from debug_config import *
from config import *


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode((1, 1))

        self.MAP_HEIGHT = None
        self.MAP_WIDTH = None

        self.game_map = create_main_map()
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
        self.race = None
        self.debug_mode = config.DEBUG  # DO TESTOW POTEM ZMIENIC NA FALSE LUB NONE!! (POKAZUJE STREFY PRZEJSC, STREFY SAL ORAZ FPSY)
        self.printed_destination = True
        if self.debug_mode:
            self.printed_arrived = False

        self.default_zone_name = "Nieznany obszar"
        self.player1_current_zone_name = self.default_zone_name
        self.player2_current_zone_name = self.default_zone_name
        self.zone_font = pygame.font.SysFont("arial", 20, bold=True)
        self.game_info_font = pygame.font.SysFont("arial", 24, bold=True)
        self.notification_font = pygame.font.SysFont("arial", 30, bold=True)
        self.target_info_font = pygame.font.SysFont("arial", 18, bold=True)
        self.zone_text_color = BLACK
        self.zone_text_bg = None
        self.active_notifications = []
        self.notified_flag = False
        self.energolimg = pygame.image.load("img/grafika power-up.png")
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        self.menu_music_path = "sounds/menu_background_opcja1.mp3"
        self.race_music_path = "sounds/race_background_music.mp3"
        self.end_of_match = "sounds/menu_background_opcja3.mp3"

        self.sounds['menu_click'] = pygame.mixer.Sound("sounds/menu_select.wav")
        self.sounds['countdown'] = pygame.mixer.Sound("sounds/race_countdown_opcja1.mp3")
        self.sounds['room_change'] = pygame.mixer.Sound("sounds/room_change_notification.ogg")
        self.sounds['success'] = pygame.mixer.Sound("sounds/success_opcja2.wav")
        self.sounds['lekotka_ouch'] = pygame.mixer.Sound("sounds/ouch_opcja1.wav")
        self.sounds['bone_crack'] = pygame.mixer.Sound("sounds/bone_crack.wav")
        # self.sounds['energizer'] = pygame.mixer.Sound("sounds/energizer.wav")

    def add_notification(self, message, duration_seconds, target_player=None, text_color=WHITE, bg_color=None,
                         position_topleft=None, position_center=None, pos_y_diff=0, font_type=None,
                         outline_color=BLACK, outline_thickness=1):  # NOWE PARAMETRY
        # target_player global (srodek ekranu) lub None (ale ustwiajcie global), lub player1 (lewo), player2(prawo)
        # position_topleft i position_center maja priorytet nad target_player!
        # pos_y_diff obniza napis w y, bg color nie ma co ruszac bo to prostokat,
        # a przynajmniej tak bylo jak ostatnio sprawdzalem

        # dla filipa nr2: uzywaj message, duration, target, text color i outline color ew. pos y,
        # outline thickness, font type(wielkosc, chyba ze zmienisz tez rodzaj (tam wyzej ^))

        # Wybór czcionki
        if font_type == "zone":
            font = self.zone_font  # 20
        elif font_type == "game":
            font = self.game_info_font  # 24
        elif font_type == "target":
            font = self.target_info_font  # 18
        else:
            font = self.notification_font  # 30

        text_surf = font.render(message, True, text_color)
        padding = 10
        bg_width = text_surf.get_width() + 2 * padding
        bg_height = text_surf.get_height() + 2 * padding
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)

        if bg_color:
            bg_surface.fill(bg_color)

        text_rect_on_bg = text_surf.get_rect(center=(bg_width // 2, bg_height // 2))

        # obramowka dla tekstu
        if outline_color and outline_thickness > 0:
            outline_surf = font.render(message, True, outline_color)
            for dx in range(-outline_thickness, outline_thickness + 1):
                for dy in range(-outline_thickness, outline_thickness + 1):
                    if dx == 0 and dy == 0:  # Nie rysuj na pozycji głównego tekstu
                        continue
                    outline_pos = (text_rect_on_bg.x + dx, text_rect_on_bg.y + dy)
                    bg_surface.blit(outline_surf, outline_pos)

        bg_surface.blit(text_surf, text_rect_on_bg)

        final_rect = bg_surface.get_rect()
        if position_topleft:
            final_rect.topleft = position_topleft
        elif position_center:
            final_rect.center = position_center
        else:
            default_top_y = 70 + pos_y_diff
            if target_player is None or target_player == "global":
                final_rect.centerx = self.WIDTH // 2
                final_rect.top = default_top_y
            elif target_player == "player1":
                final_rect.centerx = self.WIDTH // 4
                final_rect.top = default_top_y
            elif target_player == "player2":
                final_rect.centerx = self.WIDTH * 3 // 4
                final_rect.top = default_top_y
            else:  # dla pewnosci zeby nie bylo bledow
                final_rect.centerx = self.WIDTH // 2
                final_rect.top = default_top_y

        end_time = pygame.time.get_ticks() + duration_seconds * 1000

        self.active_notifications.append({
            "surface": bg_surface,
            "rect": final_rect,
            "end_time": end_time
        })

    def render_text_with_outline(self, message: str, text_color=WHITE, outline_color=BLACK,
                                 antialias: bool = True, font=None, outline_thickness=1) -> pygame.Surface:
        # tekst z obramowka (caly czas)
        # :param antialias: Czy używać antyaliasingu (domyślnie True).

        # 1. Renderuj główny tekst
        font = self.game_info_font
        text_surf = font.render(message, antialias, text_color)

        if outline_thickness <= 0 or outline_color is None:
            return text_surf

        outline_surf = font.render(message, antialias, outline_color)
        final_width = text_surf.get_width() + 2 * outline_thickness
        final_height = text_surf.get_height() + 2 * outline_thickness
        final_surface = pygame.Surface((final_width, final_height), pygame.SRCALPHA)
        final_surface.fill((0, 0, 0, 0))

        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                outline_pos = (outline_thickness + dx, outline_thickness + dy)
                final_surface.blit(outline_surf, outline_pos)

        text_pos_on_final = (outline_thickness, outline_thickness)
        final_surface.blit(text_surf, text_pos_on_final)

        return final_surface

    def intro_screen(self):
        intro = True

        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

        def start_game():
            nonlocal intro

            self.all_sprites = pygame.sprite.Group()

            selected_p1, selected_p2 = character_selection_screen(self, self.screen, self.WIDTH, self.clock)

            spawn_x1, spawn_y1 = self.game_map.get_random_spawn_point()
            spawn_x2, spawn_y2 = self.game_map.get_random_spawn_point()
            self.current_target_room = random.choice(self.game_map.target_rooms)
            self.is_current_target_room = True
            self.player1 = Player(spawn_x1, spawn_y1, CONTROL_TYPE_WSAD, selected_p1)
            self.player2 = Player(spawn_x2, spawn_y2, CONTROL_TYPE_ARROWS, selected_p2)
            self.all_sprites.add(self.player1)
            self.all_sprites.add(self.player2)
            self.race = RaceManager(self.player1, self.player2, self)
            self.race.events.get_target_rooms(self.game_map.target_rooms)

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
            Menu("Start", button_x, button_y_start + 0 * button_spacing, button_width, button_height, start_game),
            Menu("Ustawienia", button_x, button_y_start + 1 * button_spacing, button_width, button_height,
                 open_settings),
            Menu("Wyjście", button_x, button_y_start + 2 * button_spacing, button_width, button_height, quit_game),
        ]

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                for button in buttons:
                    if button.handle_event(event):
                        self.sounds['menu_click'].play()

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
                    if self.player1: self.player1.update_player_position(spawn_x1, spawn_y1)
                    if self.player2: self.player2.update_player_position(spawn_x2, spawn_y2)
                    if self.debug_mode:
                        self.printed_arrived = False

                self.is_current_target_room = False
                self.add_notification(f"Nowy cel: Sala {self.current_target_room.name}", 6, target_player="player1")
                self.add_notification(f"Nowy cel: Sala {self.current_target_room.name}", 6, target_player="player2")
                self.update()
                self.draw()
                self.race.events.get_current_target_room(self.current_target_room)
                self.race.start_round(self.current_target_room.rect)
                if self.game_map.path != DEFAULT_MAP and not self.notified_flag:
                    self.add_notification("UWAGA!! NA WYDZIALE MAMY REMONT, MOZLIWE ZABLOKOWANE PRZEJSCIA", 6,
                                          target_player="global", pos_y_diff=100, font_type="game", )
                    self.notified_flag = True
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
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
                    self.race.events.maybe_event_lekotka(self.player1, zone)
                    self.player1.rect.topleft = new_pos
                    if self.debug_mode:
                        log_player_transition("Gracz 1", zone.name, new_pos)
                    break

        if self.player2:
            for zone in self.game_map.transition_zones:
                if zone.rect.colliderect(self.player2.rect):
                    new_pos = zone.target_position
                    self.race.events.maybe_event_lekotka(self.player2, zone)
                    self.player2.rect.topleft = new_pos
                    if self.debug_mode:
                        log_player_transition("Gracz 2", zone.name, new_pos)
                    break

        if self.debug_mode:
            log_player_goal_arrival(self, self.player1, "Gracz 1")
            log_player_goal_arrival(self, self.player2, "Gracz 2")

        if self.player1:
            for named_zone in self.game_map.named_zones:
                if named_zone.rect.colliderect(self.player1.rect):
                    self.player1_current_zone_name = named_zone.name

        if self.player2:
            for named_zone in self.game_map.named_zones:
                if named_zone.rect.colliderect(self.player2.rect):
                    self.player2_current_zone_name = named_zone.name

        if self.race:
            goal = self.race.update()
            if goal is not None:
                self.current_target_room = goal

        if self.race.energol_picked_up1:
            self.add_notification("Znajdujesz energetyka!", 1, target_player="player1", font_type="game",
                                  text_color=GREEN, pos_y_diff=150)
        if self.race.energol_picked_up2:
            self.add_notification("Znajdujesz energetyka!", 1, target_player="player2", font_type="game",
                                  text_color=GREEN, pos_y_diff=150)

        current_time = pygame.time.get_ticks()
        self.active_notifications = [n for n in self.active_notifications if current_time < n["end_time"]]

    def draw(self):
        self.left_view.fill(GAME_BACKGROUND_COLOR)
        self.right_view.fill(GAME_BACKGROUND_COLOR)

        if not self.player1:
            for notification in self.active_notifications:
                self.screen.blit(notification["surface"], notification["rect"])
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

        scaled_target_width = int(ENE_WIDTH * self.zoom)
        scaled_target_height = int(ENE_HEIGHT * self.zoom)

        scaled_energol_image_to_blit = pygame.transform.smoothscale(
            self.energolimg, (scaled_target_width, scaled_target_height))

        for current_energol_rect in self.race.events.active_energols:
            energol_map_pos = pygame.Vector2(current_energol_rect.topleft)

            # Rysowanie na lewym widoku (dla gracza 1)
            scaled_pos_left_energol = (energol_map_pos * self.zoom) - self.camera_left_offset
            self.left_view.blit(scaled_energol_image_to_blit, scaled_pos_left_energol)

            # Rysowanie na prawym widoku, jeśli istnieje gracz 2
            if self.player2:
                scaled_pos_right_energol = (energol_map_pos * self.zoom) - self.camera_right_offset
                self.right_view.blit(scaled_energol_image_to_blit, scaled_pos_right_energol)

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

        text_surf_p1 = self.render_text_with_outline(self.player1_current_zone_name)
        text_rect_p1 = text_surf_p1.get_rect(topleft=(10, 10))
        self.left_view.blit(text_surf_p1, text_rect_p1)

        if self.player2:
            text_surf_p2 = self.render_text_with_outline(self.player2_current_zone_name)
            text_rect_p2 = text_surf_p2.get_rect(topright=((self.WIDTH // 2) - 15, 10))
            self.right_view.blit(text_surf_p2, text_rect_p2)

        if self.debug_mode:
            draw_debug_visuals(
                self.left_view,
                self.game_map,
                self.current_target_room,
                self.camera_left_offset,
                self.zoom
            )
            if self.player2:
                draw_debug_visuals(
                    self.right_view,
                    self.game_map,
                    self.current_target_room,
                    self.camera_right_offset,
                    self.zoom
                )

        self.screen.blit(self.left_view, (0, 0))
        if self.player2:
            self.screen.blit(self.right_view, (self.WIDTH // 2, 0))
            pygame.draw.line(self.screen, DARKGRAY, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT), 1)

        if self.race:
            if self.race.round_active:
                current_round_time = (pygame.time.get_ticks() - self.race.globaltimer) / 1000
                time_str = f"{int(current_round_time // 60)}:{current_round_time % 60:.2f}"
                time_surf = self.render_text_with_outline(message=time_str)
                time_rect = time_surf.get_rect(centerx=self.WIDTH // 2, top=10)
                self.screen.blit(time_surf, time_rect)
            else:
                time_str = "0:00"
                time_surf = self.render_text_with_outline(message=time_str)
                time_rect = time_surf.get_rect(centerx=self.WIDTH // 2, top=10)
                self.screen.blit(time_surf, time_rect)

            p1_score_str = str(self.race.player1points)
            p1_score_surf = self.render_text_with_outline(p1_score_str)
            p1_score_rect = p1_score_surf.get_rect(centerx=self.WIDTH // 2 - 10, top=40)
            self.screen.blit(p1_score_surf, p1_score_rect)

            colon_surf = self.render_text_with_outline(":")
            colon_rect = colon_surf.get_rect(centerx=self.WIDTH // 2, top=40)
            self.screen.blit(colon_surf, colon_rect)

            if self.player2:
                p2_score_str = str(self.race.player2points)
                p2_score_surf = self.render_text_with_outline(p2_score_str)
                p2_score_rect = p2_score_surf.get_rect(centerx=self.WIDTH // 2 + 10, top=40)
                self.screen.blit(p2_score_surf, p2_score_rect)

        if self.debug_mode:
            pygame.display.set_caption(
                f"FPS: {self.clock.get_fps():.2f}")

        target_text_str = f"Cel: {self.current_target_room.name}"
        text_surf = self.render_text_with_outline(target_text_str)

        if self.player1 and self.current_target_room:
            rect_p1_target = text_surf.get_rect()
            rect_p1_target.bottomleft = (15, self.HEIGHT - 15)
            self.screen.blit(text_surf, rect_p1_target)

        if self.player2 and self.current_target_room:
            rect_p2_target = text_surf.get_rect()
            rect_p2_target.bottomright = (self.WIDTH - 15, self.HEIGHT - 15)
            self.screen.blit(text_surf, rect_p2_target)

        for notification in self.active_notifications:
            self.screen.blit(notification["surface"], notification["rect"])

        pygame.display.flip()

    def reset_game(self):
        self.race.player1points = 0
        self.race.player2points = 0
        self.race.globaltimer = 0
        self.race.player1times = [0, 0, 0]
        self.race.player2times = [0, 0, 0]
        self.race.player1_finished = False
        self.race.player2_finished = False
        self.race.round_index = 0
        self.race.game_over = False
        self.race.goal_rect = None
        self.race.round_active = False
        self.active_notifications = []
        temp = self.game_map.path
        self.game_map.path, self.game_map.mask_path = map_config.get_random_map()
        if self.game_map.path != temp:
            self.bg_image, self.collision_mask = self.game_map.load()
            self.MAP_WIDTH, self.MAP_HEIGHT = self.bg_image.get_size()
        self.notified_flag = False
        self.race.reset_players_state()
        self.add_notification("Nastąpił restart gry!", 5, target_player="global", position_center=(800, 800))


if __name__ == "__main__":
    game = Game()
    game.intro_screen()
    game.run()
