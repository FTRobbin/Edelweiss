import threading
class SynByzController:

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
    