import random

from Messages.Message import Message
from Util.Util import *
from Util.Forest import *


class Nakamoto:
    name = "Nakamoto Protocol"

    def __init__(self, **kargs):
        self.genesis_block = Nakamoto_Block.get_genesis_block()
        self.block_forest = Forest(self.genesis_block)
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)

    def receive_block(self):
        myid = self.env.get_id(self)
        msg = self.env.get_input_msg(self)
        if not msg:
            return
        if (not self.pki.verify(msg)):
            self.pki.verify(msg)
            raise RuntimeError
        block = msg.get_extraction()
        # block_set.add(block)
        if self.block_forest.block_is_in(block):
            return
        self.block_forest.insert(block)
        self.env.put_broadcast(self, myid, self.pki.sign(
            self, Message(myid, block, round)))

    def mine_block(self):
        myid = self.env.get_id(self)
        new_block = Nakamoto_Block(
            self.block_forest.query_max_depth_block_id())
        self.block_forest.insert(new_block)
        self.env.put_broadcast(self, myid, self.pki.sign(
            self, Message(myid, new_block, round)))
        # self.env.put_broadcast(self,myid, self.pki.sign(self, Message(myid, new_block, round)))

    def put_output(self):
        self.env.put_output(self, ContentToString(
            self.block_forest.get_chain()))
        # self.env.put_output(self,len(self.block_forest.get_longest_chain()))
