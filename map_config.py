import pygame


class Map:
    def __init__(self, name, path, mask_path):
        self.name = name
        self.path = path
        self.mask_path = mask_path

    def load(self):
        bg_image = pygame.image.load(self.path).convert()
        collision_mask = pygame.image.load(self.mask_path).convert()
        collision_mask.set_colorkey((255, 255, 255))
        collision_mask = pygame.mask.from_threshold(collision_mask, (0, 0, 0), (50, 50, 50))
        return bg_image, collision_mask


class MapConfig:
    def __init__(self):
        self.maps = [
            Map("Glowne wejscie", "img/wejscie.png", "img/wejscie_maska.png"), #Zmienic na wejscie weeia i parter
            Map("Korytarz na parterze", "img/parter dlugi korytarz + szatnia.png", "img/wejscie_maska.png"),
            Map("Budynek IMSI", "img/imsi.png", "img/wejscie_maska.png"),
            Map("Pierwsze pietro", "img/pietro.png", "img/wejscie_maska.png")
        ]
