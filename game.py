import random

class Game:

    N = 4

    def __init__(self, game=None):
        if game:
            self.field = [*game.field]
            self.score = game.score
            return

        self.field = [0 for _ in range(self.N * self.N)]
        self.score = 0
        self._spawn()

    def step_validate(self, direction):
        field, score = self._step(direction)
        return field != self.field

    def step(self, direction):
        self.field, score = self._step(direction)
        self.score += score
        self._spawn()

    def end(self):
        return all(x != 0 for x in self.field) and \
            not self.step_validate(0) and \
            not self.step_validate(1) and \
            not self.step_validate(2) and \
            not self.step_validate(3)

    def candidate_moves(self):
        return [
            direction
            for direction in range(4)
            if self.step_validate(direction)
        ]

    def _step(self, direction):
        field = [0 for _ in range(self.N * self.N)]
        score = 0
        if direction == 0: # up
            for column in range(self.N):
                r = -1
                last_panel = 0
                for row in range(self.N):
                    panel = self.field[row * self.N + column]
                    if panel > 0:
                        if panel == last_panel:
                            field[r * self.N + column] = panel + 1
                            last_panel = 0
                            score += 2 ** panel
                        else:
                            r += 1
                            field[r * self.N + column] = panel
                            last_panel = panel
        if direction == 1: # left
            for row in range(self.N):
                c = -1
                last_panel = 0
                for column in range(self.N):
                    panel = self.field[row * self.N + column]
                    if panel > 0:
                        if panel == last_panel:
                            field[row * self.N + c] = panel + 1
                            last_panel = 0
                            score += 2 ** panel
                        else:
                            c += 1
                            field[row * self.N + c] = panel
                            last_panel = panel
        if direction == 2: # down
            for column in range(self.N):
                r = self.N
                last_panel = 0
                for row in reversed(range(self.N)):
                    panel = self.field[row * self.N + column]
                    if panel > 0:
                        if panel == last_panel:
                            field[r * self.N + column] = panel + 1
                            last_panel = 0
                            score += 2 ** panel
                        else:
                            r -= 1
                            field[r * self.N + column] = panel
                            last_panel = panel
        if direction == 3: # right
            for row in range(self.N):
                c = self.N
                last_panel = 0
                for column in reversed(range(self.N)):
                    panel = self.field[row * self.N + column]
                    if panel > 0:
                        if panel == last_panel:
                            field[row * self.N + c] = panel + 1
                            last_panel = 0
                            score += 2 ** panel
                        else:
                            c -= 1
                            field[row * self.N + c] = panel
                            last_panel = panel
        return field, score

    def _spawn(self):
        self.field[
            random.choice([
                i
                for i, x in enumerate(self.field)
                if x == 0
            ])
        ] = random.choice([1, 1, 1, 2])

    def print(self):
        print('score: {:>4}'.format(self.score))
        for row in range(self.N):
            for column in range(self.N):
                panel = self.field[row * self.N + column]
                if panel > 0:
                    print('[{:>4}]'.format(2 ** panel), end='')
                else:
                    print('[    ]', end='')
            print()
