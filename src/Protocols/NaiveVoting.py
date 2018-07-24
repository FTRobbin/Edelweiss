from Messages.Message import Message


class NaiveVoting:

    name = "Naive Voting Protocol"
    SENDER = 0

    def __init__(self, env, pki, sk):
        self.env = env
        self.pki = pki
        self.sk = sk
        self.input = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self.sk)
        if round == 0:
            if myid == NaiveVoting.SENDER:
                self.input = self.env.get_input(self.sk)
                self.env.put_broadcast(self.sk, self.pki.sign(self.sk, Message(myid, self.input)))
        elif round == 1:
            msgs = self.env.get_input_msgs(self.sk)
            for msg in msgs:
                if self.pki.verify(msg) and msg.get_sender() == NaiveVoting.SENDER and (msg.get_extraction() == 0 or msg.get_extraction() == 1):
                    self.env.put_broadcast(self.sk, self.pki.sign(self.sk, Message(myid, msg)))
        elif round == 2:
            msgs = self.env.get_input_msgs(self.sk)
            seen = set()
            cnt = [0, 0]
            for msg in msgs:
                if self.pki.verify(msg) and (msg.get_sender() not in seen) and (msg.get_extraction() == 0 or msg.get_extraction() == 1):
                    seen.add(msg.get_sender())
                    cnt[msg.get_extraction()] += 1
            bar = self.env.get_n() * 2 / 3
            if cnt[0] >= bar:
                self.env.put_output(self.sk, 0)
            elif cnt[1] >= bar:
                self.env.put_output(self.sk, 1)
            else:
                self.env.put_output(self.sk, None)
        else:
            raise RuntimeError
