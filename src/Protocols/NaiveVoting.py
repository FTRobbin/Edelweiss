from Messages.Message import Message


class NaiveVoting:
    name = "Naive Voting Protocol"
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
            if self.env.get_id(self) == NaiveVoting.SENDER:
                self.input = self.env.get_input(self)
                self.env.put_broadcast(self, self.pki.sign(
                    self, Message(myid, self.input)))
        elif round == 1:
            msgs = self.env.get_input_msgs(self)
            for msg in msgs:
                if self.pki.verify(msg) and msg.get_sender() == NaiveVoting.SENDER and (
                        msg.get_extraction() == 0 or msg.get_extraction() == 1):
                    self.env.put_broadcast(
                        self, self.pki.sign(self, Message(myid, msg)))
        elif round == 2:
            msgs = self.env.get_input_msgs(self)
            seen = set()
            cnt = [0, 0]
            for msg in msgs:
                if self.pki.verify(msg) and (msg.get_sender() not in seen) and (
                        msg.get_extraction() == 0 or msg.get_extraction() == 1):
                    seen.add(msg.get_sender())
                    cnt[msg.get_extraction()] += 1
            bar = self.env.get_n() * 2 / 3
            if cnt[0] >= bar:
                self.env.put_output(self, 0)
            elif cnt[1] >= bar:
                self.env.put_output(self, 1)
            else:
                self.env.put_output(self, None)
        else:
            raise RuntimeError
