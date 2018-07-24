from Messages.Message import Message

class BOSCO:

    name = "BOSCO Protocol"
    def __init__(self, env, pki):
        self.env = env
        self.pki = pki
        self.pki.register(self)
        self.input = None

    def run_node(self):
        round = self.env.get_round()
        myid = self.env.get_id(self)
        if round == 0:
            self.input = self.env.get_input(myid)
            self.env.put_broadcast(self, self.pki.sign(self, Message(myid, self.input)))
        else:
            msgs = self.env.get_input_msgs(self)
            if(len(msgs)>self.env.get_n()-self.env.get_f()):
                msgs=msgs[0:self.env.get_n()-self.env.get_f()]
            d = {}
            for msg in msgs:
                key = msg.get_extraction()
                if key not in d:
                    d[key] = 0
                d[key]=d[key]+1
            if not bool(d):
                raise RuntimeError
            d_sorted=sorted(d.items(), key=lambda kv: kv[1],reverse=True)
            if(d_sorted[0][1]>(self.env.get_n()+3*self.env.get_f())/2):
                self.env.put_output(self,d_sorted[0][0])
                self.input = d_sorted[0][0]
                self.env.put_broadcast(self, self.pki.sign(self, Message(myid, self.input)))
            elif (d_sorted[0][1]>(self.env.get_n()+self.env.get_f())/2):
                if len(d_sorted)>1:
                    if d_sorted[1][1]>(self.env.get_n()+self.env.get_f())/2:
                        self.env.put_broadcast(self, self.pki.sign(self, Message(myid, self.input)))
                    else:
                        self.input = d_sorted[0][0]
                        self.env.put_broadcast(self, self.pki.sign(self, Message(myid, self.input)))
                else:
                    self.input=d_sorted[0][0]
                    self.env.put_broadcast(self, self.pki.sign(self, Message(myid, self.input)))
