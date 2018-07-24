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
        print("Experiment Setting:")
        self.setting.report()
        print("")
        print("Experiment Result:")
        self.controller.report()
        print("")
        if len(self.setting.measure) > 0:
            print("Measurements:")
            for m in self.setting.measure:
                m.measure(self.controller)

    def run_and_report(self):
        self.run()
        self.report()
