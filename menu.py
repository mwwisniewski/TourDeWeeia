import pygame
import sys
from config import *


class Button:
    def __init__(self, text, x, y, width, height, callback, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.hover_color = (170, 170, 170)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_render = self.font.render(text, True, BLACK)
        self.text_pos = self.text_render.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.blit(self.text_render, self.text_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()


def character_selection_screen(screen, width, clock):
    selection_done = False
    selected_p1 = None
    selected_p2 = None
    character_options = [RED, GREEN, BLUE, YELLOW] # narazie kolorowe kwadraty, sprite'y potem
    font = pygame.font.SysFont("arial", 24)

    p1_index = 0
    p2_index = 1

    button_font = pygame.font.SysFont("arial", 28)
    play_button = Button("GRAJ", width // 2 - 75, 450, 150, 50, lambda: None, font_size=28)
    play_clicked = False

    def draw_selection():
        screen.fill(WHITE)

        # Nagłówki
        title_p1 = font.render("Gracz 1 wybiera ↑/↓ i ENTER", True, BLUE)
        title_p2 = font.render("Gracz 2 wybiera W/S i SPACJA", True, RED)
        screen.blit(title_p1, (100, 50))
        screen.blit(title_p2, (width - title_p2.get_width() - 100, 50))

        for idx, color in enumerate(character_options):
            is_taken_by_p1 = selected_p1 == color
            is_taken_by_p2 = selected_p2 == color

            # Wyszarz jeśli wybrane
            display_color = tuple(int(c * 0.3) for c in color) if (is_taken_by_p1 or is_taken_by_p2) else color

            rect_p1 = pygame.Rect(300, 150 + idx * 60, 50, 50)
            rect_p2 = pygame.Rect(650, 150 + idx * 60, 50, 50)

            pygame.draw.rect(screen, display_color, rect_p1)
            pygame.draw.rect(screen, display_color, rect_p2)

            # Obwódki zaznaczenia
            pygame.draw.rect(screen, BLACK, rect_p1, 2)
            pygame.draw.rect(screen, BLACK, rect_p2, 2)

            if idx == p1_index:
                pygame.draw.rect(screen, BLUE, rect_p1, 4)
            if idx == p2_index:
                pygame.draw.rect(screen, RED, rect_p2, 4)

            if is_taken_by_p1:
                pygame.draw.line(screen, BLUE, rect_p1.topleft, rect_p1.bottomright, 3)
                pygame.draw.line(screen, BLUE, rect_p1.topright, rect_p1.bottomleft, 3)
                pygame.draw.line(screen, BLUE, rect_p2.topleft, rect_p2.bottomright, 3)
                pygame.draw.line(screen, BLUE, rect_p2.topright, rect_p2.bottomleft, 3)

            if is_taken_by_p2:
                pygame.draw.line(screen, RED, rect_p1.topleft, rect_p1.bottomright, 3)
                pygame.draw.line(screen, RED, rect_p1.topright, rect_p1.bottomleft, 3)
                pygame.draw.line(screen, RED, rect_p2.topleft, rect_p2.bottomright, 3)
                pygame.draw.line(screen, RED, rect_p2.topright, rect_p2.bottomleft, 3)

        if selected_p1 and selected_p2:
            play_button.draw(screen)

        pygame.display.flip()

    while not selection_done:
        draw_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if selected_p1 and selected_p2:
                play_button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and play_button.rect.collidepoint(event.pos):
                    play_clicked = True
                    selection_done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1_index = (p1_index - 1) % len(character_options)
                elif event.key == pygame.K_DOWN:
                    p1_index = (p1_index + 1) % len(character_options)
                elif event.key == pygame.K_RETURN:
                    if selected_p1 == character_options[p1_index]:
                        selected_p1 = None
                    elif character_options[p1_index] != selected_p2:
                        selected_p1 = character_options[p1_index]
                elif event.key == pygame.K_w:
                    p2_index = (p2_index - 1) % len(character_options)
                elif event.key == pygame.K_s:
                    p2_index = (p2_index + 1) % len(character_options)
                elif event.key == pygame.K_SPACE:
                    if selected_p2 == character_options[p2_index]:
                        selected_p2 = None
                    elif character_options[p2_index] != selected_p1:
                        selected_p2 = character_options[p2_index]

        if selected_p1 and selected_p2:
            play_button.draw(screen)
            pygame.display.flip()

        clock.tick(FPS)

    return selected_p1, selected_p2
