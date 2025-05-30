import pygame

class RaceManager:
    def __init__(self, player1, player2, goal_rect):
        self.player1 = player1
        self.player2 = player2
        self.goal_rect = goal_rect

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

    def start_round(self):
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

    def update(self):
        if not self.round_active:
            return

        now = pygame.time.get_ticks()

        if not self.player1_finished and self.goal_rect.colliderect(self.player1.rect):
            self.player1_finished = True
            self.player1times[self.round_index] = now - self.globaltimer
            print(f"🏁 Gracz 1 dotarł w {self.player1times[self.round_index]} ms")

        if not self.player2_finished and self.goal_rect.colliderect(self.player2.rect):
            self.player2_finished = True
            self.player2times[self.round_index] = now - self.globaltimer
            print(f"🏁 Gracz 2 dotarł w {self.player2times[self.round_index]} ms")

        if self.player1_finished and self.player2_finished:
            self.end_round()

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

        if self.round_index >= 3:
            self.end_match()
        else:
            self.start_round()

    def end_match(self):
        self.game_over = True
        print("🎉 Koniec gry!")
        print(f"Gracz 1: {self.player1points} pkt"
              f"/tCzasy: "
              f"runda 1: {self.player1times[0]} "
              f"runda 2: {self.player1times[1]} "
              f"runda 3: {self.player1times[2]} ")
        print(f"Gracz 2: {self.player2points} pkt"
              f"/tCzasy: "
              f"runda 1: {self.player2times[0]} "
              f"runda 2: {self.player2times[1]} "
              f"runda 3: {self.player2times[2]} ")

        if self.player1points > self.player2points:
            print("🥇 Wygrywa Gracz 1!")
        elif self.player2points > self.player1points:
            print("🥇 Wygrywa Gracz 2!")
        else:
            print("🤝 Remis!")
