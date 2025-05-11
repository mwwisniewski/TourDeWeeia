import pygame
from config import BLACK


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
