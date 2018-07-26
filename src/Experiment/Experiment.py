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
        self.controller.report_message()
        print("")
        flag = 0
        if len(self.setting.measure) > 0:
            print("Measurements:")
            for m in self.setting.measure:
                flag = not m.measure(self.controller) or flag
            if flag == 0:
                print("\033[1;32mCongrats! All properties are satisified! \033[0m")
            else:
                print("\033[1;31mOops! Some properties are violated! \033[0m")

    def run_and_report(self):
        self.run()
        self.report()
