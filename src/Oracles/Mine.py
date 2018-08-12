import random
import sys

class Mine:
    def __init__(self, _lambda,k,n,seed=None):
        self.memory = {}
        if _lambda==-1:
            return
        self.n=n
        random.seed(seed)
        for i in range(k*_lambda*_lambda):  # round
            for j in range(n):  # id
                for k in range(2):  # belief
                    self.memory[(i, j, k)] = random.randint(1,n * _lambda) == 1
        


    def POW(self, round, id, belief):
        if (round, id, belief) not in self.memory.keys():
            raise RuntimeError
        return self.memory[(round, id, belief)]

    def set_seed(self, seed):
        random.seed(seed)
