import random
import sys
import math
from Messages.Message import Message
from Util.Util import *
from Util.Tangle import *
# import matplotlib.pyplot as plt



class SynIOTAForkAttacker:
    name = "Synchronous IOTA Fork Attacker"

    def __init__(self, **kargs):

        self.env = kargs["env"]
        if self.env.get_f() == 0:
            return
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.input = None
        self.Tangle = Tangle.init_with_fork(self.env.get_seed())
        self.belief = 0
        self.chameleon_dict = {}
        self.my_sites=[]
        self.one_vote_father_id=2
        self.zero_vote_father_id=3
        for node in self.con.node_id.keys():
            id = node.env.get_id(node)
            if self.env.check_corrupt(id):
                self.chameleon_dict[id] = node
        self.represent_id = self.env.get_n() - 1
        self.represent_node = self.chameleon_dict[self.represent_id]
        self.limit = self.con.limit

    def run_node(self):
        running_round = self.env.get_round()
        msgs=self.env.get_input_msgs(self.represent_node)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                raise RuntimeError
            if msg.sender == self.represent_id:
                continue
            new_site = msg.get_extraction().copy()
            if not new_site:
                raise RuntimeError
            self.Tangle.insert_site(new_site)
        for site in self.chameleon_dict.values():
            my_pow=True
            if my_pow:
                new_site = Tangle_Site([], [], self.represent_id,None,[],0)
                self.my_sites.append(new_site)
        weight1=self.Tangle.genesis_site.children_list[0].calculate_cumulative_weight()
        weight0 =self.Tangle.genesis_site.children_list[1].calculate_cumulative_weight()
        if weight0==weight1:
            if len(self.my_sites)>self.limit:
                self.equal_add(running_round)
            return
        else:
            if weight0>weight1:
                indicator=0
            else:
                indicator=1
            delta=abs(weight0-weight1) + round((self.con.n-self.con.tf)*abs(weight0-weight1)/(weight0+weight1))
            for i in range(min(delta,len(self.my_sites))):
                balance_site=self.my_sites.pop()
                balance_site.vote=1-indicator
                balance_site.father_id_list=[2+indicator]
                balance_site.father_list.append(self.Tangle.genesis_site.children_list[indicator])
                balance_site.update_weight()
                signed_site = self.pki.sign(self.represent_node, balance_site)
                self.Tangle.genesis_site.children_list[indicator].children_list.append(signed_site)
                self.env.put_broadcast(self.represent_node, self.pki.sign(
                    self.represent_node, Message(self.represent_id, signed_site, running_round)))
            if len(self.my_sites)>self.limit:
                self.equal_add(running_round)

                
    def receive_messages(self):
        pass
        # msgs = self.env.get_input_msgs(self)
        # for msg in msgs:
        #     if (not self.pki.verify(msg)):
        #         raise RuntimeError
        #     new_site = msg.get_extraction().copy()
        #     if not new_site:
        #         raise RuntimeError
        #     self.Tangle.insert_site(new_site)
        
    def equal_add(self,running_round):
        add_num=math.ceil((len(self.my_sites)-self.limit)/2)
        for i in range(add_num):
            for indicator in range(2):
                balance_site=self.my_sites.pop()
                balance_site.vote=1-indicator
                balance_site.father_id_list=[2+indicator]
                balance_site.father_list.append(self.Tangle.genesis_site.children_list[indicator])
                balance_site.update_weight()
                signed_site = self.pki.sign(self.represent_node, balance_site)
                self.Tangle.genesis_site.children_list[indicator].children_list.append(signed_site)
                self.env.put_broadcast(self.represent_node, self.pki.sign(
                    self.represent_node, Message(self.represent_id, signed_site, running_round)))


