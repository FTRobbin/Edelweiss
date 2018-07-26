from Messages.Message import *


class SynBOSCOValidityAttacker:
    name = "Synchronous BOSCO Validity Attacker"
    SENDER = 0

    def __init__(self, env, pki):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.attack_value = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        self.attack_value = self.env.get_input(myid)
        if round == 0:
            for i in range(0, 2 * self.env.get_f() + 1):
                self.env.put_packet(self, self.pki.sign(
                    self, Message(myid, self.attack_value)), i)
                self.env.put_packet(self, Message(myid, self.attack_value), i)
            for i in range(2*self.env.get_f() + 1, self.env.get_n()):
                self.env.put_packet(self, self.pki.sign(
                    self, Message(myid, 1 - self.attack_value)), i)
        else:
            pass
