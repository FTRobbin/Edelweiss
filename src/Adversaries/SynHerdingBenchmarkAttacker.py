import random

from Messages.Message import Message
from Util.Util import *


class SynHerdingBenchmarkAttacker:
    name = "Synchronous Herding Benchmark Attacker"

    def __init__(self, **kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.input = None
        self._lambda = kargs["lambda"]
        self.buckets = [[], []]
        self.bar = self.env.get_k() * self._lambda * self._lambda
        self.my_mine = kargs["mine"]
        self.called = 0
        self.corrupt_node_list = list(
            filter(lambda x: self.env.check_corrupt(x), range(self.env.get_n())))
        self.chameleon_dict = {}
        self.represent = None
        self.represent_id = self.env.get_n()-1
        for node in self.con.node_id.keys():
            if node.env.get_id(node) == self.represent_id:
                self.represent_node = node
                break

    def run_node(self):
        self.called += 1
        if (self.called % self.con.f) != 1:
            return
        round = self.env.get_round()
        if round == 0:
            pass
        elif round < self.bar-1:
            for i in range(2):
                for id in self.corrupt_node_list:
                    my_pow = self.my_mine.POW(round, id, i)
                    if my_pow:
                        new_block = self.pki.sign(
                            self.represent_node, Block(round, id, i))
                        self.buckets[i].append(new_block)
                        break
        elif round == self.bar-1:
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    pass
                else:
                    if self.buckets[i % 2]:
                        self.represent_node.env.put_packet(self.represent_node, self.represent_node.pki.sign(
                            self.represent_node, Message(self.represent_id, self.buckets[i % 2])), i)

        else:
            pass
