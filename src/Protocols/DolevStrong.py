from Messages.Message import Message


class DolevStrong:

    name = "Dolev-Strong Protocol"
    SENDER = 0

    def __init__(self, env, pki, sk):
        self.env = env
        self.pki = pki
        self.sk = sk
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
        myid = self.env.get_id(self.sk)
        if round == 0:
            if myid == DolevStrong.SENDER:
                self.input = self.env.get_input(self.sk)
                self.env.put_broadcast(self.sk, self.pki.sign(self.sk, Message(myid, self.input)))
                self.seen[self.input] = True
        elif 1 <= round <= self.env.get_f() + 1:
            msgs = self.env.get_input_msgs(self.sk)
            for msg in msgs:
                if self.pki.verify(msg) and self.my_verify(round, msg):
                    b = msg.get_extraction()
                    if (b == 0 or b == 1) and not self.seen[b]:
                        self.seen[b] = True
                        self.env.put_broadcast(self.sk, self.pki.sign(self.sk, Message(myid, msg)))
            if round == self.env.get_f() + 1:
                if self.seen[1] and not self.seen[0]:
                    self.env.put_output(self.sk, 1)
                else:
                    self.env.put_output(self.sk, 0)
        else:
            raise RuntimeError
