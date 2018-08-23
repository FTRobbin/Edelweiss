from Messages.Message import Message
from Util.Util import *


class SynHerdingAgreementFast:
    name = "Synchronous Herding Agreement Fast"

    def __init__(self, **kargs):
        self.env = kargs["env"]
        if self.env.get_f() == 0:
            return
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.input = None
        self._lambda = kargs["lambda"]
        self.buckets = [[], []]
        self.bar = self.env.get_k() * self._lambda * self._lambda
        self.my_mine = kargs["mine"]
        self.pow_info = [[[self.my_mine.POW(i, j, k) for k in range(
            2)] for j in range(self.env.get_n())] for i in range(self.bar)]
        self.called = 0
        self.corrupt_node_list = list(
            filter(lambda x: self.env.check_corrupt(x), range(self.env.get_n())))
        self.good_node_list = list(
            filter(lambda x: not self.env.check_corrupt(x), range(self.env.get_n())))
        self.node_receive_bucket_len = {}
        for i in self.good_node_list:
            self.node_receive_bucket_len[i] = [0, 0]
        self.predict_node_belief = {}  # estimate of current belief of every node
        for i in self.good_node_list:
            self.predict_node_belief[i] = self.con.input[i]
        self.chameleon_dict = {}
        for node in self.con.node_id.keys():
            id = node.env.get_id(node)
            if self.env.check_corrupt(id):
                self.chameleon_dict[id] = node
        self.represent_id = self.env.get_n() - 1
        self.represent_node = self.chameleon_dict[self.represent_id]
        self.bak_len = [0, 0]

    def run_node(self):
        if self.env.get_f() == 0:
            return
        self.called += 1
        if (self.called % self.con.f) != 1:
            return
        round = self.env.get_round()
        if round == 0:
            pass
        elif round < self.bar:
            current_buckets = [[], []]
            msgs = self.env.get_input_msgs(self.represent_node)
            for chameleon in self.chameleon_dict.values():
                self.env.get_input_msgs(chameleon)
            for msg in msgs:
                bucket = msg.get_extraction()
                if not bucket:
                    raise RuntimeError
                b = bucket[0].belief
                if len(bucket) > len(current_buckets[b]):
                    current_buckets[b] = bucket
            l = [len(current_buckets[0]), len(current_buckets[1])]
            for i in self.good_node_list:
                for j in range(2):
                    self.node_receive_bucket_len[i][j] = max(
                        l[j], self.node_receive_bucket_len[i][j])
            for i in range(2):
                if len(current_buckets[i]) > len(self.buckets[i]):
                    self.buckets[i] = current_buckets[i]
            for i in self.good_node_list:
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
                    my_pow = self.pow_info[round][id][i]
                    if my_pow:
                        new_block = self.pki.sign(
                            self.represent_node, Block(round, id, i))
                        self.buckets[i] = self.buckets[i].copy()
                        self.buckets[i].append(new_block)
                        break
            # the max len of the bucket that all honest nodes will receive in next round
            predict_bucketslen = self.bak_len
            for i in self.good_node_list:
                b = self.predict_node_belief[i]
                if self.pow_info[round][i][b]:
                    predict_bucketslen[b] = max(
                        predict_bucketslen[b], self.node_receive_bucket_len[i][b] + 1)
            for i in self.good_node_list:
                self.node_receive_bucket_len[i][0] = max(
                    self.node_receive_bucket_len[i][0], predict_bucketslen[0])
                self.node_receive_bucket_len[i][1] = max(
                    self.node_receive_bucket_len[i][1], predict_bucketslen[1])
                if self.node_receive_bucket_len[i][0] == 0 and self.node_receive_bucket_len[i][1] == 0:
                    continue
                if self.node_receive_bucket_len[i][0] >= self.node_receive_bucket_len[i][1]:
                    self.predict_node_belief[i] = 0
                else:
                    self.predict_node_belief[i] = 1
            if round < self.bar - 1:
                for i in self.good_node_list:
                    b = self.predict_node_belief[b]
                    tosend = []
                    if b == 0 and self.pow_info[round + 1][i][0] == 1 and self.pow_info[round + 1][i][1] == 0:
                        if len(self.buckets[1]) > self.node_receive_bucket_len[i][0]:
                            tosend = self.buckets[1][:self.node_receive_bucket_len[i][0] + 1]
                    elif b == 1 and self.pow_info[round + 1][i][1] == 1 and self.pow_info[round + 1][i][0] == 0:
                        if len(self.buckets[0]) > 0 and len(self.buckets[0]) >= self.node_receive_bucket_len[i][1]:
                            tosend = self.buckets[0][:self.node_receive_bucket_len[i][1]]
                    if tosend:
                        self.represent_node.env.put_packet(self.represent_node, self.represent_node.pki.sign(
                            self.represent_node, Message(self.represent_id, tosend)), i)
                        self.node_receive_bucket_len[i][1 - b] = len(tosend)
                        self.bak_len[1 -
                                     b] = max(self.bak_len[1 - b], len(tosend))
            else:
                can0 = []
                can1 = []
                for i in self.good_node_list:
                    if (len(self.buckets[0]) > 0 and len(self.buckets[0]) >= self.node_receive_bucket_len[i][1]) or self.predict_node_belief[i] == 0:
                        can0.append(i)
                    if len(self.buckets[1]) > self.node_receive_bucket_len[i][0] or self.predict_node_belief[i] == 1:
                        can1.append(i)
                if can0 and can1:
                    flag = False
                    for t0 in can0:
                        for t1 in can1:
                            if t0 != t1:
                                if self.predict_node_belief[t0] == 1:
                                    self.represent_node.env.put_packet(self.represent_node, self.represent_node.pki.sign(
                                        self.represent_node, Message(self.represent_id, self.buckets[0])), t0)
                                if self.predict_node_belief[t1] == 0:
                                    self.represent_node.env.put_packet(self.represent_node, self.represent_node.pki.sign(
                                        self.represent_node, Message(self.represent_id, self.buckets[1])), t1)
                                flag = True
                                break
                        if flag:
                            break
