import random
import sys

class Mine:
    def __init__(self, _lambda, seed=None):
        self.memory = {}
        self._lambda = _lambda
        # seed = random.randrange(sys.maxsize)
        # rng = random.seed(8624404103361372903)
        random.seed(seed)
        # print("Seed was:", seed)

    def POW(self, round, id, belief):
        if (round, id, belief) in self.memory.keys():
            return self.memory[(round, id, belief)]
        self.memory[(round, id, belief)] = (
            random.randint(1, self._lambda) == 1)
        # id<1)
        return self.memory[(round, id, belief)]

    def verify(self, round, id, belief):
        if (round, id, belief) not in self.memory.keys():
            return False
        return self.memory[(round, id, belief)] == True

    def set_seed(self, seed):
        random.seed(seed)
