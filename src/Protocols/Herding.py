from Messages.Message import Message
import random


class Herding:

    name = "Herding Protocol"

    def __init__(self, env, pki, _lambda=10):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.input = None
        self._lambda = _lambda
        self.zero_bucket = []
        self.one_bucket = []
        self.belief = None
        self.bar = random.randint(1, 10) * self._lambda*self._lambda

    def POW(self, round, id, belief):
        return random.randint(1, self._lambda) == 1

    def bucket_verify(self, bucket):
        sender_round_set = []
        for block in bucket:
            if not block.verify():
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
            my_pow = self.POW(round, myid, self.belief)
            if my_pow:
                new_block = Block(round, myid, self.belief)
                if self.belief == 0:
                    self.zero_bucket.append(new_block)
                    self.env.put_broadcast(self, self.pki.sign(
                        self, Message(myid, self.zero_bucket.copy(), round)))
                elif self.belief == 1:
                    self.one_bucket.append(new_block)
                    self.env.put_broadcast(self, self.pki.sign(
                        self, Message(myid, self.one_bucket.copy(), round)))

        elif round <= self.bar:  # < or <=?
            msgs = self.env.get_input_msgs(self)
            zero_bucket_list = []
            one_bucket_list = []
            for msg in msgs:
                if(not self.pki.verify(msg)):
                    self.pki.verify(msg)
                    raise RuntimeError
                bucket = msg.get_extraction()
                if not bool(bucket):
                    # raise RuntimeError
                    return
                if self.bucket_verify(bucket):
                    if bucket[0].belief == 0:
                        zero_bucket_list.append(bucket)
                    else:
                        one_bucket_list.append(bucket)
            my_pow = self.POW(round, myid, self.belief)
            if my_pow:
                new_block = Block(round, myid, self.belief)
                if self.belief == 0:
                    self.zero_bucket.append(new_block)
                    zero_bucket_list.append(self.zero_bucket.copy())
                elif self.belief == 1:
                    self.one_bucket.append(new_block)
                    one_bucket_list.append(self.one_bucket.copy())
            if(zero_bucket_list):
                self.zero_bucket = sorted(
                    zero_bucket_list, key=lambda x: len(x), reverse=True)[0]
            if(one_bucket_list):
                self.one_bucket = sorted(
                    one_bucket_list, key=lambda x: len(x), reverse=True)[0]
            if my_pow:
                if(len(self.zero_bucket) > len(self.one_bucket)):
                    self.belief = 0
                    self.env.put_broadcast(self, self.pki.sign(
                        self, Message(myid, self.zero_bucket.copy(), round)))
                elif(len(self.zero_bucket) < len(self.one_bucket)):
                    self.belief = 1
                    self.env.put_broadcast(self, self.pki.sign(
                        self, Message(myid, self.one_bucket.copy(), round)))
                else:
                    if random.randint(0, 1) == 0:
                        self.belief = 0
                        self.env.put_broadcast(self, self.pki.sign(
                            self, Message(myid, self.zero_bucket.copy(), round)))
                    else:
                        self.belief = 1
                        self.env.put_broadcast(self, self.pki.sign(
                            self, Message(myid, self.one_bucket.copy(), round)))
            else:
                if (len(self.zero_bucket) > len(self.one_bucket)):
                    self.belief = 0
                elif (len(self.zero_bucket) < len(self.one_bucket)):
                    self.belief = 1
                else:
                    if random.randint(0, 1) == 0:
                        self.belief = 0
                    else:
                        self.belief = 1

        else:
            self.env.put_output(self, self.belief)


class Block:
    def __init__(self, round, id, belief):
        self.round = round
        self.id = id
        self.belief = belief

    def verify(self):
        return True

    def __str__(self):
        return str(self.round) + '-' + str(self.id) + '-' + str(self.belief)
