from src.Messages.Message import Message
from src.Protocols.Paxos import PaxosMsg

class FigPaxos:

    name = "FigPaxos Protocol"

    def __init__(self, **kwargs):
        self.env = kwargs['env']
        self.n = self.env.get_n()
        self.id = -1
        self.current_belief = None
        self.current_ballots = {}
        self.maximum_ballot_no = (-1, -1)
        self.last_accepted = None
        self.last_accepted_ballot_no = (-1, -1)
        self.current_proposals = {}
        self.current_proposal_ballot_nos = {}
        self.reply_lists = {}
        self.accept_counts = {}
        self.decision = None

    # Received some msg
    def recv(self, msg):
        self.id = self.env.get_id(self)
        msgtype = msg.get_extraction()[0]
        if msgtype is PaxosMsg.INIT:
            self.init_ballot(msg)
        elif msgtype is PaxosMsg.PREPARE:
            self.prepare(msg)
        elif msgtype is PaxosMsg.REPLY:
            self.reply(msg)
        elif msgtype is PaxosMsg.PROPOSE:
            self.propose(msg)
        elif msgtype is PaxosMsg.ACCEPT:
            self.accept(msg)
        elif msgtype is PaxosMsg.DECIDE:
            self.decide(msg)
        else:
            raise RuntimeError

    # I am the leader to initiate a new ballot
    def init_ballot(self, msg):
        new_ballot_no = (self.maximum_ballot_no[0] + 1, self.id)
        if self.last_accepted is None:
            new_proposal = msg.get_extraction()[1]
        else:
            new_proposal = self.last_accepted
        new_msg = Message(self.id, [PaxosMsg.PREPARE, new_ballot_no, new_proposal])
        if self.current_belief != new_proposal:
            self.current_ballots.clear()
            self.current_belief = new_proposal
        self.maximum_ballot_no = new_ballot_no
        self.current_ballots[new_ballot_no] = None
        self.current_proposals[new_ballot_no] = msg.get_extraction()[1]
        self.current_proposal_ballot_nos[new_ballot_no] = (-1, -1)
        self.reply_lists[new_ballot_no] = []
        self.env.put_broadcast(self, self.id, new_msg)

    # Received a prepare message
    def prepare(self, msg):
        ballot_no = msg.get_extraction()[1]
        assumption = msg.get_extraction()[2]
        if ballot_no <= self.maximum_ballot_no:
            if assumption == self.current_belief:
                if ballot_no not in self.current_ballots:
                    self.current_ballots[ballot_no] = None
                new_msg = Message(self.id, [PaxosMsg.REPLY, ballot_no, self.last_accepted, self.last_accepted_ballot_no])
                self.env.put_packet(self, self.id, new_msg, msg.get_sender())
        else:
            if assumption != self.current_belief:
                self.current_ballots.clear()
                self.current_belief = assumption
            self.maximum_ballot_no = ballot_no
            self.current_ballots[ballot_no] = None
            new_msg = Message(self.id, [PaxosMsg.REPLY, ballot_no, self.last_accepted, self.last_accepted_ballot_no])
            self.env.put_packet(self, self.id, new_msg, msg.get_sender())

    # Received a reply message
    def reply(self, msg):
        content = msg.get_extraction()
        ballot_no = content[1]
        last_acc = content[2]
        last_acc_no = content[3]
        if ballot_no in self.current_ballots:
            if len(self.reply_lists[ballot_no]) * 2 <= self.n:
                if self.current_proposal_ballot_nos[ballot_no] < last_acc_no:
                    self.current_proposals[ballot_no] = last_acc
                    self.current_proposal_ballot_nos[ballot_no] = last_acc_no
                self.reply_lists[ballot_no].append(msg.get_sender())
                if len(self.reply_lists[ballot_no]) * 2 > self.n:
                    if self.current_proposals[ballot_no] != self.current_belief:
                        self.current_ballots.pop(ballot_no)
                    else:
                        self.accept_counts[ballot_no]= 0
                        new_msg = Message(self.id, [PaxosMsg.PROPOSE, ballot_no])
                        for id in self.reply_lists[ballot_no]:
                            self.env.put_packet(self, self.id, new_msg, id)

    # Received a propose message
    def propose(self, msg):
        content = msg.get_extraction()
        ballot_no = content[1]
        if ballot_no in self.current_ballots:
            new_msg = Message(self.id, [PaxosMsg.ACCEPT, ballot_no])
            if self.last_accepted_ballot_no is None or ballot_no > self.last_accepted_ballot_no:
                self.last_accepted = self.current_belief
                self.last_accepted_ballot_no = ballot_no
            self.env.put_packet(self, self.id, new_msg, msg.get_sender())

    # Received an accept message
    def accept(self, msg):
        ballot_no = msg.get_extraction()[1]
        if ballot_no in self.current_ballots:
            self.accept_counts[ballot_no] += 1
            if self.accept_counts[ballot_no] == len(self.reply_lists[ballot_no]):
                new_msg = Message(self.id, [PaxosMsg.DECIDE, self.current_belief])
                self.env.put_broadcast(self, self.id, new_msg)

    # Received a decide message
    def decide(self, msg):
        proposal = msg.get_extraction()[1]
        if self.decision is not None and self.decision is not proposal:
            raise RuntimeError
        if self.decision is None:
            self.decision = proposal
            self.env.put_output(self, proposal)
