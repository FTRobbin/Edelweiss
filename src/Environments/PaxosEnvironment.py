# TODO to be merged with AsynEnvironment

class PaxosEnvironment:

    name = "Paxos Asynchronous Environment"

    def __init__(self, con):
        self.controller = con

    def get_n(self):
        return self.controller.n

    def get_id(self, sk):
        return self.controller.node_id[sk]

    def put_broadcast(self, sk, id, msg):
        self.controller.put_broadcast(id, msg)

    def put_packet(self, sk, id, msg, target):
        self.controller.put_packet(id, msg, target)

    def put_output(self, sk, output):
        self.controller.put_output(sk, output)

