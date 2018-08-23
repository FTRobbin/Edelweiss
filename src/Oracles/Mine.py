import random
import sys


class Mine:
    def __init__(self, _lambda, k, n, seed=None):
        self.memory = {}
        if _lambda == -1:
            return
        self.n = n
        self.bar = k * _lambda * _lambda
        random.seed(seed)
        self.memory = [[[random.randint(1, n * _lambda) == 1 for k in range(2)]
                        for j in range(self.n)] for i in range(self.bar)]

    def POW(self, round, id, belief):
        if round >= self.bar or id >= self.n or belief not in [0, 1]:
            raise RuntimeError
        return self.memory[round][id][belief]

    def set_seed(self, seed):
        random.seed(seed)
