import pygame
import random


class TransitionZone:
    def __init__(self, name, area_rect, target_position):
        self.name = name
        self.rect = area_rect
        self.target_position = target_position


class Map:
    def __init__(self, path, mask_path, spawn_points, transition_zones=None):
        self.path = path
        self.mask_path = mask_path
        self.spawn_points = spawn_points
        self.transition_zones = transition_zones

    def load(self):
        bg_image = pygame.image.load(self.path).convert()
        mask_image = pygame.image.load(self.mask_path).convert()
        mask_image.set_colorkey((255, 255, 255))
        mask_image = pygame.mask.from_threshold(mask_image, (0, 0, 0), (50, 50, 50))
        return bg_image, mask_image

    def get_random_spawn_point(self):
        return random.choice(self.spawn_points)


def create_main_map():
    transitions = [
        TransitionZone("Wejscie WEEIA -> Pierwsze pietro", pygame.Rect(2030, 1450, 240, 100), (130, 110)),
        TransitionZone("Wejscie WEEIA -> Parter dlugi korytarz", pygame.Rect(3060, 1540, 180, 30), (2955, 1750)),
        TransitionZone("Wejscie WEEIA -> Pierwsze pietro sieci (DT i Bistro)", pygame.Rect(2230, 110, 50, 80),
                       (4540, 400)),
        TransitionZone("Parter dlugi korytarz -> Wejscie WEEIA", pygame.Rect(2870, 1690, 170, 30), (3150, 1510)),
        TransitionZone("Parter dlugi korytarz -> Pierwsze pietro #1", pygame.Rect(2575, 1680, 25, 90), (1040, 180)),
        TransitionZone("Parter dlugi korytarz -> Pierwsze pietro #2", pygame.Rect(2420, 2710, 100, 180), (840, 1150)),
        TransitionZone("Pierwsze pietro -> Wejscie WEEIA", pygame.Rect(40, 40, 185, 40), (2150, 1430)),
        TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #1", pygame.Rect(968, 135, 32, 90), (2645, 1730)),
        TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #2", pygame.Rect(616, 1065, 134, 175), (2620, 2760)),
        TransitionZone("Pierwsze pietro -> IMSI", pygame.Rect(1535, 685, 30, 40), (1510, 3150)),
        TransitionZone("IMSI -> Pierwsze pietro", pygame.Rect(1490, 3210, 60, 40), (1440, 705)),
        TransitionZone("Pierwsze pietro sieci (DT i Bistro) -> Wejscie WEEIA", pygame.Rect(4460, 250, 180, 70),
                       (2150, 150)),
        TransitionZone("Pierwsze pietro sieci (DT i Bistro) -> Drugie pietro sieci", pygame.Rect(4360, 55, 80, 180),
                       (5730, 425)),
        TransitionZone("Drugie pietro sieci -> Pierwsze pietro sieci (DT i Bistro)", pygame.Rect(5640, 280, 185, 80),
                       (4330, 135)),
        TransitionZone("Drugie pietro sieci -> Drugi korytarz sieci", pygame.Rect(5255, 285, 25, 175), (4950, 325)),
        TransitionZone("Drugie pietro sieci -> Trzecie pietro sieci", pygame.Rect(5540, 85, 90, 185), (6870, 440)),
        TransitionZone("Drugi korytarz sieci -> Drugie pietro sieci", pygame.Rect(5030,255,25,175), (5330,370)),
        TransitionZone("Trzecie pietro sieci -> Drugie pietro sieci", pygame.Rect(6780, 295, 185, 80), (5480, 175)),
        TransitionZone("Trzecie pietro sieci -> Trzeci korytarz sieci", pygame.Rect(6400,300,25,175),(6100,380)),
        TransitionZone("Trzecie pietro sieci -> Czwarte pietro sieci", pygame.Rect(6680,105,90,185),(8010,425)),
        TransitionZone("Trzeci korytarz sieci -> Trzecie pietro sieci", pygame.Rect(6175,290,25,175),(6490,385)),
        TransitionZone("Czwarte pietro sieci -> Trzecie pietro sieci", pygame.Rect(7920,305,185,80),(6625,195)),
        TransitionZone("Czwarte pietro sieci -> Czwarty korytarz sieci", pygame.Rect(7535,310,25,175),(7250,395)),
        TransitionZone("Czwarty korytarz sieci -> Czwarte pietro sieci", pygame.Rect(7335, 310,25,175), (7630,395))
    ]
    spawn_list = [(1950, 300)]
    return Map("img/mapa.png", "img/mapa_maska_test.png", spawn_list, transition_zones=transitions)
