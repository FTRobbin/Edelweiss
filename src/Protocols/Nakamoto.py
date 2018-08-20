import random

from Messages.Message import Message
from Util.Util import *
from Util.Forest import *


class Nakamoto:
    name = "Nakamoto Protocol"

    def __init__(self, **kargs):
        self.genesis_block=Nakamoto_Block.get_genesis_block()
        self.block_forest=Forest({(Tree(self.genesis_block,set()))})
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)

    def get_remaining_msgs(self):
        msgs = self.env.drain_message_buffer(self)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                self.pki.verify(msg)
                raise RuntimeError
            block = msg.get_extraction()
            self.block_forest.insert(block)

        
    def receive_block(self):
        myid = self.env.get_id(self)
        msgs = self.env.get_input_msgs(self)
        block_set=set()
        for msg in msgs:
            if (not self.pki.verify(msg)):
                self.pki.verify(msg)
                raise RuntimeError
            block = msg.get_extraction()
            block_set.add(block)
            self.block_forest.insert(block)
        # for block in block_set:
        #     self.env.put_broadcast(self,myid, self.pki.sign(
        #         self, Message(myid, block, round)))
        
    def mine_block(self):
        myid = self.env.get_id(self)
        tail=self.block_forest.get_forest_tail()
        new_block=Nakamoto_Block(tail.get_node().get_id())
        self.block_forest.insert(new_block)
        self.env.put_broadcast(self,myid,self.pki.sign(self, Message(myid, new_block, round)))
        # self.env.put_broadcast(self,myid, self.pki.sign(self, Message(myid, new_block, round)))
    def put_output(self):
        self.env.put_output(self,ContentToString(self.block_forest.get_longest_chain()))
        # self.env.put_output(self,len(self.block_forest.get_longest_chain()))
        


