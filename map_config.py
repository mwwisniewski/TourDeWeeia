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
        TransitionZone("Wejscie WEEIA -> Pierwsze pietro", pygame.Rect(2190, 1440, 240, 100), (130, 110)),
        TransitionZone("Wejscie WEEIA -> Parter dlugi korytarz", pygame.Rect(3220, 1538, 180, 30), (3100, 2010)),
        TransitionZone("Wejscie WEEIA -> Pierwsze pietro sieci (DT i Bistro)", pygame.Rect(2390, 110, 50, 80),
                       (4870, 370)),
        TransitionZone("Parter dlugi korytarz -> Wejscie WEEIA", pygame.Rect(3020, 1970, 170, 30), (3300, 1500)),
        TransitionZone("Parter dlugi korytarz -> Pierwsze pietro #1", pygame.Rect(2725, 1965, 25, 90), (1040, 180)),
        TransitionZone("Parter dlugi korytarz -> Pierwsze pietro #2", pygame.Rect(2570, 2995, 100, 180), (840, 1150)),
        TransitionZone("Pierwsze pietro -> Wejscie WEEIA", pygame.Rect(40, 40, 185, 40), (2300, 1400)),
        TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #1", pygame.Rect(968, 135, 32, 90), (2795, 2015)),
        TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #2", pygame.Rect(616, 1065, 134, 175), (2770, 3045)),
        TransitionZone("Pierwsze pietro -> IMSI", pygame.Rect(1535, 685, 30, 40), (1510, 3400)),
        TransitionZone("IMSI -> Pierwsze pietro", pygame.Rect(1508, 3456, 50, 40), (1440, 705)),
        TransitionZone("Pierwsze pietro sieci (DT i Bistro) -> Wejscie WEEIA", pygame.Rect(4790, 260, 180, 70),
                       (2350, 150)),
        TransitionZone("Pierwsze pietro sieci (DT i Bistro) -> Drugie pietro sieci", pygame.Rect(4690, 40, 80, 180),
                       (5810 , 370)),
        TransitionZone("Drugie pietro sieci -> Pierwsze pietro sieci (DT i Bistro)", pygame.Rect(5705, 260, 180, 80),
                       (4650, 135)),
        TransitionZone("Drugie pietro sieci -> Trzecie pietro sieci", pygame.Rect(5600, 40, 80, 180), (7135, 370)),
        TransitionZone("Trzecie pietro sieci -> Drugie pietro sieci", pygame.Rect(7055, 260, 185, 80), (5560, 135)),
        TransitionZone("Trzecie pietro sieci -> Trzeci korytarz sieci", pygame.Rect(6672, 235, 25, 175), (6415, 320)),
        TransitionZone("Trzecie pietro sieci -> Czwarte pietro sieci", pygame.Rect(6955, 40, 80, 180), (8570, 370)),
        TransitionZone("Trzeci korytarz sieci -> Trzecie pietro sieci", pygame.Rect(6455, 235, 25, 175), (6735, 320)),
        TransitionZone("Czwarte pietro sieci -> Trzecie pietro sieci", pygame.Rect(8488, 260, 185, 80), (6915, 135)),
        TransitionZone("Czwarte pietro sieci -> Czwarty korytarz sieci", pygame.Rect(8105, 235, 25, 175), (7800, 320)),
        TransitionZone("Czwarty korytarz sieci -> Czwarte pietro sieci", pygame.Rect(7840, 235, 25, 175), (8145, 320))
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
        TargetRoom("105", pygame.Rect(65, 1973, 25, 50)),
        TargetRoom("104", pygame.Rect(65, 2069, 25, 50)),
        TargetRoom("103", pygame.Rect(65, 2165, 25, 50)),
        TargetRoom("102", pygame.Rect(65, 2260, 25, 50)),
        TargetRoom("131", pygame.Rect(65, 2420, 25, 50)),
        TargetRoom("135", pygame.Rect(65, 2803, 25, 50)),
        TargetRoom("134", pygame.Rect(65, 3252, 25, 50)),
        TargetRoom("133", pygame.Rect(515, 2512, 50, 25)),
        TargetRoom("132", pygame.Rect(995, 2512, 50, 25)),
        TargetRoom("122", pygame.Rect(1567, 2037, 25, 50)),
        TargetRoom("123", pygame.Rect(1567, 2197, 25, 50)),
        TargetRoom("124", pygame.Rect(1567, 2388, 25, 50)),
        TargetRoom("125", pygame.Rect(1567, 2548, 25, 50)),
        TargetRoom("126", pygame.Rect(1567, 2739, 25, 50)),
        TargetRoom("127", pygame.Rect(1567, 2932, 25, 50)),
        TargetRoom("128", pygame.Rect(1567, 3091, 25, 50)),
        TargetRoom("129", pygame.Rect(1567, 3252, 25, 50)),
        # Wejscie WEEIA: (zmienic nazwy jak Piliszek sie dowie jakie to sale)
        TargetRoom("Pokój wykładowców", pygame.Rect(2415, 365, 25, 50)),
        TargetRoom("E4", pygame.Rect(2415, 490, 25, 50)),
        TargetRoom("E3", pygame.Rect(2415, 590, 25, 50)),
        TargetRoom("Laboratorium PEE", pygame.Rect(2415, 1100, 25, 50)),
        TargetRoom("E2", pygame.Rect(2900, 680, 50, 25)),
        TargetRoom("E1", pygame.Rect(3283, 680, 50, 25)),
        # Parter dlugi korytarz:
        TargetRoom("E5", pygame.Rect(2540, 2575, 50, 25)),
        # Sieci pietro 1:
        TargetRoom("Sala DT", pygame.Rect(4375, 1005, 25, 80)),
        # Reszta sal zostanie dodana, gdy ktoś dowie się jakie tam są sale.
        # Drugie pietro sieci (te laboratoria elektrotechniki)
        TargetRoom("Laboratoria elektrotechniki", pygame.Rect(5320, 235, 25, 175))
    ]
    # Zapisane koordynaty spawnow dla roznych pozimow:
    # Wejscie WEEIA: (2140, 275), (2060, 360), (3470, 780)
    # Pierwsze Pietro: (1425, 180), (1020, 1475), (1020, 1320), (1350, 1415)
    # IMSI: (140, 3400), (1200, 2460)
    # Parter dlugi korytarz: (3060, 3450)
    # Pietra sieci: (8210, 300), (6840, 150), (5425, 530), (4900, 400)
    spawn_list = [(2140, 275), (2060, 360), (3470, 780), (1425, 180), (1020, 1475), (1020, 1320), (1350, 1415),
                  (140, 3400), (1200, 2460), (3060, 3450), (8210, 300), (6840, 150), (5425, 530), (4900, 400)]
    return Map("img/mapa_ostateczna.png", "img/mapa_ostateczna_maska.png", spawn_list, transition_zones=transitions,
               target_rooms=rooms)  # MAPA_MASKA_TEST do usuniecia i podmienienia na MAPA_MASKA jak zostanie dodana do main brancha
