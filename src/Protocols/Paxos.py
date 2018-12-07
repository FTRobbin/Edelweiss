from src.Messages.Message import Message

from enum import Enum

class PaxosMsg(Enum):
    INIT = 1
    PREPARE = 2
    REPLY = 3
    PROPOSE = 4
    ACCEPT = 5
    DECIDE = 6

class Paxos:

    name = "Paxos Protocol"

    def __init__(self, **kwargs):
        self.env = kwargs['env']
        self.n = self.env.get_n()
        self.id = -1
        self.current_ballot = (-1, -1)
        self.last_accepted = None
        self.last_accepted_ballot_no = (-1, -1)
        self.current_proposal = None
        self.current_proposal_ballot_no = None
        self.reply_list = []
        self.accept_count = None
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
        new_ballot_no = (self.current_ballot[0] + 1, self.id)
        new_msg = Message(self.id, [PaxosMsg.PREPARE, new_ballot_no])
        self.current_ballot = new_ballot_no
        self.current_proposal = msg.get_extraction()[1]
        self.current_proposal_ballot_no = (-1, -1)
        self.reply_list = []
        # TODO: use quorum?
        self.env.put_broadcast(self, self.id, new_msg)

    # Received a prepare message
    def prepare(self, msg):
        ballot_no = msg.get_extraction()[1]
        if self.current_ballot <= ballot_no:
            self.current_ballot = ballot_no
            new_msg = Message(self.id, [PaxosMsg.REPLY, ballot_no, self.last_accepted, self.last_accepted_ballot_no])
            self.env.put_packet(self, self.id, new_msg, msg.get_sender())

    # Received a reply message
    def reply(self, msg):
        content = msg.get_extraction()
        ballot_no = content[1]
        last_acc = content[2]
        last_acc_no = content[3]
        if self.current_ballot == ballot_no:
            if len(self.reply_list) * 2 <= self.n:
                if self.current_proposal_ballot_no < last_acc_no:
                    self.current_proposal = last_acc
                    self.current_proposal_ballot_no = last_acc_no
                self.reply_list.append(msg.get_sender())
                if len(self.reply_list) * 2 > self.n:
                    self.accept_count = 0
                    new_msg = Message(self.id, [PaxosMsg.PROPOSE, ballot_no, self.current_proposal])
                    for id in self.reply_list:
                        self.env.put_packet(self, self.id, new_msg, id)

    # Received a propose message
    def propose(self, msg):
        content = msg.get_extraction()
        ballot_no = content[1]
        proposal = content[2]
        if self.current_ballot == ballot_no:
            new_msg = Message(self.id, [PaxosMsg.ACCEPT, ballot_no])
            self.last_accepted = proposal
            self.last_accepted_ballot_no = ballot_no
            self.env.put_packet(self, self.id, new_msg, msg.get_sender())

    # Received an accept message
    def accept(self, msg):
        ballot_no = msg.get_extraction()[1]
        if ballot_no == self.current_ballot:
            self.accept_count += 1
            if self.accept_count == len(self.reply_list):
                new_msg = Message(self.id, [PaxosMsg.DECIDE, self.current_proposal])
                self.env.put_broadcast(self, self.id, new_msg)

    # Received a decide message
    def decide(self, msg):
        proposal = msg.get_extraction()[1]
        if self.decision is not None and self.decision is not proposal:
            raise RuntimeError
        if self.decision is None:
            self.decision = proposal
            self.env.put_output(self, proposal)
