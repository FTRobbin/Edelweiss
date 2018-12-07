# TODO: to be merged with AsynPermissionedController

from src.Oracles.PaxosScheduler import *


class PaxosController:
    name = "Asynchronous Paxos Controller"

    def __init__(self, setting):
        self.n = setting.n
        self.env = setting.env_type(self)
        self.node_id = {}
        self.id_node = {}
        self.message_pool = {}
        for i in range(0, self.n):
            self.message_pool[i] = []
        self.message_history = []
        self.output = {}
        if setting.adv_type is None:
            self.adv = None
        else:
            self.adv = setting.adv_type(self.n)
        self.scheduler = PaxosScheduler(self.n, setting.seed, self.adv)
        self.counter = 0
        kargs = {"env": self.env, "con": self}
        for i in range(self.n):
            current_node = setting.protocol(**kargs)
            self.node_id[current_node] = i
            self.id_node[i] = current_node
        self.message_bar = 5000
        self.all_decided = -1

    def is_completed(self):
        self.counter += 1
        # TODO
        return self.counter > self.message_bar

    def run_step(self):
        id, msg = self.scheduler.schedule(self.message_pool)
        self.message_history.append([id, msg])
        if msg in self.message_pool[id]:
            self.message_pool[id].remove(msg)
        self.id_node[id].recv(msg)

    def run(self):
        while not self.is_completed():
            self.run_step()

    def put_broadcast(self, id, msg):
        for i in range(self.n):
            self.message_pool[i].append(msg.clone())
            if self.adv is not None:
                self.adv.obv_message(msg, i)

    def put_packet(self, id, msg, target):
        self.message_pool[target].append(msg)
        if self.adv is not None:
            self.adv.obv_message(msg, target)

    def put_output(self, node, output):
        id = self.node_id[node]
        self.output[id] = output
        if len(self.output) == self.n:
            self.all_decided = self.counter

    def report_message(self):
        for msg in self.message_history:
            print('%d : %s' % (msg[0], msg[1]))
        print('Total # of messages: %d' % len(self.message_history))
        for id in range(0, self.n):
            if id in self.output:
                print('%d : %s' % (id, self.output[id]))
