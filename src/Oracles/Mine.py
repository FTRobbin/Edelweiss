import random
import sys

class Mine:
    def __init__(self, _lambda, seed=None,n=1):
        self.memory = {}
        self._lambda = _lambda
        self.n=n
        random.seed(seed)

    def POW(self, round, id, belief):
        if (round, id, belief) in self.memory.keys():
            return self.memory[(round, id, belief)]
        self.memory[(round, id, belief)] = (
            random.randint(1,self.n * self._lambda) == 1)
        # id<1)
        return self.memory[(round, id, belief)]

    def set_seed(self, seed):
        random.seed(seed)
