from Messages.Message import *


class CrashAdversary:

    name = "Crash Adversary"

    def __init__(self, *args):
        pass

    def run_node(self):
        pass


class HalfHalfSender:

    name = "Half-half Sender"
    SENDER = 0

    def __init__(self, env, pki):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.input = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            if self.env.get_id(self) == HalfHalfSender.SENDER:
               self.input = self.env.get_input(self)
               for i in range(1, (self.env.get_n() >> 1) + 1):
                    self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
               for i in range((self.env.get_n() >> 1) + 1, self.env.get_n()):
                    self.env.put_packet(self, self.pki.sign(self, Message(myid, 1 - self.input)), i)
        else:
            pass

