import hashlib


class ExpResult():

    def __init__(self, setting, controller):
        self.experiment_type = setting.experiment_type
        self.controller = controller.name
        self.Environment = setting.env_type.name
        self.PKI = setting.pki_type.name
        self.Protocol = setting.protocol.name
        self.adversary = setting.adversary.name
        if setting.f > 0:
            self.adversary = setting.adversary.name
        self.f = setting.f
        self.tf = setting.tf
        self.n = setting.n
        self.input = setting.input
        self.centralized = setting.centralized
        self.has_sender = setting.has_sender
        round_history = {}
        round_count = {}
        for r in range(1, controller.round + 1):
            # print("Round %d : " % r)
            round_history[str(r)] = []
            round_count[str(r)] = []
            d = {}
            for packet in sorted(controller.message_history[r], key=lambda x: x[1].get_sender()):
                round_history[str(r)].append(
                    (packet[1].get_sender(), packet[0], packet[1].get_extraction()))
                key = (packet[0], packet[1].get_extraction())
                if key not in d:
                    d[key] = 0
                d[key] = d[key] + 1
            round_history[str(r)] = sorted(round_history[str(r)])
            for k in sorted(d):
                round_count[str(r)].append((k[0], k[1], d[k]))
        self.round_history = round_history
        self.round_count = round_count
        self.round = controller.round
        self.output = {}
        for k, v in controller.output.items():
            self.output[str(k)] = v
        self.measures = {}
        for m in setting.measure:
            self.measures[m.measure(controller)[0]] = m.measure(
                controller)[1]

    def object_key(self):
        # m = hashlib.sha256(.encode('utf-8'))
        arg = self.experiment_type + self.PKI + self.Protocol + self.Environment + \
            str(self.input) + str(self.n) + str(self.f)+str(self.tf) + \
            str(self.centralized) + str(self.has_sender)
        if self.f > 0:
            arg = arg+self.adversary
        arg.encode('utf-8')
        # hashlib.sha256((arg.encode('utf-8'))).hexdigest()
        # m.update(arg)
        return hashlib.sha256((arg.encode('utf-8'))).hexdigest()
    def print(self):
        print()
