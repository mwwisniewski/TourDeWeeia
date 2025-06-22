import pygame
import random
import map_config
from config import *


class EventManager:
    def __init__(self, player1, player2, game_instance):
        self.player1 = player1
        self.player2 = player2
        self.game_ref = game_instance

        self.goal_rect = None
        self.target_rooms = None
        self.target_room = None
        self.new_target_room = None
        self.portier_trigger = pygame.Rect(3170,2990,95,255)
        self.map_triggers = [
            map_config.TransitionZone("Pierwsze pietro -> Wejscie WEEIA", pygame.Rect(40, 40, 185, 40), (2300, 1400)),
            map_config.TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #1", pygame.Rect(968, 135, 32, 90),
                                      (2820, 2075)),
            map_config.TransitionZone("Pierwsze pietro -> Parter dlugi korytarz #2", pygame.Rect(616, 1065, 134, 175),
                                      (2770, 3045)),
            map_config.TransitionZone("Pierwsze pietro sieci (DT i Bistro) -> Wejscie WEEIA",
                                      pygame.Rect(4790, 260, 180, 70), (4870, 370)),
            map_config.TransitionZone("Drugie pietro sieci -> Pierwsze pietro sieci (DT i Bistro)",
                                      pygame.Rect(5705, 260, 180, 80), (4650, 135)),
            map_config.TransitionZone("Trzecie pietro sieci -> Drugie pietro sieci", pygame.Rect(7055, 260, 185, 80),
                                      (5560, 135)),
            map_config.TransitionZone("Czwarte pietro sieci -> Trzecie pietro sieci", pygame.Rect(8488, 260, 185, 80),
                                      (6915, 135))
        ]
        self.active_energols = []
        self.energol_spawn_points = [
            pygame.Rect(100,300,ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(1320, 290, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(1330, 1500, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(3380, 1020, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(3340,2610, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(1470,2000, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(4000,380, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(4000,500, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(6330,110, ENE_WIDTH,ENE_HEIGHT),
            pygame.Rect(7730,110, ENE_WIDTH,ENE_HEIGHT),
        ]

    # static mozna generowac wraz z mapa
    # dynamic podczas gry
    def get_current_target_room(self, target_room):
        self.target_room = target_room

    def get_target_rooms(self, target_rooms):
        self.target_rooms = target_rooms

    def maybe_event_sala(self):
        if random.random() < EVENT_SALA_CHANCE:
            return self.event_zmiana_sali()
        return None

    def event_zmiana_sali(self):  # static
        self.new_target_room = self.target_room
        while self.new_target_room == self.target_room:
            self.new_target_room = random.choice(self.target_rooms)

        message = f"Sala zajęć została zmieniona - nowy cel: Sala - {self.new_target_room.name}"
        if self.game_ref:
            self.game_ref.add_notification(message, duration_seconds=3, target_player="global")
            self.game_ref.sounds['room_change'].play()
        return self.new_target_room

    def maybe_event_lekotka(self, player1, zone):
        if zone.name not in [trigger.name for trigger in self.map_triggers]:
            return None
        if random.random() < EVENT_LEKOTKA_CHANCE:
            return self.event_lekotka(player1)
        return None

    #
    # obecnie lekotka canceluje energola nw czy tak zostawiamy czy cos z tym zrobic
    #
    def event_lekotka(self, player):  # static
        slow_duration_seconds = 8
        freeze_duration_seconds = 2
        display_duration_seconds = 4
        message = f"Auć, pękła Ci łękotka! Jesteś spowolniony na {slow_duration_seconds}s"
        target_player_id = None
        if player == self.player1:
            target_player_id = "player1"
            self.player1.freeze(freeze_duration_seconds * 1000)
            self.player1.speed = PLAYER_SPEED_SLOWED
            self.player1.brokenLeg = True
            self.player1.slow_until(slow_duration_seconds * 1000)

        elif player == self.player2:
            target_player_id = "player2"
            self.player2.freeze(freeze_duration_seconds * 1000)
            self.player2.speed = PLAYER_SPEED_SLOWED
            self.player2.brokenLeg = True
            self.player2.slow_until(slow_duration_seconds * 1000)

        if self.game_ref and target_player_id:
            self.game_ref.add_notification(message, duration_seconds=display_duration_seconds,
                                           target_player=target_player_id)
            self.game_ref.sounds['bone_crack'].play()
            self.game_ref.sounds['lekotka_ouch'].play()

    def spawn_energy_drinks(self):  # static/dynamic nw
        while len(self.active_energols) < ENERGY_DRINKS_UNIT_LIMIT:
            energol = random.choice(self.energol_spawn_points)
            if energol not in self.active_energols:
                self.active_energols.append(energol)

    def event_portier(self):  # static
        if random.random() < EVENT_PORTIER_CHANCE:
            self.player2.kurtka = True
            self.game_ref.add_notification("Musisz odnieść kurtkę do szatni!!!",3,target_player="player2",pos_y_diff=50)
        else:
            self.player2.kurtka = False

        if random.random() < EVENT_PORTIER_CHANCE:
            self.player1.kurtka = True
            self.game_ref.add_notification("Musisz odnieść kurtkę do szatni!!!",3,target_player="player1",pos_y_diff=50)
        else:
            self.player2.kurtka = False