from Experiment.Experiment import *

def ContentToString(input):
    if type(input) is tuple:
        return '('+str(input[0])+','+(''.join(str(e) + ' ' for e in input[1]))[0:-1]+')'
    if type(input) is list:
        return (''.join(str(e) + ' ' for e in input))[0:-1]
    else:
        return str(input)


class Block:
    def __init__(self, round, id, belief):
        self.round = round
        self.id = id
        self.belief = belief

    def verify(self):
        return True

    def __str__(self):
        return str(self.round) + '-' + str(self.id) + '-' + str(self.belief)

    def get_sender(self):
        return self.id


def run_and_print(setting):
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    res[1].print()


def run_and_get_result(setting):
    exp = Experiment(setting)
    exp.run()
    return exp.get_result()
