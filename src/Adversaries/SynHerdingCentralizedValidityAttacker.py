import random

from Messages.Message import Message
from Util.Util import *


class SynHerdingCentralizedValidityAttacker:
    name = "Synchronous Herding Centralized Validity Attacker"

    def __init__(self, **kargs):
        self.env = kargs["env"]
        if self.env.get_f()==0:
            return        
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.input = None
        self._lambda = kargs["lambda"]
        self.buckets = [[], []]
        self.bar = self.env.get_k() * self._lambda * self._lambda
        self.my_mine = kargs["mine"]
        self.pow_info = {}
        self.called = 0
        for i in range(self.bar):  # round
            for j in range(self.env.get_n()):  # id
                for k in range(2):  # belief
                    self.pow_info[(i, j, k)] = self.my_mine.POW(i, j, k)
        self.corrupt_node_list = list(
            filter(lambda x: self.env.check_corrupt(x), range(self.env.get_n())))
        self.node_receive_bucket_len = {}
        for i in range(self.env.get_n()):
            if self.env.check_corrupt(i):
                continue
            self.node_receive_bucket_len[i] = [0, 0]
        self.predict_node_belief = {}  # estimate of current belief of every node
        for i in range(self.env.get_n()):
            if self.env.check_corrupt(i):
                continue
            self.predict_node_belief[i] = self.con.input[i]
        self.chameleon_dict = {}
        self.represent = None
        for i in self.corrupt_node_list:
            for node in self.con.node_id.keys():
                if node.env.get_id(node) == i:
                    # chameleon_dict is a mapping corrupt node i to its corresponding object in controller
                    self.chameleon_dict[i] = node
                    break
        if not self.chameleon_dict:
            raise RuntimeError
        self.represent_id = self.env.get_n()-1
        self.represent_node = self.chameleon_dict[self.represent_id]

    def run_node(self):
        if self.env.get_f()==0:
            return
        self.called += 1
        if (self.called % self.con.f) != 1:
            return
        round = self.env.get_round()
        if round == 0:
            pass
        elif round < self.bar-1:
            current_buckets = [[], []]
            msgs = []
            for chameleon in self.chameleon_dict.values():
                msgs.extend(self.env.get_input_msgs(chameleon))
            for msg in msgs:
                bucket = msg.get_extraction()
                if not bool(bucket):
                    raise RuntimeError
                current_buckets[bucket[0].belief] = max(
                    current_buckets[bucket[0].belief], bucket.copy(), key=lambda x: len(x))
            l = [None, None]
            l[0] = len(current_buckets[0])
            l[1] = len(current_buckets[1])
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    continue
                for j in range(2):
                    self.node_receive_bucket_len[i][j] = max(
                        l[j], self.node_receive_bucket_len[i][j])
            for i in range(2):
                self.buckets[i] = max(current_buckets[i].copy(
                ), self.buckets[i], key=lambda x: len(x))
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    continue
                if self.node_receive_bucket_len[i][0] == 0 and self.node_receive_bucket_len[i][1] == 0:
                    continue
                if self.node_receive_bucket_len[i][0] >= self.node_receive_bucket_len[i][1]:
                    # current belief of node i is 0
                    self.predict_node_belief[i] = 0
                else:
                    # current belief of node i is 1
                    self.predict_node_belief[i] = 1
            for i in range(2):
                for id in self.corrupt_node_list:
                    my_pow = self.pow_info[(round, id, i)]
                    if my_pow:
                        new_block = self.pki.sign(
                            self.represent_node, Block(round, id, i))
                        self.buckets[i].append(new_block)
                        break
            # the max len of the bucket that all honest nodes will receive in next round
            predict_bucketslen = [0, 0]
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    pass
                else:
                    if self.pow_info[(round, i, 0)] and self.predict_node_belief[i] == 0:
                        predict_bucketslen[0] = max(
                            predict_bucketslen[0], self.node_receive_bucket_len[i][0]+1)
                        self.node_receive_bucket_len[i][0] += 1
                    elif self.pow_info[(round, i, 1)] and self.predict_node_belief[i] == 1:
                        predict_bucketslen[1] = max(
                            predict_bucketslen[1], self.node_receive_bucket_len[i][1]+1)
                        self.node_receive_bucket_len[i][1] += 1
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    pass
                else:
                    if self.pow_info[(round+1, i, 0)] == 1 and self.pow_info[(round+1, i, 1)] == 1:
                        continue
                    for j in range(2):
                        if self.pow_info[(round+1, i, j)] == 1:
                            if len(self.buckets[1-j]) >= max(predict_bucketslen[j], self.node_receive_bucket_len[i][j]):
                                stop = max(
                                    predict_bucketslen[j], self.node_receive_bucket_len[i][j])+1-j
                                if self.buckets[1-j][0:stop]:
                                    self.represent_node.env.put_packet(self.represent_node, self.represent_node.pki.sign(
                                        self.represent_node, Message(self.represent_id, self.buckets[1-j][0:stop])), i)
                                    self.node_receive_bucket_len[i][1-j] = max(
                                        stop, self.node_receive_bucket_len[i][1-j])
                            else:
                                pass
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
