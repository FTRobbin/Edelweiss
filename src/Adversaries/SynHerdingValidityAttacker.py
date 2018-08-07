import random

from Messages.Message import Message
from Util.Util import *


class SynHerdingValidityAttacker:
    name = "Synchronous Herding Validity Attacker"

    def __init__(self, **kargs):

        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.input = None
        self._lambda = kargs["lambda"]
        self.buckets = [[], []]
        self.belief = None
        self.bar = 1 * self._lambda * self._lambda
        self.my_mine = kargs["mine"]
        self.pow_info = {}
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
            self.predict_node_belief[i] = random.choice([0, 1])

    def bucket_verify(self, bucket):
        sender_round_set=[]
        belief=-1
        round=-1
        current_round=self.env.get_round()
        for block in bucket:
            if belief == -1:
                belief=block.belief
            elif belief != block.belief:
                return False
            if block.round > current_round:
                return False
            if block.round <= round:
                return False
            round=block.round
            if not self.pki.verify(block):
                self.pki.verify(block)
                return False
            if not self.my_mine.verify(block.round, block.id, block.belief):
                return False
            if (block.round, block.id) in sender_round_set:
                return False
            sender_round_set.append((block.round, block.id))
        return True

    def run_node(self):
        round=self.env.get_round()
        myid=self.env.get_id(self)
        if round == 0:
            self.belief=self.env.get_input(myid)
        elif round < self.bar-1:
            msgs=self.env.get_input_msgs(self)
            bucket_lists=[[], []]

            # mapping from node to the length of max bucket it receives

            for msg in msgs:
                if (not self.pki.verify(msg)):
                    self.pki.verify(msg)
                    raise RuntimeError
                content=msg.get_extraction()
                if type(content) is list:  # receive a bucket
                    if not bool(content):
                        return
                    if self.bucket_verify(content):
                        # msg from broadcast
                        if not self.env.check_corrupt(msg.get_sender()):
                            bucket_lists[content[0].belief].append(
                                content.copy())
                        else:  # msg from adversary
                            self.buckets[content[0].belief]=max(
                                self.buckets[content[0].belief], content.copy(), key = lambda x: len(x))
                else:  # receive a (receiver,bucket) tuple,this msg is from another adversary
                    if not content[1]:
                        raise RuntimeError
                    if self.bucket_verify(content[1]):
                        self.node_receive_bucket_len[content[0]][content[1][0].belief] = max(
                            len(content[1]), self.node_receive_bucket_len[content[0]][content[1][0].belief])
            # msg from broadcast
            if not bucket_lists[0]:
                l0 = -1
            else:
                l0 = len(max(bucket_lists[0], key=lambda x: len(x)))
            if not bucket_lists[1]:
                l1 = -1
            else:
                l1 = len(max(bucket_lists[1], key=lambda x: len(x)))
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    continue
                self.node_receive_bucket_len[i][0] = max(
                    l0, self.node_receive_bucket_len[i][0])
                self.node_receive_bucket_len[i][1] = max(
                    l1, self.node_receive_bucket_len[i][1])
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

            for bucket in self.buckets:
                if bucket:
                    bucket_lists[bucket[0].belief].append(bucket.copy())
            i = 0
            for bucket_list in bucket_lists:
                if bucket_list:
                    self.buckets[i] = max(bucket_list, key=lambda x: len(x))
                i += 1
            for i in range(2):
                my_pow = self.pow_info[(round, myid, i)]
                if my_pow:
                    new_block = self.pki.sign(
                        self, Block(round, myid, i))
                    self.buckets[i].append(new_block)
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
                    for j in range(2):
                        if self.buckets[j] and i != myid:
                            self.env.put_packet(self, self.pki.sign(
                                self, Message(myid, self.buckets[j])), i)
                else:
                    if self.pow_info[(round+1, i, 0)] == 1 and self.pow_info[(round+1, i, 1)] == 1:
                        continue
                    for j in range(2):
                        if self.pow_info[(round+1, i, j)] == 1:
                            if len(self.buckets[1-j]) > max(predict_bucketslen[j], self.node_receive_bucket_len[i][j])+1:
                                stop = max(
                                    predict_bucketslen[j], self.node_receive_bucket_len[i][j])+1
                            else:
                                stop = len(self.buckets[1-j])
                            if self.buckets[1-j][0:stop]:
                                self.env.put_packet(self, self.pki.sign(
                                    self, Message(myid, self.buckets[1-j][0:stop])), i)
                                for k in (self.corrupt_node_list):
                                    if self.buckets[1-j][0:stop]:
                                        self.env.put_packet(self, self.pki.sign(
                                            self, Message(myid, (i, self.buckets[1-j][0:stop]))), k)
        elif round == self.bar-1:
            for i in range(self.env.get_n()):
                if self.env.check_corrupt(i):
                    pass
                else:
                    if self.buckets[i % 2]:
                        self.env.put_packet(self, self.pki.sign(
                            self, Message(myid,  self.buckets[i % 2])), i)

        else:
            pass
