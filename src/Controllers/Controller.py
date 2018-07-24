import threading
class SynByzController:

<<<<<<< HEAD
	name = "Synchronous Byzantine Controller"

	def __init__(self, setting):
		self.n = setting.n
		self.input = setting.input
		self.f = setting.f
		self.corf = setting.corrupt_sender
		self.tf = self.f
		if self.corf:
			self.f -= 1
		self.env = setting.env_type(self)
		self.pki = setting.pki_type(self.env)
		self.round = -1
		self.node_id = {}
		for i in range(self.n):
			if self.corf and i == setting.protocol.SENDER or i + self.f >= self.n:
				self.node_id[setting.adversary(self.env, self.pki)] = i
			else:
				self.node_id[setting.protocol(self.env, self.pki)] = i
		self.message_pool = []
		self.message_buffer = [[] for x in range(self.n)]
		self.message_history = []
		self.output = {}
		self.sender_id = setting.protocol.SENDER

	def is_corrupt(self, id):
		# TODO
		return self.corf and id == 0 or id + self.f >= self.n

	def is_completed(self):
		return len(self.output) == self.n - self.tf

	def run_step(self):
		self.round += 1
		for packet in self.message_pool:
			self.message_buffer[packet[0]].append(packet[1])
		self.message_history.append(self.message_pool)
		self.message_pool = []
		for node in self.node_id.keys():
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
			for packet in self.message_history[r]:
				print("From %d to %d content %s " %
					  (packet[1].get_sender(), packet[0], packet[1].get_chain()))

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

class SynByzControllerWithoutSender:
    
	name = "Synchronous Byzantine Controller without sender"

	def __init__(self, setting):
		self.n = setting.n
		self.input = setting.input.copy()
		self.f = setting.f
		self.env = setting.env_type(self)
		self.pki = setting.pki_type(self.env)
		self.round = -1
		self.node_id = {}
		for i in range(self.n):
			if self.is_corrupt(i):
				self.node_id[setting.adversary(self.env, self.pki)] = i
			else:
				self.node_id[setting.protocol(self.env, self.pki)] = i
		self.message_pool = []
		self.message_buffer = [[] for x in range(self.n)]
		self.message_history = []
		self.output = {}

	def is_corrupt(self, id):
		return id < self.f

	def is_completed(self):
		return len(self.output) == self.n - self.f

	def run_step(self):
		self.round += 1
		for packet in self.message_pool:
			self.message_buffer[packet[0]].append(packet[1])
		self.message_history.append(self.message_pool)
		self.message_pool = []
		for node in self.node_id.keys():
			node.run_node()

	def dispatch_message(self):
		if not bool(self.message_pool):
			return
		for packet in self.message_pool:
			self.message_buffer[packet[0]].append(packet[1])
		self.message_history.append(self.message_pool)
		self.message_pool = []

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
			for packet in self.message_history[r]:
				print("From %d to %d content %s " %
					  (packet[1].get_sender(), packet[0], packet[1].get_chain()))

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


class AsynByzController:

	name = "Asynchronous Byzantine Controller"

	def __init__(self, setting):
		self.n = setting.n
		self.input = setting.input
		self.f = setting.f
		self.corf = setting.corrupt_sender
		self.tf = self.f
		if self.corf:
			self.f -= 1
		self.env = setting.env_type(self)
		self.pki = setting.pki_type(self.env)
		self.round = -1
		self.node_id = {}
		for i in range(self.n):
			if self.corf and i == setting.protocol.SENDER or i + self.f >= self.n:
				self.node_id[setting.adversary(self.env, self.pki)] = i
			else:
				self.node_id[setting.protocol(self.env, self.pki)] = i
		self.message_pool = []
		self.message_buffer = [[] for x in range(self.n)]
		self.message_history = []
		self.output = {}
		self.sender_id = setting.protocol.SENDER

	def is_corrupt(self, id):
		return id <= self.f

	def is_completed(self):
		pass


	def run_step(self):
		self.round += 1
		for packet in self.message_pool:
			self.message_buffer[packet[0]].append(packet[1])
		self.message_history.append(self.message_pool)
		self.message_pool = []
		for node in self.node_id.keys():
			node.run_node()


	def run(self):
		threads = []
		for node in self.node_id.keys():
			t = threading.Thread(target=node.run_node)
			threads.append(t)
			t.start()
		

	def report_message(self):
		print("")
		print("Message History :")
		for r in range(1, self.round + 1):
			print("Round %d : " % r)
			for packet in self.message_history[r]:
				print("From %d to %d content %s " %
					  (packet[1].get_sender(), packet[0], packet[1].get_chain()))

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
=======
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
>>>>>>> 7a1ca05d6a6fdee0570ebb4de48d0a256ef8ed7d
