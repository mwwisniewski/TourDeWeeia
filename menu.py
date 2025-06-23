import pygame
import sys
import config


class Menu:
    def __init__(self, text, x, y, width, height, callback, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.hover_color = (170, 170, 170)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_render = self.font.render(text, True, config.BLACK)
        self.text_pos = self.text_render.get_rect(center=self.rect.center)
        self.active = True

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if not self.active:
            color = (150, 150, 150)
        else:
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, config.BLACK, self.rect, 2)
        screen.blit(self.text_render, self.text_pos)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
            return True
        return False


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label_text = label
        self.callback = callback

        self.handle_width = 20
        self.handle_rect = pygame.Rect(0, 0, self.handle_width, height + 10)
        self.update_handle_pos()

        self.dragging = False
        self.font = pygame.font.SysFont("arial", 24)

    def _update_value_from_pos(self, x_pos):
        new_x = max(self.rect.left, min(x_pos, self.rect.right))

        # przeliczenie pozycji na wartosc
        if self.rect.width > 0:
            ratio = (new_x - self.rect.x) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            self.update_handle_pos()
            self.callback(self.value)

    def update_handle_pos(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * (self.rect.width - self.handle_width)
        self.handle_rect.centerx = handle_x + self.handle_width // 2
        self.handle_rect.centery = self.rect.centery

    def draw(self, screen):
        # suwak tło
        pygame.draw.rect(screen, config.DARKGRAY, self.rect)

        # wypelnienie suwaka
        fill_width = (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, config.GREEN, fill_rect)

        # uchwyt
        pygame.draw.rect(screen, config.WHITE, self.handle_rect)
        pygame.draw.rect(screen, config.BLACK, self.handle_rect, 2)

        # etykieta
        label_surf = self.font.render(self.label_text, True, config.BLACK)
        screen.blit(label_surf, (self.rect.x, self.rect.y - 30))

        # wartosc procentowa
        percent_val = int(self.value * 100)
        value_surf = self.font.render(f"{percent_val}%", True, config.BLACK)
        screen.blit(value_surf, (self.rect.right + 15, self.rect.centery - value_surf.get_height() // 2))

    def handle_event(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # czy klikniety w pasek
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value_from_pos(mouse_x)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value_from_pos(mouse_x)


def character_selection_screen(game_instance, screen, width, clock):
    selection_done = False
    selected_p1 = None
    selected_p2 = None

    character_paths = [
        "img/sprites/sprite1",
        "img/sprites/sprite2",
        "img/sprites/sprite3",
        "img/sprites/sprite4",
    ]
    character_options = []
    for path in character_paths:
        img = pygame.image.load(f"{path}/idle_down_0.png").convert_alpha()
        img = pygame.transform.scale(img,
                                     (50 * config.ZOOM_CHARACTER_SCREEN_MULT, 50 * config.ZOOM_CHARACTER_SCREEN_MULT))
        character_options.append((path, img))  # (ścieżka, obrazek)

    font = pygame.font.SysFont("arial", int(24 * config.ZOOM_CHARACTER_SCREEN_MULT))
    p1_index = 0
    p2_index = 1

    sprite_size = int(50 * config.ZOOM_CHARACTER_SCREEN_MULT)
    spacing_y = int(80 * config.ZOOM_CHARACTER_SCREEN_MULT)

    button_width = int(150 * config.ZOOM_CHARACTER_SCREEN_MULT)
    button_height = int(50 * config.ZOOM_CHARACTER_SCREEN_MULT)
    button_x = width // 2 - button_width // 2

    num_characters = len(character_options)
    bottom_of_selection = 150 + num_characters * spacing_y
    space_after = 40
    button_y = bottom_of_selection + space_after

    play_button = Menu("GRAJ", button_x, button_y, button_width, button_height, lambda: None,
                       font_size=int(28 * config.ZOOM_CHARACTER_SCREEN_MULT))

    def draw_cross(surface, color, rect):
        # zeby uniknac duplikacji funkcja do przekreslania wybranej postaci
        pygame.draw.line(surface, color, rect.topleft, rect.bottomright, 4)
        pygame.draw.line(surface, color, rect.topright, rect.bottomleft, 4)

    def draw_selection():
        screen.fill(config.WHITE)

        title_p1 = font.render("Gracz 1 wybiera W/S i SPACJA", True, config.BLUE)
        title_p2 = font.render("Gracz 2 wybiera ↑/↓ i ENTER", True, config.RED)
        screen.blit(title_p1, (100, 50))
        screen.blit(title_p2, (width - title_p2.get_width() - 100, 50))

        for idx, (char_path, char_img) in enumerate(character_options):
            is_taken_by_p1 = selected_p1 == char_path
            is_taken_by_p2 = selected_p2 == char_path

            left_x = width // 4 - sprite_size // 2
            right_x = width * 3 // 4 - sprite_size // 2

            rect_p1 = pygame.Rect(left_x, 150 + idx * spacing_y, sprite_size, sprite_size)
            rect_p2 = pygame.Rect(right_x, 150 + idx * spacing_y, sprite_size, sprite_size)

            img_p1 = char_img.copy()
            img_p2 = char_img.copy()
            if is_taken_by_p1 or is_taken_by_p2:
                img_p1.set_alpha(100)
                img_p2.set_alpha(100)

            screen.blit(img_p1, rect_p1)
            screen.blit(img_p2, rect_p2)

            pygame.draw.rect(screen, config.BLACK, rect_p1, 2)
            pygame.draw.rect(screen, config.BLACK, rect_p2, 2)

            if idx == p1_index:
                pygame.draw.rect(screen, config.BLUE, rect_p1, 4)
            if idx == p2_index:
                pygame.draw.rect(screen, config.RED, rect_p2, 4)

            if is_taken_by_p1:
                draw_cross(screen, config.BLUE, rect_p1)
                draw_cross(screen, config.BLUE, rect_p2)

            if is_taken_by_p2:
                draw_cross(screen, config.RED, rect_p1)
                draw_cross(screen, config.RED, rect_p2)

        both_selected = selected_p1 and selected_p2
        play_button.active = both_selected
        play_button.draw(screen)
        pygame.display.flip()

    while not selection_done:
        draw_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Gracz 1 — WSAD + SPACJA
                if event.key == pygame.K_w:
                    p1_index = (p1_index - 1) % len(character_options)
                    game_instance.sounds['menu_click'].play()
                elif event.key == pygame.K_s:
                    p1_index = (p1_index + 1) % len(character_options)
                    game_instance.sounds['menu_click'].play()
                elif event.key == pygame.K_SPACE:
                    selected_path = character_options[p1_index][0]
                    if selected_p1 == selected_path:
                        selected_p1 = None
                    elif selected_path != selected_p2:
                        selected_p1 = selected_path
                    game_instance.sounds['menu_click'].play()

                # Gracz 2 — STRZAŁKI + ENTER
                elif event.key == pygame.K_UP:
                    p2_index = (p2_index - 1) % len(character_options)
                    game_instance.sounds['menu_click'].play()
                elif event.key == pygame.K_DOWN:
                    p2_index = (p2_index + 1) % len(character_options)
                    game_instance.sounds['menu_click'].play()
                elif event.key == pygame.K_RETURN:
                    selected_path = character_options[p2_index][0]
                    if selected_p2 == selected_path:
                        selected_p2 = None
                    elif selected_path != selected_p1:
                        selected_p2 = selected_path
                    game_instance.sounds['menu_click'].play()

            if selected_p1 and selected_p2:
                if play_button.handle_event(event):
                    game_instance.sounds['menu_click'].play()
                    pygame.mixer.music.fadeout(500)
                    selection_done = True

        clock.tick(config.FPS)

    return selected_p1, selected_p2
