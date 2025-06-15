import pygame
import events

class RaceManager:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.goal_rect = None
        self.player1points = 0
        self.player2points = 0
        self.globaltimer = 0

        self.player1times = [0, 0, 0]
        self.player2times = [0, 0, 0]

        self.player1_finished = False
        self.player2_finished = False

        self.round_index = 0
        self.round_active = False
        self.game_over = False
        self.events = events.EventManager(self.player1, self.player2)

    def start_round(self,goal_rect):
        self.goal_rect = goal_rect
        print(f"▶️ Runda {self.round_index + 1}!") #freeze obydwu graczy
        self.player1.freeze(1000)
        self.player2.freeze(1000)
        pygame.time.wait(1000)
        print("3!")
        self.player1.freeze(1000)
        self.player2.freeze(1000)
        pygame.time.wait(1000)
        print("2!")
        self.player1.freeze(1000)
        self.player2.freeze(1000)
        pygame.time.wait(1000)
        print("1!")
        self.player1.freeze(1000)
        self.player2.freeze(1000)
        pygame.time.wait(1000)
        print("START!")
        self.globaltimer = pygame.time.get_ticks()
        self.round_active = True
        self.player1_finished = False
        self.player2_finished = False
        pygame.event.clear()

    def update(self):
        if not self.round_active:
            return None

        now = pygame.time.get_ticks()

        if not self.player1_finished and self.goal_rect.colliderect(self.player1.rect):
            new_goal = self.events.maybe_event_sala()
            if new_goal and not self.player1_finished and not self.player2_finished:
                self.goal_rect = new_goal.rect
                return new_goal

            self.player1_finished = True
            self.player1times[self.round_index] = now - self.globaltimer
            print(f"🏁 Gracz 1 dotarł w {self.player1times[self.round_index]/1000} s")

        if not self.player2_finished and self.goal_rect.colliderect(self.player2.rect):
            new_goal = self.events.maybe_event_sala()
            if new_goal and not self.player1_finished and not self.player2_finished:
                self.goal_rect = new_goal.rect
                return new_goal

            self.player2_finished = True
            self.player2times[self.round_index] = now - self.globaltimer
            print(f"🏁 Gracz 2 dotarł w {self.player2times[self.round_index]/1000} s")

        if self.player1_finished and self.player2_finished:
            self.end_round()
        return None

    def end_round(self):
        t1 = self.player1times[self.round_index]
        t2 = self.player2times[self.round_index]

        if t1 < t2:
            self.player1points += 1
            print("✅ Punkt dla Gracza 1")
        elif t2 < t1:
            self.player2points += 1
            print("✅ Punkt dla Gracza 2")
        else:
            print("⚖️ Remis – bez punktu")

        self.round_index += 1
        self.round_active = False
        if self.player1points == 2 or self.player2points == 2:
            self.end_match()

    def end_match(self):
        self.game_over = True
        print("🎉 Koniec gry!")
        print(f"Gracz 1: {self.player1points} pkt\n"
              f"\tCzasy: \n"
              f"runda 1: {self.player1times[0]/1000} s\n"
              f"runda 2: {self.player1times[1]/1000} s\n"
              f"runda 3: {self.player1times[2]/1000} s\n")
        print(f"Gracz 2: {self.player2points} pkt\n"
              f"\tCzasy: \n"
              f"runda 1: {self.player2times[0]/1000} s\n"
              f"runda 2: {self.player2times[1]/1000} s\n"
              f"runda 3: {self.player2times[2]/1000} s\n")

        if self.player1points > self.player2points:
            print("🥇 Wygrywa Gracz 1!")
        elif self.player2points > self.player1points:
            print("🥇 Wygrywa Gracz 2!")
        else:
            print("🤝 Remis!")


