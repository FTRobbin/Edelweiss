from Util.Util import  *

class Message:

    def __init__(self, sender, content, round=None, receiver=None, iden=None):
        self.sender = sender
        self.content = content
        self.round = round
        self.receiver = receiver
        self.iden = iden

    def clone(self):
        if type(self.content) is Message:
            return Message(self.sender, self.content.clone(),self.round, self.receiver, self.iden)
        else:
            return Message(self.sender, self.content, self.round, self.receiver, self.iden)

    def __str__(self):
        if type(self.content) is Message:
            return str(self.content) + "|" + str(self.sender)
        else:
            return ContentToString(self.content) + "|" + str(self.sender)

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
