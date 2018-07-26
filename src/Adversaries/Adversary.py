from Messages.Message import *


class CrashAdversary:

    name = "Crash Adversary"
    
    def __init__(self, *args):
        pass
    
    def run_node(self):
        pass


class HalfHalfSenderAdversary:
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
        self.input = self.env.get_input(myid)
        if round == 0:
            for i in range(1, (self.env.get_n() >> 1) + 1):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
            for i in range((self.env.get_n() >> 1) + 1, self.env.get_n()):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, 1 - self.input)), i)
        else:
            self.env.get_input_msgs(self)

            for i in range(1, (self.env.get_n() >> 1) + 1):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
            for i in range((self.env.get_n() >> 1) + 1, self.env.get_n()):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, 1 - self.input)), i)


class SynBOSCOValidityAttacker:
    name = "Synchronous BOSCO Validity Attacker"
    SENDER = 0

    def __init__(self, env, pki):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.input = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        self.input = self.env.get_input(myid)
        if round == 0:
            for i in range(0, 2*self.env.get_f() + 1):
                # self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
                self.env.put_packet(self, Message(myid, self.input), i)
            for i in range(2*self.env.get_f() + 1, self.env.get_n()):
                self.env.put_packet(self, Message(myid, 1 - self.input), i)
        else:
            msgs = self.env.get_input_msgs(self)
            for i in range(0, 2*self.env.get_f() + 1):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, self.input)), i)
            for i in range(2*self.env.get_f() + 1, self.env.get_n()):
                self.env.put_packet(self, self.pki.sign(self, Message(myid, 1 - self.input)), i)


class SynBOSCOValidityCentrolizedAttacker:
    name = "Synchronous BOSCO Validity Centrolized Attacker"
    SENDER = 0

    def __init__(self, env, pki):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.input = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        self.input = self.env.get_input(myid)
        if round == 0:
            for j in range(0, myid+1):
                for i in range(0, 2*self.env.get_f() + 1):
                    self.env.put_packet(self, Message(j, self.input), i)
                for i in range(2*self.env.get_f() + 1, self.env.get_n()):
                    self.env.put_packet(self, Message(j, 1 - self.input), i)
        else:
            msgs = self.env.get_input_msgs(self)
            for j in range(0, myid+1):
                for i in range(0, 2*self.env.get_f() + 1):
                    self.env.put_packet(self, Message(j, self.input), i)
                for i in range(2*self.env.get_f() + 1, self.env.get_n()):
                    self.env.put_packet(self, Message(j, 1 - self.input), i)
