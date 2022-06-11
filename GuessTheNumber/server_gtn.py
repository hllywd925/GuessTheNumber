import random
import time


class GuessTheNumber:
    def __init__(self, server, player):
        self.server = server
        self.run = False
        self.player = player  # liste mit Spieler wird vom Server übergeben (alle Angemeldeten) alle müssen mitmachen
        self.guesses = 0

    def start(self):
        da_fuckin_numba = random.randint(1, 100)
        needed = len(self.player)
        while True:
            print(f'{self.guesses} von {needed} Schätzungen abgegeben.')  # der gamethread, hier gehts weiter
            if self.guesses == needed:
                break
            time.sleep(2)
        for g in self.player:
            if g.guess >= da_fuckin_numba:
                g.diff = g.guess - da_fuckin_numba
            else:
                g.diff = da_fuckin_numba - g.guess
        pimmel = 1000
        winner = None
        win_diff = None
        for d in self.player:
            if d.diff < pimmel:
                pimmel = d.diff
                winner = d.name
                win_guess = d.guess

        self.server.end_gtn(da_fuckin_numba, winner, win_guess)

    def who_is_the_winner(self):
        pass
