from Controller import Controller


class Experiment:

    def __init__(self, setting):
        self.setting = setting
        self.controller = Controller(setting)

    def run(self):
        self.controller.run()

    def report(self):
        self.controller.report()
