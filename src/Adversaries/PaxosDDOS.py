from src.Protocols.Paxos import PaxosMsg

class PaxosDDOS:

    name = "PaxosDDOS"

    def __init__(self, n):
        self.bar = (n - 1) / 2
        self.attacked = {}
        self.current_cnt = {}
        self.current_leader = None

    def obv_message(self, msg, receiver):
        if msg.get_extraction()[0] is PaxosMsg.REPLY:
            ballot_no = msg.get_extraction()[1]
            if ballot_no not in self.attacked:
                if ballot_no not in self.current_cnt:
                    self.current_cnt[ballot_no] = 0
                self.current_cnt[ballot_no] += 1
                if self.current_cnt[ballot_no] >= self.bar:
                    self.current_leader = receiver
                    self.attacked[ballot_no] = True

    def is_target(self, target):
        return self.current_leader == target
