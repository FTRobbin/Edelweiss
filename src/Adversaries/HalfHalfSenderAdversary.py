from Messages.Message import *


class HalfHalfSenderAdversary:
    name = "Half-half Sender"
    SENDER = 0

    def __init__(self,**kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.attack_value = None

    # def run_node(self):
    #     round = self.env.get_round()
    #     myid = self.env.get_id(self)
    #     self.attack_value = self.env.get_input(myid)
    #     if round == 0:
    #         for i in range(1, (self.env.get_n() >> 1) + 1):
    #             self.env.put_packet(self, self.pki.sign(
    #                 self, Message(myid, self.attack_value)), i)
    #         for i in range((self.env.get_n() >> 1) + 1, self.env.get_n()):
    #             self.env.put_packet(self, self.pki.sign(
    #                 self, Message(myid, 1 - self.attack_value)), i)
    #     else:
    #         pass

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            if self.env.get_id(self) == HalfHalfSenderAdversary.SENDER:
               self.input = self.env.get_input(self)
               for i in range(1, (self.env.get_n() >> 1) + 1):
                    self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
               for i in range((self.env.get_n() >> 1) + 1, self.env.get_n()):
                    self.env.put_packet(self, self.pki.sign(self, Message(myid, 1 - self.input)), i)
        else:
            pass