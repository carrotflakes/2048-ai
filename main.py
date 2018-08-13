# -*- coding: utf-8 -*-
import tensorflow as tf
from game import Game
from neural_agent import Agent

sess = tf.Session()

def playout(agent, limit=10000):
    game = Game()
    records = []
    while not game.end():
        direction = agent.think(game)
        records.append((game.field, direction))
        game.step(direction)

        limit -= 1
        if limit <= 0:
            break
    return records, game.score

def playout_show(agent):
    game = Game()
    for i in range(1000):
        print(i)
        direction = agent.think(game)
        game.step(direction)
        game.print()
        if game.end():
            break

def main():
    agent = Agent(Game.N)
    for epoch in range(500):
        print(epoch)
        records, score = playout(agent)
        print('score: {}, len: {}'.format(score, len(records)))

        agent.learn(records)
        if epoch % 100 == 99:
            playout_show(agent)

if __name__ == '__main__':
    main()
    #agent = Agent(Game.N)
    #playout_show(agent)
