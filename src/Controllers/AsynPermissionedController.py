from Util.Util import *
from Oracles.Mine import Mine
from Oracles.NakamotoScheduler import NakamotoScheduler


class AsynPermissionedController:
    name = "Asynchronous Permissioned Controller"

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
        self.node_id = {}
        self.id_node = {}
        self.has_sender = setting.has_sender
        self.message_pool = {}
        for i in range(0, self.n):
            self.message_pool[i] = []
        # self.message_buffer = [[] for x in range(self.n)]
        self.message_history = []
        self.output = {}
        self.centralized = setting.centralized
        self.corf = setting.corrupt_sender
        self.mine = None
        self.round = None
        self.scheduler = NakamotoScheduler(self.n, setting.seed)
        self.counter = 0
        if (self.has_sender):
            self.sender_id = setting.protocol.SENDER
        if (self.has_sender):
            self.tf = self.f
            if self.corf:
                self.f -= 1
        kargs = {"env": self.env, "pki": self.pki, "con": self}
        for i in range(self.n):
            if self.is_corrupt(i) and not self.centralized:
                current_adversaey = setting.adversary(**kargs)
                self.node_id[current_adversaey] = i
                self.id_node[i] = current_adversaey
            else:
                current_adversaey = setting.protocol(**kargs)
                self.node_id[current_adversaey] = i
                self.id_node[i] = current_adversaey
        if (setting.centralized):
            self.centralized_adversary = setting.centralized_adversary(
                **kargs)

    def is_corrupt(self, id):
        if self.has_sender:
            return self.corf and id == 0 or id + self.f >= self.n
        else:
            return id + self.tf >= self.n

    def is_completed(self):
        self.counter += 1
        return self.counter > 1000

    def run_step(self):
        [node, event] = self.scheduler.schedule()
        if event == 'Deliver':
            self.id_node[node].receive_block()
        elif event == 'Mine':
            self.id_node[node].mine_block()
        else:
            raise RuntimeError

    def drain(self):
        while not isListEmpty(list(self.message_pool.values())):
            alive_list=list(filter(lambda x:self.message_pool[x],self.message_pool.keys()))
            self.scheduler.set_alive_list(alive_list)
            node = None
            event = None
            [node, event] = self.scheduler.schedule()
            self.id_node[node].receive_block()

    def run(self):
        while not self.is_completed():
            self.run_step()
        self.drain()
        # raise NotImplementedError
        for node in self.node_id.keys():
            node.put_output()
    # get only one message
    def get_message(self, node):
        id = self.node_id[node]
        if not self.message_pool[id]:
            return None
        ret = self.message_pool[id][0]
        self.message_pool[id].remove(self.message_pool[id][0])
        return ret

    def put_broadcast(self, id, msg):
        for i in range(self.n):
            if i == id:
                continue
            self.message_pool[i].append(msg.clone())

    def put_packet(self, msg, target):
        self.message_pool[target].append(msg)

    def put_output(self, node, output):
        id = self.node_id[node]
        self.output[id] = output
