class Experiment:

    id = 0

    def __init__(self, setting):
        self.id = Experiment.id
        Experiment.id += 1
        self.setting = setting
        self.controller = setting.con_type(setting)

    def run(self):
        self.controller.run()

    def report(self):
        print("Experiment #%d" % self.id)
        self.setting.report()
        self.controller.report()

    def run_and_report(self):
        self.run()
        self.report()
