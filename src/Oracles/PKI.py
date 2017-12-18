from Messages.Message import Message


class IdealPKI:

    name = "IdealPKI"

    def __init__(self, env):
        self.env = env
        self.mem = set()

    def register(self, node):
        pass

    def sign(self, node, msg):
        if self.env.get_id(node) != msg.get_sender() and (type(msg.get_content()) is not Message or self.verify(msg.get_content())):
            raise RuntimeError
        self.mem.add(msg.get_chain())
        return msg

    def verify(self, msg):
        return msg.get_chain() in self.mem
