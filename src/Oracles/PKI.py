import random


class IdealPKI:

    name = "IdealPKI"

    def __init__(self, env):
        self.env = env
        self.sk = {}
        self.msg_mem = set()
        self.block_mem = set()

    def register(self, id):
        self.sk[id] = random.random()
        return self.sk[id]

    def sign(self, sk, info):
        if (self.env.get_id(sk) != info.get_sender()) and ((type(info) is Message) and (type(info.get_content()) is not Message or self.verify(info.get_content()))):
            raise RuntimeError
        if type(info) is Message:
            self.msg_mem.add(info.__str__())
        elif type(info) is Block:
            self.block_mem.add(info.__str__())
        return info

    def verify(self, info):
        if type(info) is Message:
            return info.__str__() in self.msg_mem
        elif type(info) is Block:
            return info.__str__() in self.block_mem


from Messages.Message import Message
from Protocols.Herding import Block
