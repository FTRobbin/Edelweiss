import random

from Messages.Message import Message
from Util.Util import *


class HerdingWithBroadcast:
    name = "Herding Protocol with Broadcast"

    def __init__(self, **kargs):

        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.input = None
        self._lambda = kargs["lambda"]
        self.buckets = [[], []]
        self.belief = None
        self.bar = self.env.get_k() * self._lambda * self._lambda
        self.my_mine = kargs["mine"]

    def bucket_verify(self, bucket):
        belief = -1
        round = -1
        current_round = self.env.get_round()
        for block in bucket:
            if belief == -1:
                belief = block.belief
            elif belief != block.belief:
                return False
            if block.round > current_round:
                return False
            if block.round <= round:
                return False
            round = block.round
            if not self.pki.verify(block):
                return False
            if not self.my_mine.POW(block.round, block.id, block.belief):
                return False
        return True

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            self.belief = self.env.get_input(myid)
        elif round <= self.bar:
            msgs = self.env.get_input_msgs(self)
            bucket_lens = [len(self.buckets[0]), len(self.buckets[1])]
            for msg in msgs:
                if (not self.pki.verify(msg)):
                    self.pki.verify(msg)
                    raise RuntimeError
                bucket = msg.get_extraction()
                if not bool(bucket):
                    bool(bucket)
                    raise RuntimeError
                if self.bucket_verify(bucket):
                    if bucket:
                        self.buckets[bucket[0].belief] = max(self.buckets[bucket[0].belief],bucket.copy(),key=lambda x:len(x))
            l0 = len(self.buckets[0])
            l1 = len(self.buckets[1])
            if  l0 != 0 or l1 != 0:
                if (l0 > l1) or (l0 == l1):
                    self.belief = 0
                else:
                    self.belief = 1
            if round == self.bar:
                self.env.put_output(self, self.belief)
                return
            my_pow = self.my_mine.POW(round, myid, self.belief)
            if my_pow:
                new_block = self.pki.sign(
                    self, Block(round, myid, self.belief))
                self.buckets[self.belief].append(new_block)
            for bucket in self.buckets:
                if bucket:
                    if len(bucket)>bucket_lens[bucket[0].belief]:
                        self.env.put_broadcast(self, self.pki.sign(
                            self, Message(myid, bucket.copy(), round)))
