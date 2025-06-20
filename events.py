from time import gmtime

import pygame
import random
import map_config
import config


class EventManager:
    def __init__(self, player1, player2, game_instance):
        self.player1 = player1
        self.player2 = player2
        self.game_ref = game_instance

        self.goal_rect = None
        self.target_rooms = None
        self.target_room = None
        self.new_target_room = None

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

    # static mozna generowac wraz z mapa
    # dynamic podczas gry
    def get_current_target_room(self, target_room):
        self.target_room = target_room

    def get_target_rooms(self, target_rooms):
        self.target_rooms = target_rooms

    def maybe_event_sala(self):
        if random.random() < config.EVENT_SALA_CHANCE:
            return self.event_zmiana_sali()
        return None

    def event_zmiana_sali(self):  # static
        self.new_target_room = self.target_room
        while self.new_target_room == self.target_room:
            self.new_target_room = random.choice(self.target_rooms)

        message = f"Sala zajęć została zmieniona - nowy cel: Sala - {self.new_target_room.name}"
        if self.game_ref:
            self.game_ref.add_notification(message, duration_seconds=4, target_player="global")
            self.game_ref.sounds['room_change'].play()
        return self.new_target_room

    def maybe_event_lekotka(self, player1, zone):
        if zone.name not in [trigger.name for trigger in self.map_triggers]:
            return None
        if random.random() < config.EVENT_LEKOTKA_CHANCE:
            return self.event_lekotka(player1)
        return None

    def event_lekotka(self, player):  # static
        slow_duration_seconds = 8
        freeze_duration_seconds = 2
        display_duration_seconds = 5
        message = f"Auć, pękła Ci łękotka! Jesteś spowolniony na {slow_duration_seconds}s"
        target_player_id = None
        if player == self.player1:
            target_player_id = "player1"
            self.player1.freeze(freeze_duration_seconds * 1000)
            self.player1.speed = config.PLAYER_SPEED_SLOWED
            self.player1.brokenLeg = True
            self.player1.slow_until(slow_duration_seconds * 1000)

        elif player == self.player2:
            target_player_id = "player2"
            self.player2.freeze(freeze_duration_seconds * 1000)
            self.player2.speed = config.PLAYER_SPEED_SLOWED
            self.player2.brokenLeg = True
            self.player2.slow_until(slow_duration_seconds * 1000)

        if self.game_ref and target_player_id:
            self.game_ref.add_notification(message, duration_seconds=display_duration_seconds,
                                           target_player=target_player_id)
            self.game_ref.sounds['bone_crack'].play()
            self.game_ref.sounds['lekotka_ouch'].play()

    ############################################################################## do zrobienia (moze)

    def event_energol(self):  # static/dynamic nw
        print("⚡ Rozdają energetyki! Masz bonus do prędkości.")

        if self.player.brokenLeg:
            self.player.speed = 3
        else:
            self.player.speed = 6

    def event_portier(self):  # static
        print("🚷 Portier cię woła – podejdź do niego.")

        def zapytaj_o_kurtke():
            print("🧥 Portier: 'Zostawiasz kurtkę w szatni?' [T/N]")
            self.awaiting_kurtka_answer = True

        self.player.forceMove(0, 0, on_arrival=zapytaj_o_kurtke)
        self.player.freeze(4000)
        # chyba git

    def event_remont(self):  # static
        print("🚧 Remont! To przejście jest zablokowane.")
