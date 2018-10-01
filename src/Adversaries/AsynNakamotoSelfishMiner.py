import random

from Messages.Message import Message
from Util.Util import *
from Util.Forest import *


class AsynNakamotoSelfishMiner:
    name = "Asynchronous Nakamoto selfish miner"

    def __init__(self, **kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.called = 0
        self.corrupt_node_list = list(
            filter(lambda x: self.env.check_corrupt(x), range(self.env.get_n())))
        self.chameleon_dict = {}
        for node in self.con.node_id.keys():
            id = node.env.get_id(node)
            if self.env.check_corrupt(id):
                self.chameleon_dict[id] = node
        self.public_block_forest = Forest()
        self.private_block_forest = Forest()
        self.private_branch_len = 0
        self.unpublished_len=0
    def receive_block(self,id):
        msg = self.env.get_input_msg(self.chameleon_dict[id])
        if not msg:
            return
        block = msg.get_extraction()
        if self.public_block_forest.block_is_in(block):
            return
        delta_prev=len(self.private_block_forest.get_chain())-len(self.public_block_forest.get_chain())
        self.public_block_forest.insert(block)
        if delta_prev==0:
            self.private_block_forest=self.public_block_forest.clone()
            self.private_branch_len=0
            self.unpublished_len=0
        elif delta_prev==1:
            self.env.put_broadcast(self, id, self.pki.sign(
                self.chameleon_dict[id], Message(id, self.private_block_forest.get_chain()[-1], round)))
            self.unpublished_len-=1
        elif delta_prev==2:
            private_chain=self.private_block_forest.get_chain()
            for i in range(self.unpublished_len):
                self.env.put_broadcast(self, id, self.pki.sign(
                    self.chameleon_dict[id], Message(id, private_chain[-1-i], round)))
            self.private_branch_len=0
            self.unpublished_len=0
        else:
            if self.unpublished_len==0:
                # raise RuntimeError
                return
            self.env.put_broadcast(self, id, self.pki.sign(
                self.chameleon_dict[id], Message(id, self.private_block_forest.get_chain()[-self.unpublished_len], round)))
            self.unpublished_len=-1
    def mine_block(self,id):
        delta_prev=len(self.private_block_forest.get_chain())-len(self.public_block_forest.get_chain())
        new_block = Nakamoto_Block(
            self.private_block_forest.query_max_depth_block_id(),miner=id)
        self.env.insert_block(new_block)
        self.private_block_forest.insert(new_block)
        self.private_branch_len+=1
        self.unpublished_len+=1
        private_chain=self.private_block_forest.get_chain()
        if delta_prev==0 and self.private_branch_len==2:
            for i in range(self.unpublished_len):
                self.env.put_broadcast(self, id, self.pki.sign(
                    self.chameleon_dict[id], Message(id, private_chain[-1-i], round)))
            self.private_branch_len=0
            self.unpublished_len=0
    
    def put_output(self):
        self.env.put_output(self, ContentToString(
            self.private_block_forest.get_chain()))

       



            
                

        
        