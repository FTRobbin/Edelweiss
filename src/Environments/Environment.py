class SynByzEnvironment:

    name = "Synchronous Byzantine Environment"

    def __init__(self, con):
        self.controller = con

    def get_n(self):
        return self.controller.n

    def get_f(self):
        return self.controller.f

    def get_round(self):
        return self.controller.round

    def get_id(self, sk):
        return self.controller.node_id[sk]

<<<<<<< HEAD
    def get_input(self, node):
        return self.controller.input[node]
=======
    def get_input(self, sk):
        return self.controller.input
>>>>>>> 7a1ca05d6a6fdee0570ebb4de48d0a256ef8ed7d

    def get_input_msgs(self, sk):
        return self.controller.get_message_buffer(sk)

    def put_broadcast(self, sk, msg):
        self.controller.put_broadcast(msg)

    def put_packet(self, sk, msg, target):
        self.controller.put_packet(msg, target)

    def put_output(self, sk, output):
        self.controller.put_output(sk, output)
