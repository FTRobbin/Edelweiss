class Controller:

    def __init__(self, setting):
        self.n = setting.n
        self.input = setting.input
        self.env = setting.env_type(self)
        self.pki = setting.pki_type(self.env)
        self.round = -1
        self.node_id = {}
        for i in range(self.n):
            self.node_id[setting.protocol(self.env, self.pki)] = i
        self.message_pool = []
        self.message_buffer = [[] for x in range(self.n)]
        self.output = {}

    def is_completed(self):
        return len(self.output) == self.n

    def run_step(self):
        self.round += 1
        for packet in self.message_pool:
            self.message_buffer[packet[0]].append(packet[1])
        self.message_pool.clear()
        for node in self.node_id.keys():
            node.run_node()

    def run(self):
        while not self.is_completed():
            self.run_step()

    def report(self):
        print (self.output)

    def get_message_buffer(self, node):
        id = self.node_id[node]
        ret = self.message_buffer[id]
        self.message_buffer[id] = []
        return ret

    def put_broadcast(self, msg):
        for i in range(self.n):
            self.message_pool.append([i, msg.clone()])

    def put_output(self, node, output):
        id = self.node_id[node]
        self.output[id] = output
