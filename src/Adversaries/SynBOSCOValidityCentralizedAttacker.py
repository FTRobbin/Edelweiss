from Messages.Message import *


class SynBOSCOValidityCentralizedAttacker:
    name = "Synchronous BOSCO Validity centralized Attacker"
    SENDER = 0

    def __init__(self, env, pki, con):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.attack_value = None
        self.called = False
        self.con = con

    def run_node(self):
        if self.called:
            return
        self.called = True
        round = self.env.get_round()
        self.attack_value = 1
        if round == 0:
            for j in range(0, self.env.get_tf()):
                for node in self.con.node_id.keys():
                    if node.env.get_id(node) == j:
                        chameleon = node  # chameleon is used to pretend the corrupt node
                        break
                for i in range(0, self.env.get_f() ):
                    self.env.put_packet(self, self.pki.sign(
                        chameleon, Message(j, self.attack_value)), i)
                for i in range(self.env.get_f() , self.env.get_n()):
                    self.env.put_packet(self, self.pki.sign(
                        chameleon, Message(j, 1 - self.attack_value)), i)
        else:
            pass
