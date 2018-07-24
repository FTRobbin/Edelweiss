class Message:

	def __init__(self, sender, content,receiver=None, round=None, iden=None):
		self.sender = sender
		self.content = content
		self.round = round
		self.receiver = receiver
		self.iden = iden
	def clone(self):
		if type(self.content) is Message:
			return Message(self.sender, self.content.clone(),self.receiver,self.round,self.iden)
		else:
			return Message(self.sender, self.content,self.receiver,self.round,self.iden)

	def get_chain(self):
		if type(self.content) is Message:
			return str(self.content.get_chain()) + "|" + str(self.sender) + "|" + str(self.round) + "|" + str(self.receiver)
		else:
			return str(self.content) + "|" + str(self.sender)  + "|" + str(self.round) + "|" + str(self.receiver)

	def get_extraction(self):
		if type(self.content) is Message:
			return self.content.get_extraction()
		else:
			return self.content

	def get_content(self):
		return self.content

	def get_sender(self):
		return self.sender
	
	def get_round(self):
		return self.round
	
	def get_receiver(self):
		return self.receiver
	def get_iden(self):
		return self.iden
