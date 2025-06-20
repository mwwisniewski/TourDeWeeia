import pygame
import events
import config


class RaceManager:
    def __init__(self, player1, player2, game_instance):
        self.player1 = player1
        self.player2 = player2
        self.game_instance = game_instance
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
        self.events = events.EventManager(self.player1, self.player2, self.game_instance)

    def start_round(self, goal_rect):
        self.goal_rect = goal_rect
        round_start_delay_ms = 1000
        if self.game_instance:
            self.game_instance.add_notification(f"Runda {self.round_index + 1}!", 1, target_player="global")
            self.game_instance.update()
            self.game_instance.draw()
        self.player1.freeze(round_start_delay_ms * 4)
        self.player2.freeze(round_start_delay_ms * 4)
        pygame.time.wait(round_start_delay_ms)

        if self.game_instance:
            self.game_instance.sounds['countdown'].play()

        if self.game_instance:
            self.game_instance.add_notification("3!", 1, target_player="global", text_color=config.RED)
            self.game_instance.update()
            self.game_instance.draw()
        pygame.time.wait(1000)
        if self.game_instance:
            self.game_instance.add_notification("2!", 1, target_player="global", text_color=config.ORANGE)
            self.game_instance.update()
            self.game_instance.draw()
        pygame.time.wait(1000)
        if self.game_instance:
            self.game_instance.add_notification("1!", 1, target_player="global", text_color=config.YELLOW)
            self.game_instance.update()
            self.game_instance.draw()
        pygame.time.wait(1000)
        if self.game_instance:
            self.game_instance.add_notification("START!", 1, target_player="global", text_color=config.GREEN)
            self.game_instance.update()
            self.game_instance.draw()

            pygame.mixer.music.load(self.game_instance.race_music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)

        self.globaltimer = pygame.time.get_ticks()
        self.round_active = True
        self.player1_finished = False
        self.player2_finished = False
        pygame.event.clear()

    def update(self):
        if not self.round_active:
            return None

        now = pygame.time.get_ticks()
        new_goal_to_return = None

        if not self.player1_finished and self.goal_rect.colliderect(self.player1.rect):
            if not self.player1_finished and not self.player2_finished:
                potential_new_goal = self.events.maybe_event_sala()
                if potential_new_goal:
                    self.goal_rect = potential_new_goal.rect
                    new_goal_to_return = potential_new_goal
                else:
                    self.player1_finished = True
                    self.game_instance.sounds['success'].play()
                    self.player1times[self.round_index] = now - self.globaltimer
                    finish_message_p1 = f"Gracz 1 dotarł do celu w {self.player1times[self.round_index] / 1000:.2f}s"
                    if self.game_instance:
                        self.game_instance.add_notification(finish_message_p1, 3, target_player="player1",
                                                            position_topleft=(200, 700))
            else:
                self.player1_finished = True
                self.player1times[self.round_index] = now - self.globaltimer
                finish_message_p1 = f"Gracz 1 dotarł do celu w {self.player1times[self.round_index] / 1000:.2f}s"
                if self.game_instance:
                    self.game_instance.add_notification(finish_message_p1, 3, target_player="player1",
                                                        position_topleft=(200, 700))

        if not self.player2_finished and self.goal_rect.colliderect(self.player2.rect):
            if new_goal_to_return is None:
                if not self.player1_finished and not self.player2_finished:
                    potential_new_goal = self.events.maybe_event_sala()
                    if potential_new_goal:
                        self.goal_rect = potential_new_goal.rect
                        new_goal_to_return = potential_new_goal
                    else:
                        self.player2_finished = True
                        self.game_instance.sounds['success'].play()
                        self.player2times[self.round_index] = now - self.globaltimer
                        finish_message_p2 = f"Gracz 2 dotarł do celu w {self.player2times[self.round_index] / 1000:.2f}s"
                        if self.game_instance:
                            self.game_instance.add_notification(finish_message_p2, 3, target_player="player2",
                                                                position_topleft=(1000, 700))
                else:
                    self.player2_finished = True
                    self.player2times[self.round_index] = now - self.globaltimer
                    finish_message_p2 = f"Gracz 2 dotarł do celu w {self.player2times[self.round_index] / 1000:.2f}s"
                    if self.game_instance:
                        self.game_instance.add_notification(finish_message_p2, 3, target_player="player2",
                                                            position_topleft=(1000, 700))
        if new_goal_to_return:
            self.player1_finished = False
            self.player2_finished = False
            return new_goal_to_return
        if self.player1_finished and self.player2_finished:
            self.end_round()

        return None

    def end_round(self):
        t1 = self.player1times[self.round_index]
        t2 = self.player2times[self.round_index]

        if t1 < t2:
            self.player1points += 1
            round_result_message = "Punkt dla Gracza 1"
        elif t2 < t1:
            self.player2points += 1
            round_result_message = "Punkt dla Gracza 2"
        else:
            round_result_message = "Remis - brak punktów"

        if self.game_instance:
            self.game_instance.add_notification(round_result_message, 3, target_player="global",
                                                position_center=(800, 200))

        self.round_index += 1
        self.round_active = False
        if self.player1points == 2 or self.player2points == 2 or self.round_index >= 3:
            self.end_match()

    def end_match(self):
        self.game_over = True
        final_message = "Koniec gry!"
        if self.game_instance:
            self.game_instance.add_notification(final_message, 3, target_player="global")

        # to dodac do notyfikacji na mega dlugi czas na ekran koncowy jak zostanie zrobiony
        print(f"Gracz 1: {self.player1points} pkt\n"
              f"\tCzasy: \n"
              f"runda 1: {self.player1times[0] / 1000} s\n"
              f"runda 2: {self.player1times[1] / 1000} s\n"
              f"runda 3: {self.player1times[2] / 1000} s\n")
        print(f"Gracz 2: {self.player2points} pkt\n"
              f"\tCzasy: \n"
              f"runda 1: {self.player2times[0] / 1000} s\n"
              f"runda 2: {self.player2times[1] / 1000} s\n"
              f"runda 3: {self.player2times[2] / 1000} s\n")

        if self.player1points > self.player2points:
            print("🥇 Wygrywa Gracz 1!")
            self.game_instance.sounds['game_win'].play()
        elif self.player2points > self.player1points:
            print("🥇 Wygrywa Gracz 2!")
            self.game_instance.sounds['game_win'].play()
        else:
            print("🤝 Remis!")
