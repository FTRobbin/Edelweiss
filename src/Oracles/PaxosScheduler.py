from src.Messages.Message import Message
from src.Protocols.Paxos import PaxosMsg

import random

class PaxosScheduler:

    def __init__(self, n, seed=None, ddos_adv=None):
        random.seed(seed)
        self.n = n
        self.adv = ddos_adv

    # Simple random scheduler
    def schedule(self, msg_pool):
        # if no messages, choose a leader
        # send a random message otherwise
        bak = []
        for id in range(0, self.n):
            if self.adv is None or not self.adv.is_target(id):
                for msg in msg_pool[id]:
                    bak.append((id, msg))
        if len(bak) == 0:
            while True:
                id = random.randint(0, self.n - 1)
                if self.adv is None or not self.adv.is_target(id):
                    break
            msg = Message(None, [PaxosMsg.INIT, random.choice([0, 1, 2, 3])])
        else:
            id, msg = random.choice(bak)
        return id, msg
