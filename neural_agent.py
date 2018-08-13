import tensorflow as tf
import random
from game import Game

class Agent:

    def __init__(self, N, trial=10, cutout_depth=10):
        self.N = N
        self.trial=trial
        self.cutout_depth=cutout_depth
        self.build()

    def build(self):
        input_len = self.N ** 2
        with tf.Graph().as_default():
            self.keep_prob = tf.placeholder(tf.float32)
            self.x  = tf.placeholder(tf.int32, [None, input_len])

            hidden = tf.reshape(tf.one_hot(self.x, 13), [-1, input_len * 13])
            hidden = tf.layers.dense(hidden, input_len * 13, activation=tf.nn.elu)
            hidden = tf.layers.dense(hidden, 100, activation=tf.nn.elu)
            hidden = tf.layers.dense(hidden, 4)
            self.y = tf.argmax(hidden, axis=1)

            self.t = tf.placeholder(tf.int32, [None])

            self.loss = tf.losses.sparse_softmax_cross_entropy(labels=self.t, logits=hidden)
            self.optimize = tf.train.AdamOptimizer(0.001).minimize(self.loss)

            self.sess = tf.Session()
            self.saver = tf.train.Saver()
            self.sess.run(tf.global_variables_initializer())

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
                    game_.step(self.neural_move(game_))
        return sorted(score_dict.items(), key=lambda x: x[1])[-1][0]

    def neural_move(self, game):
        y = self.sess.run(self.y, {self.x: [game.field]})
        direction = y[0]
        if game.step_validate(direction):
            return direction
        return self.random_move(game)

    def random_move(self, game):
        return random.choice(game.candidate_moves())

    def learn(self, records):
        x, t = zip(*records)
        loss, _ = self.sess.run([
            self.loss,
            self.optimize
        ], {
            self.x: x,
            self.t: t
        })
        print('loss: {}'.format(loss))
