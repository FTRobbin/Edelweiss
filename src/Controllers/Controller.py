class SynByzController:

    name = "Synchronous Byzantine Controller"

    def __init__(self, setting):
        self.n = setting.n
        self.input = setting.input
        self.env = setting.env_class(self)
        self.pki = setting.pki_class(self.env)

        self.round = -1
        self.node_id = {}
        self.node_obj = []

        # TODO PKI not working

        self.f = 0 # num of corrupted
        if setting.adv_class is None:
            self.no_adv = True
            for i in range(self.n):
                sk = self.pki.register(i)
                self.node_id[sk] = i
                self.node_obj.append(setting.protocol(self.env, self.pki, sk))
        else:
            self.no_adv = False
            self.corrupted = []
            if setting.adv_class.is_central:
                self.adv = setting.adv_class(self, **setting.adv_para)
                for i in range(self.n):
                    sk = self.pki.register(i)
                    self.node_id[sk] = i
                    if self.adv.decide_corrupt(i):
                        self.adv.create_node(i, sk)
                        self.node_obj.append("Adv %d" % i)
                        self.corrupted.append(True)
                        self.f += 1
                    else:
                        self.node_obj.append(setting.protocol(self.env, self.pki, sk))
                        self.corrupted.append(False)
            else:
                # TODO: Distributed adv
                raise NotImplementedError

        self.output = {}
        self.sender_id = setting.protocol.SENDER

        self.message_pool = []
        self.message_buffer = [[] for _ in range(self.n)]
        self.message_history = []

        self.measure = setting.measure[:]

    def is_corrupt(self, id):
        if self.no_adv:
            return False
        else:
            return self.corrupted[id]

    def is_completed(self):
        return len(self.output) == self.n - self.f

    def run_step(self):
        self.round += 1
        for packet in self.message_pool:
            self.message_buffer[packet[0]].append(packet[1])
        self.message_history.append(self.message_pool)
        self.message_pool = []
        if self.no_adv:
            for node in self.node_obj:
                node.run_node()
        else:
            for i in range(self.n):
                if self.corrupted[i]:
                    self.adv.run_node(i)
                else:
                    self.node_obj[i].run_node()

    def run(self):
        while not self.is_completed():
            self.run_step()

    def report(self):
        print("Experiment Result:")
        # report output
        for x, y in self.output.items():
            print("Node %d : %s" % (x, str(y)))
        print("")
        # report message
        print("Message History :")
        for r in range(1, self.round + 1):
            print("Round %d : " % r)
            for packet in self.message_history[r]:
                print("From %d to %d content %s " % (packet[1].get_sender(), packet[0], packet[1].get_chain()))
        print("")
        # report measure
        # TODO: dynamic measure
        for m in self.measure:
            m.measure(self)
        print("")

    def get_message_buffer(self, sk):
        id = self.node_id[sk]
        ret = self.message_buffer[id]
        self.message_buffer[id] = []
        return ret

    def put_broadcast(self, msg):
        for i in range(self.n):
            self.message_pool.append([i, msg.clone()])

    def put_packet(self, msg, target):
        self.message_pool.append([target, msg])

    def put_output(self, sk, output):
        id = self.node_id[sk]
        self.output[id] = output
