

class ByzValidity:

    @staticmethod
    def measure(con):
        input_local = []
        if type(con.input) is not list:
            input_local = [con.input]
        else:
            input_local = con.input
        if con.has_sender and con.is_corrupt(con.sender_id):
            valid = True
        else:
            valid = True
            for x, y in con.output.items():
                if not con.is_corrupt(x) and y not in input_local:
                    valid = False
        # print("Validity : " + str(valid))
        # if not valid:
        #     print("\033[1;31mOops! Validity is violated \033[0m")
        return ("Validity",bool(valid))


class ByzConsistency:

    @staticmethod
    def measure(con):
        output = -1
        consistent = True
        for x, y in con.output.items():
            if not con.is_corrupt(x):
                if output == -1:
                    output = y
                elif output != y:
                    consistent = False
        # print("Consistency : " + str(consistent))
        # if not consistent:
            # print("\033[1;31mOops! Consistency is violated \033[0m")
        return ("Consistency",bool(consistent))


class ByzUnanimity:
    
    @staticmethod
    def measure(con):
        if type(con.input) is not list:
            con.input = [con.input]
        if len(set(con.input)) == 0:
            raise RuntimeError
        if len(set(con.input)) == 1:
            output = -1
            unanimity = True
            for x, y in con.output.items():
                if not con.is_corrupt(x):
                    if output == -1:
                        output = y
                    elif output != con.input[0]:
                        unanimity = False
            # print("Unanimity : " + str(unanimity))
            # if not unanimity:
            #     print("\033[1;31mOops! Unanimity is violated \033[0m!")
            return ("Unanimity", bool(unanimity))
        else:
            # print("Unanimity : " + str(True))
            return ("Unanimity", bool(True))
