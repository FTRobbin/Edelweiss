
class SynByzController:
    name = "Synchronous Byzantine Controller without sender"

    def __init__(self, setting):
        self.n = setting.n
        if type(input) is list:
            self.input = setting.input.copy()
        else:
            self.input = setting.input
        self.f = setting.f
        self.tf = setting.tf
        self.env = setting.env_type(self)
        self.pki = setting.pki_type(self.env)
        self.centralized = setting.centralized
        self.round = -1
        self.node_id = {}
        self.has_sender = setting.has_sender
        self.message_pool = []
        self.message_buffer = [[] for x in range(self.n)]
        self.message_history = []
        self.output = {}
        self.corf = setting.corrupt_sender
        if(self.has_sender):
            self.sender_id = setting.protocol.SENDER
        if (self.has_sender):
            self.tf = self.f
            if self.corf:
                self.f -= 1
        for i in range(self.n):
            if self.is_corrupt(i):
                self.node_id[setting.adversary(self.env, self.pki)] = i
            else:
                self.node_id[setting.protocol(self.env, self.pki)] = i
        if(setting.centralized):
            self.centralized_adversary = setting.centralized_adversary(
                self.env, self.pki, self)

    def is_corrupt(self, id):
        if self.has_sender:
            return self.corf and id == 0 or id + self.f >= self.n
        else:
            return id < self.tf

    def is_completed(self):
        return len({k: v for k, v in self.output.items() if not self.is_corrupt(k)}) == self.n - self.tf

    def run_step(self):
        self.round += 1
        for packet in self.message_pool:
            self.message_buffer[packet[0]].append(packet[1])
        self.message_history.append(self.message_pool)
        self.message_pool = []
        for node in self.node_id.keys():
            if self.centralized and self.is_corrupt(self.node_id[node]):
                self.centralized_adversary.run_node()
            else:
                node.run_node()

    def run(self):
        while not self.is_completed():
            self.run_step()

    def report(self):
        for x, y in self.output.items():
            print("Node %d : %s" % (x, str(y)))

    def report_message(self):
        print("")
        print("Message History :")
        for r in range(1, self.round + 1):
            print("Round %d : " % r)
            d = {}
            for packet in self.message_history[r]:
                print("From %d to %d content %s " %
                      (packet[1].get_sender(), packet[0], packet[1].get_extraction()))
                key = (packet[0], packet[1].get_extraction())
                if key not in d:
                    d[key] = 0
                d[key] = d[key] + 1
            print(" ")
            print("Summary :")
            for k in sorted(d):
                print("Receiver %d receive %d for %d times " %
                      (k[0], k[1], d[k]))

        print(" ")
        print("Node Output :")
        for x, y in self.output.items():
            print("Node %d : %s" % (x, str(y)))

    def get_message_buffer(self, node):
        id = self.node_id[node]
        ret = self.message_buffer[id]
        self.message_buffer[id] = []
        return ret

    def put_broadcast(self, msg):
        for i in range(self.n):
            self.message_pool.append([i, msg.clone()])

    def put_packet(self, msg, target):
        self.message_pool.append([target, msg])

    def put_output(self, node, output):
        id = self.node_id[node]
        self.output[id] = output
