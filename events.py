import pygame
import random
import sprites
#import sale

class EventTrigger:
    def __init__(self, rect, func, once=True):
        self.rect = rect
        self.func = func
        self.once = once
        self.triggered = False

    def check(self, player_rect):
        if self.rect.colliderect(player_rect) and (not self.triggered or not self.once):
            self.func()
            self.triggered = True

class EventManager:
    def __init__(self, player):
        self.player = player
        self.global_timer = 0
        self.next_event_time = random.randint(10000, 20000)
        self.awaiting_kurtka_answer = False
        self.awaiting_dzien_wydzialu_answer = False

        self.map_triggers = []
        self.blocked_areas = []
        self.map_events = [
            {"area": pygame.Rect(0,0,0,0), "callback": self.event_dzien_wydzialu, "triggered": False},
            {"area": pygame.Rect(0,0,0,0), "callback": self.event_lekotka, "triggered": False},
            {"area": pygame.Rect(0,0,0,0), "callback": self.event_portier, "triggered": False},
            {"area": pygame.Rect(0, 0, 0, 0), "callback": self.event_energol, "triggered": False},
        ]

    def add_map_trigger(self, rect, func, once=True):
        self.map_triggers.append(EventTrigger(rect, func, once))

    def block_area(self, rect):
        self.blocked_areas.append(rect)

    def is_area_blocked(self, player_rect):
        return any(player_rect.colliderect(r) for r in self.blocked_areas)

    def update(self, delta_ms):
        self.global_timer += delta_ms
        if self.global_timer >= self.next_event_time:
            self.trigger_random_event()
            self.global_timer = 0
            self.next_event_time = random.randint(10000, 20000)

        for trigger in self.map_triggers:
            trigger.check(self.player.rect)

    def trigger_random_event(self):
        event = random.choice([
            self.event_plagiat,
            self.event_uczen,
            self.event_bomba,
            self.event_remont
        ])
        event()

    #static mozna generowac wraz z mapa
    #dynamic podczas gry

    def event_plagiat(self):        #dynamic
        print("🚨 Wykryto plagiat na Dante! Rozpoczyna się pościg...")
        self.player.chased = True

    def event_dzien_wydzialu(self): #static
        print("🧑‍🎓 Student: 'Hej, masz może chwilkę?'")

        def zapytaj():
            print("🧑‍🎓 Czeka na odpowiedź... [T/N]")
            self.awaiting_dzien_wydzialu_answer = True

        self.player.forceMove(0,0, on_arrival=zapytaj)



    def event_uczen(self):      #dynamic
        print("👋 Podchodzi do ciebie losowy student. Uniknij go!")


    def event_bomba(self):      #dynamic
        print("💣 Alarm bombowy – ewakuacja budynku!")


    def event_lekotka(self):       #static
        print("Przewróciłeś się na schodach. Pękła ci łękotka.")
        self.player.freeze(2000)
        self.player.speed = 2
        self.player.brokenLeg = True



    def event_energol(self):        #static/dynamic nw
        print("⚡ Rozdają energetyki! Masz bonus do prędkości.")


        if(self.player.brokenLeg):
            self.player.speed = 3
        else:
            self.player.speed = 6


    def event_portier(self):        #static
        print("🚷 Portier cię woła – podejdź do niego.")
        def zapytaj_o_kurtke():
            print("🧥 Portier: 'Zostawiasz kurtkę w szatni?' [T/N]")
            self.awaiting_kurtka_answer = True

        self.player.forceMove(0,0,on_arrival=zapytaj_o_kurtke)
        self.player.freeze(4000)
        #chyba git

    def event_zmiana_sali(self):        #static
        print("🏫 Sala została zmieniona – nowy cel: 213")


    def event_remont(self):     #static
        print("🚧 Remont! To przejście jest zablokowane.")
