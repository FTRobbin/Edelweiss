class Message:

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def clone(self):
        if type(self.content) is Message:
            return Message(self.sender, self.content.clone())
        else:
            return Message(self.sender, self.content)

    def get_chain(self):
        if type(self.content) is Message:
            return str(self.content.get_chain()) + "|" + str(self.sender)
        else:
            return str(self.content) + "|" + str(self.sender)

    def get_extraction(self):
        if type(self.content) is Message:
            return self.content.get_extraction()
        else:
            return self.content

    def get_content(self):
        return self.content

    def get_sender(self):
        return self.sender
