class SynByzEnvironment:

    name = "Synchronous Byzantine Environment"

    def __init__(self, con):
        self.controller = con

    def get_n(self):
        return self.controller.n

    def get_f(self):
        return self.controller.f

    def get_tf(self):
        return self.controller.tf

    def get_round(self):
        return self.controller.round

    def get_id(self, sk):
        return self.controller.node_id[sk]

    def get_input(self, node):
        if type(self.controller.input) is list:
            return self.controller.input[node]
        else:
            return self.controller.input

    def get_input_msgs(self, sk):
        return self.controller.get_message_buffer(sk)

    def put_broadcast(self, sk, msg):
        self.controller.put_broadcast(msg)

    def put_packet(self, sk, msg, target):
        self.controller.put_packet(msg, target)

    def put_output(self, sk, output):
        self.controller.put_output(sk, output)
