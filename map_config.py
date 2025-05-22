import pygame
import random


class Map:
    def __init__(self, name, path, mask_path, spawn_points, transitions=None):
        self.name = name
        self.path = path
        self.mask_path = mask_path
        self.spawn_points = spawn_points
        self.transitions = transitions or []

    def load(self):
        bg_image = pygame.image.load(self.path).convert()
        collision_mask = pygame.image.load(self.mask_path).convert()
        collision_mask.set_colorkey((255, 255, 255))
        collision_mask = pygame.mask.from_threshold(collision_mask, (0, 0, 0), (50, 50, 50))
        return bg_image, collision_mask

    def get_random_spawn_point(self):
        return random.choice(self.spawn_points)


class MapConfig:
    def __init__(self):
        glowne_wejscie_transition = [
            MapTransition(pygame.Rect(235, 1100, 400, 400), "Pierwsze pietro", target_spawn=(135, 175))
        ]

        self.maps = [
            Map("Glowne wejscie", "img/wejscie weeia i parter.png", "img/wejscie weeia i parter_maska.png",
                [(150, 262), (1530, 775)], transitions=glowne_wejscie_transition),
            # Map("Korytarz na parterze", "img/parter dlugi korytarz + szatnia.png",
            #    "img/parter dlugi korytarz + szatnia_maska.png", [(1141, 46), (1126, 1526)]),
            # Map("Budynek IMSI", "img/imsi.png", "img/imsi_maska.png", [(135, 90)]),
            # Map("Pierwsze pietro", "img/pierwsze pietro.png", "img/pierwsze pietro_maska.png",
            #    [(1020, 1480), (1450, 100)]),
            # Map("Pietra przy sieciach", "img/pietra przy sieciach.png", "img/pietra przy sieciach_maska.png",
            #    [(105, 320)]),
            # Map("Klatka schodowa", "img/klatka schodowa.png", "img/klatka schodowa_maska.png", [(300, 525)])
            # tymczasowe pozniej zmienic jak nowa mapa bedzie
        ]

    def get_random_map(self):
        return random.choice(self.maps)

    def get_map_by_name(self, name):
        return next((m for m in self.maps if m.name == name), None)


class MapTransition:
    def __init__(self, area_rect, next_map_name, target_spawn=None):
        self.area_rect = area_rect
        self.next_map_name = next_map_name
        self.target_spawn = target_spawn
