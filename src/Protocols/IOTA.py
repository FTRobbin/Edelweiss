import random

from Messages.Message import Message
from Util.Util import *
from Util.Tangle import *


class IOTA:
    name = "IOTA Protocol"

    def __init__(self, **kargs):

        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.input = None
        self.Tangle = Tangle.init_with_fork()
        self.belief = 0

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        msgs = self.env.get_input_msgs(self)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                raise RuntimeError
            new_site = msg.get_extraction().copy()
            if not new_site:
                raise RuntimeError
            self.Tangle.insert_site(new_site)
        my_pow=True
        # my_pow = random.choice([True, False])
        if my_pow:
            selected_tips=[]
            while True:
                selected_tips = self.Tangle.random_walk()
                if selected_tips[0].vote==selected_tips[1].vote:
                    break
            if selected_tips[0]==selected_tips[1]:
                del selected_tips[1]
            father_id_list = []
            for tip in selected_tips:
                father_id_list.append(tip.id)
            new_site = self.pki.sign(
                self, Tangle_Site(father_id_list, [], selected_tips[0].vote, myid))
            for tip in selected_tips:
                if new_site in tip.children_list:
                    continue
                tip.children_list.append(new_site)
            self.env.put_broadcast(self, self.pki.sign(
                self, Message(myid, new_site, round)))

    def put_output(self):
        self.env.put_output(self,
                            self.Tangle)

    def receive_messages(self):
        msgs = self.env.get_input_msgs(self)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                raise RuntimeError
            new_site = msg.get_extraction().copy()
            if not new_site:
                raise RuntimeError
            self.Tangle.insert_site(new_site)
