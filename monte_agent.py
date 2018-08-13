import tensorflow as tf
import random
from game import Game

class Agent:

    def __init__(self, N, trial=50, cutout_depth=25):
        self.N = N
        self.trial=trial
        self.cutout_depth=cutout_depth

    def think(self, game):
        dirs = game.candidate_moves()
        score_dict = {dir: 0 for dir in dirs}
        for dir in dirs:
            for _ in range(self.trial):
                game_ = Game(game=game)
                game_.step(dir)
                for i in range(self.cutout_depth):
                    if game_.end():
                        score_dict[dir] += i
                        break
                    game_.step(self.random_move(game_))
        return sorted(score_dict.items(), key=lambda x: x[1])[-1][0]

    def random_move(self, game):
        return random.choice(game.candidate_moves())

    def learn(self, records):
        pass
