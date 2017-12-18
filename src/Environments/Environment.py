class SynByzEnvironment:

    name = "Synchronous Byzantine Environment"

    def __init__(self, con):
        self.controller = con

    def get_n(self):
        return self.controller.n

    def get_f(self):
        return self.controller.tf

    def get_round(self):
        return self.controller.round

    def get_id(self, node):
        return self.controller.node_id[node]

    def get_input(self, node):
        return self.controller.input

    def get_input_msgs(self, node):
        return self.controller.get_message_buffer(node)

    def put_broadcast(self, node, msg):
        self.controller.put_broadcast(msg)

    def put_packet(self, node, msg, target):
        self.controller.put_packet(msg, target)

    def put_output(self, node, output):
        self.controller.put_output(node, output)
