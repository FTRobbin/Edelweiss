import hashlib

from Util.Util import *


class ExpResult():

    def __init__(self, setting, controller):
        self.experiment_type = setting.experiment_type
        self.controller = controller.name
        self.Environment = setting.env_type.name
        self.PKI = setting.pki_type.name
        self.Protocol = setting.protocol.name
        if setting.f > 0:
            if setting.get_centralized():
                self.adversary = setting.centralized_adversary.name
            else:
                self.adversary = setting.adversary.name
        self.f = setting.f
        self.tf = setting.tf
        self.n = setting.n
        self.seed = setting.seed
        self.input = setting.input
        self.centralized = setting.centralized
        self.has_sender = setting.has_sender
        self._lambda = setting._lambda
        self.seed = setting.seed
        self.mine_results = None
        self.round = None
        if controller.round:
            round_history = {}
            round_count = {}
            for r in range(0, controller.round):
                round_history[str(r)] = []
                round_count[str(r)] = []
                d = {}
                for packet in sorted(controller.message_history[r], key=lambda x: x[1].get_sender()):
                    round_history[str(r)].append(
                        (packet[1].get_sender(), packet[0], str(packet[1])))
                    key = (packet[0], str(packet[1]))
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
            self.output[str(k)] = (v)
        self.measures = {}
        for m in setting.measure:
            self.measures[m.measure(controller)[0]] = m.measure(
                controller)[1]

    def object_key(self):
        arg = self.experiment_type + self.PKI + self.Protocol + self.Environment + \
            str(self.input) + str(self.n) + str(self.f)+str(self.tf) + \
            str(self.centralized) + str(self.has_sender)
        if self.f > 0:
            arg = arg+self.adversary
        if self._lambda != -1:
            arg = arg+str(self._lambda)
            arg = arg+str(self.seed)
        arg.encode('utf-8')
        return hashlib.sha256((arg.encode('utf-8'))).hexdigest()

    def print(self):
        print("Experiment Setting: "+self.experiment_type)
        print("Controller : " + self.controller)
        print("Environment : " + self.Environment)
        print("PKI : " + self.PKI)
        print("Protocol : " + self.Protocol)
        if self.tf > 0:
            print("Adversary : " + self.adversary)
        print("")
        print("Parameters:")
        print("n : %d" % self.n)
        if (type(self.input) is list):
            for i in range(self.n):
                print("input : %d" % self.input[i])
        else:
            print("input : %d" % self.input)
        if self.tf > 0:
            print("num of corruptions : %d" % self.tf)
        print("")
        print("Seed is:"+str(self.seed))
        print("Experiment Result:")
        print("")
        print("Message History :")
        if self.round:
            for k, v in sorted(self.round_history.items(), key=lambda kv: int(kv[0])):
                if k == '0':
                    continue
                print("Round "+str(int(k)))
                for bucket in self.round_history[k]:
                    print("from "+str(bucket[0])+" to " +
                          str(bucket[1])+" content "+str(bucket[2]))

                print("Summary")
                for (receiver, content, times) in self.round_count[k]:
                    print("Receiver "+str(receiver)+" Receive " +
                          str(content)+" for "+str(times)+" time(s)")
                print(" ")
        if self.mine_results:
            print("Mine Results")
            for k, v in sorted(self.mine_results.items()):
                print(k, end=' ')
                print(self.mine_results[k])
            print(" ")

        print("Node Output :")
        for x, y in sorted(self.output.items()):
            print("Node %s : %s" % (x, str(y)))
        print(" ")
        flag = 0
        print("Measurements:")
        for k, v in self.measures.items():
            if(v != False):
                flag += 1
            print(k, end=': ')
            print(v)
        if(flag == len(self.measures)):
            print("\033[1;32mCongrats! All properties are satisified! \033[0m")
        else:
            print("\033[1;31mOops! Some properties are violated! \033[0m")
