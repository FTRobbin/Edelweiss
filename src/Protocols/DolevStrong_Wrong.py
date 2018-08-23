from Messages.Message import Message
from Protocols.DolevStrong import *


class DolevStrong_Wrong:

    name = "Dolev-Strong Protocol (Wrongly Modified)"
    SENDER = 0

    def __init__(self, **kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.input = None
        self.seen = [False, False]

    def my_verify(self, round, msg):
        sigs = []
        mark = set()
        tmp = msg
        for i in range(round):
            if type(tmp) is not Message:
                return False
            s = tmp.get_sender()
            sigs.append(s)
            tmp = tmp.get_content()
            if s in mark:
                return False
            mark.add(s)
        if sigs[-1] != DolevStrong.SENDER:
            return False
        return True

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            if self.env.get_id(self) == DolevStrong.SENDER:
                self.input = self.env.get_input(self)
                self.env.put_broadcast(self, self.pki.sign(
                    self, Message(myid, self.input)))
                self.seen[self.input] = True
        elif 1 <= round <= self.env.get_tf():
            msgs = self.env.get_input_msgs(self)
            for msg in msgs:
                if self.pki.verify(msg) and self.my_verify(round, msg):
                    b = msg.get_extraction()
                    if (b == 0 or b == 1) and not self.seen[b]:
                        self.seen[b] = True
                        self.env.put_broadcast(
                            self, self.pki.sign(self, Message(myid, msg)))
            if round == self.env.get_tf():
                if self.seen[1] and not self.seen[0]:
                    self.env.put_output(self, 1)
                else:
                    self.env.put_output(self, 0)
        else:
            raise RuntimeErro
