import random

from Messages.Message import Message


class Herding:
    name = "Herding Protocol"

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

    def bucket_verify(self, bucket):
        sender_round_set = []
        belief = -1
        round = -1
        for block in bucket:
            if belief == -1:
                belief = block.belief
            elif belief != block.belief:
                return False
            if block.round <= round:
                return False
            round = block.round
            if not self.pki.verify(block):
                return False
            if not self.my_mine.verify(block.round, block.id, block.belief):
                return False
            if (block.round, block.id) in sender_round_set:
                return False
            sender_round_set.append((block.round, block.id))
        return True

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            self.belief = self.env.get_input(myid)
            pass
        elif round <= self.bar:
            msgs = self.env.get_input_msgs(self)
            bucket_lists = [[], []]
            for msg in msgs:
                if (not self.pki.verify(msg)):
                    self.pki.verify(msg)
                    raise RuntimeError
                bucket = msg.get_extraction()
                if not bool(bucket):
                    return
                if self.bucket_verify(bucket):
                    bucket_lists[bucket[0].belief].append(bucket.copy())
            i = 0
            for bucket_list in bucket_lists:
                if bucket_list:
                    self.buckets[i] = max(bucket_list, key=lambda x: len(x))
                i += 1
            l0 = len(self.buckets[0])
            l1 = len(self.buckets[1])
            # print("round %d : id %d belief %d" % (round + 1, myid, self.belief))
            if round != 1:
                if l0 > l1 or (l0 == l1) and random.choice([True, False]):
                    self.belief = 0
                    # print("round %d : id %d belief 0" % (round + 1, myid))
                else:
                    self.belief = 1
                    # print("round %d : id %d belief 1" % (round + 1, myid))
            if round == self.bar:
                self.env.put_output(self, self.belief)
                return
            my_pow = self.my_mine.POW(round, myid, self.belief)
            if my_pow:
                new_block = self.pki.sign(
                    self, Block(round, myid, self.belief))
                self.buckets[self.belief].append(new_block)
                self.env.put_broadcast(self, self.pki.sign(
                    self, Message(myid, (self.buckets[self.belief]).copy(), round)))


class Block:
    def __init__(self, round, id, belief):
        self.round = round
        self.id = id
        self.belief = belief

    def verify(self):
        return True

    def __str__(self):
        return str(self.round) + '-' + str(self.id) + '-' + str(self.belief)

    def get_sender(self):
        return self.id
