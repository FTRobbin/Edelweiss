import random


class NakamotoScheduler:
    def __init__(self, n, seed=None):
        random.seed(seed)
        self.n = n
        self.counter = 2
        self.counter2 = 0

    def schedule(self):
        res = []
        res.append(random.randint(0, self.n-1))
        # if random.choice([True, False]):
        # res.append(self.counter%2)
        if self.counter % (self.n+10)==0:
            # res.append(random.randint(0, self.n-1))
            # res.append(self.counter % 3)
            res.append('Mine')
        else:
            # res.append(random.randint(0, self.n-1))
            res.append('Deliver')
        self.counter += 1
        self.counter2 += 1
        return res
