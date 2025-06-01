import pygame
import random


class TargetRoom:
    def __init__(self, name, area_rect):
        self.name = name
        self.rect = area_rect


class TransitionZone:
    def __init__(self, name, area_rect, target_position):
        self.name = name
        self.rect = area_rect
        self.target_position = target_position


class Map:
    def __init__(self, path, mask_path, spawn_points, transition_zones=None, target_rooms=None):
        self.path = path
        self.mask_path = mask_path
        self.spawn_points = spawn_points
        self.transition_zones = transition_zones
        self.target_rooms = target_rooms

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
        TransitionZone("Drugi korytarz sieci -> Drugie pietro sieci", pygame.Rect(5030, 255, 25, 175), (5330, 370)),
        TransitionZone("Trzecie pietro sieci -> Drugie pietro sieci", pygame.Rect(6780, 295, 185, 80), (5480, 175)),
        TransitionZone("Trzecie pietro sieci -> Trzeci korytarz sieci", pygame.Rect(6400, 300, 25, 175), (6100, 380)),
        TransitionZone("Trzecie pietro sieci -> Czwarte pietro sieci", pygame.Rect(6680, 105, 90, 185), (8010, 425)),
        TransitionZone("Trzeci korytarz sieci -> Trzecie pietro sieci", pygame.Rect(6175, 290, 25, 175), (6490, 385)),
        TransitionZone("Czwarte pietro sieci -> Trzecie pietro sieci", pygame.Rect(7920, 305, 185, 80), (6625, 195)),
        TransitionZone("Czwarte pietro sieci -> Czwarty korytarz sieci", pygame.Rect(7535, 310, 25, 175), (7250, 395)),
        TransitionZone("Czwarty korytarz sieci -> Czwarte pietro sieci", pygame.Rect(7335, 310, 25, 175), (7630, 395))
    ]
    rooms = [
        # Pierwsze pietro:
        TargetRoom("E101", pygame.Rect(1160, 40, 50, 25)),
        TargetRoom("E103", pygame.Rect(395, 230, 50, 25)),
        TargetRoom("E104", pygame.Rect(300, 390, 50, 25)),
        TargetRoom("E105", pygame.Rect(555, 390, 50, 25)),
        TargetRoom("E102", pygame.Rect(715, 230, 50, 25)),
        TargetRoom("E106", pygame.Rect(970, 525, 25, 50)),
        TargetRoom("107", pygame.Rect(715, 680, 50, 25)),
        TargetRoom("108", pygame.Rect(460, 680, 50, 25)),
        TargetRoom("109", pygame.Rect(300, 840, 50, 25)),
        TargetRoom("110", pygame.Rect(715, 840, 50, 25)),
        TargetRoom("Pracownia komputerowa", pygame.Rect(40, 490, 25, 50)),
        # IMSI:
        TargetRoom("105", pygame.Rect(50, 1725, 25, 50)),
        TargetRoom("104", pygame.Rect(50, 1820, 25, 50)),
        TargetRoom("103", pygame.Rect(50, 1915, 25, 50)),
        TargetRoom("102", pygame.Rect(50, 2010, 25, 50)),
        TargetRoom("131", pygame.Rect(50, 2170, 25, 50)),
        TargetRoom("135", pygame.Rect(50, 2555, 25, 50)),
        TargetRoom("134", pygame.Rect(50, 3005, 25, 50)),
        TargetRoom("133", pygame.Rect(500, 2260, 50, 25)),
        TargetRoom("132", pygame.Rect(980, 2260, 50, 25)),
        TargetRoom("122", pygame.Rect(1550, 1785, 25, 50)),
        TargetRoom("123", pygame.Rect(1550, 1950, 25, 50)),
        TargetRoom("124", pygame.Rect(1550, 2140, 25, 50)),
        TargetRoom("125", pygame.Rect(1550, 2300, 25, 50)),
        TargetRoom("126", pygame.Rect(1550, 2490, 25, 50)),
        TargetRoom("127", pygame.Rect(1550, 2685, 25, 50)),
        TargetRoom("128", pygame.Rect(1550, 2845, 25, 50)),
        TargetRoom("129", pygame.Rect(1550, 3000, 25, 50)),
        # Wejscie WEEIA: (zmienic nazwy jak Piliszek sie dowie jakie to sale)
        TargetRoom("tujakassala", pygame.Rect(2255, 365, 25, 50)),
        TargetRoom("tutez", pygame.Rect(2255, 490, 25, 50)),
        TargetRoom("tute", pygame.Rect(2255, 590, 25, 50)),
        TargetRoom("elektortechniak ta", pygame.Rect(2255, 1100, 25, 50)),
        TargetRoom("E2", pygame.Rect(2740, 680, 50, 25)),
        TargetRoom("E1", pygame.Rect(3125, 680, 50, 25)),
        # Parter dlugi korytarz:
        TargetRoom("E5", pygame.Rect(2390, 2290, 50, 25)),
        # Sieci pietro 1:
        TargetRoom("Sala DT", pygame.Rect(4040, 1020, 25, 80))
        # Reszta sal zostanie dodana, gdy ktoś dowie się jakie tam są sale.
    ]
    # Zapisane koordynaty spawnow dla roznych pozimow:
    # Wejscie WEEIA: (1950, 275), (1900, 400), (3330, 785)
    # Pierwsze Pietro: (1425, 180), (1020, 1475), (1020, 1320), (1350, 1415)
    # IMSI: (140, 3200), (1100, 2250)
    # Parter dlugi korytarz: (2940, 3150)
    # Pietra sieci: (7630, 200), (6490, 580), (5730, 560)
    spawn_list = [(1950, 275), (1900, 400), (3330, 785), (1425, 180), (1020, 1475), (1020, 1320), (1350, 1415),
                  (140, 3200), (1100, 2250), (2940, 3150), (7630, 200), (6490, 580), (5730, 560)]
    return Map("img/mapa.png", "img/mapa_maska_test.png", spawn_list, transition_zones=transitions,
               target_rooms=rooms)  # MAPA_MASKA_TEST do usuniecia i podmienienia na MAPA_MASKA jak zostanie dodana do main brancha
