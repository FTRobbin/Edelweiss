from Messages.Message import *


class DolevStrongRoundAdversary:

    name = "Round f Adversary"
    adv_pool = []
    SENDER = 0
    MASTER = 0

    @staticmethod
    def clear():
        adv_pool = []


    def __init__(self,**kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        DolevStrongRoundAdversary.adv_pool.append(self)
        self.input = None



    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            if self.env.get_id(self) == DolevStrongRoundAdversary.SENDER:
                for i in range(1, self.env.get_n() - self.env.get_tf() + 1):
                    self.env.put_packet(self, self.pki.sign(self, Message(myid, 1)), i)
        elif round == self.env.get_tf() - 1:
            if self.env.get_id(self) == DolevStrongRoundAdversary.MASTER:
                msg = self.pki.sign(self, Message(myid, 0))
                for node in DolevStrongRoundAdversary.adv_pool:
                    if node is not self:
                        msg = self.pki.sign(node, Message(self.env.get_id(node), msg))
            if self.env.get_id(self) == DolevStrongRoundAdversary.SENDER:
                for i in range(1, self.env.get_n() - self.env.get_tf()):
                    self.env.put_packet(self, msg, i)
        else:
            pass