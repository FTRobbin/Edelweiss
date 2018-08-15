from Messages.Message import *


class SynBOSCOAgreementAttacker:
    name = "Synchronous BOSCO Agreement Attacker"
    SENDER = 0

    def __init__(self,**kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.attack_value = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        self.attack_value = self.env.get_input(myid)
        if round == 0:
            for i in range(0, self.env.get_f()):
                self.env.put_packet(self, self.pki.sign(
                    self, Message(myid, self.attack_value)), i)
                # self.env.put_packet(self, Message(myid, self.attack_value), i)
            for i in range(self.env.get_f(), self.env.get_n()):
                self.env.put_packet(self, self.pki.sign(
                    self, Message(myid, 1 - self.attack_value)), i)
        else:
            pass
