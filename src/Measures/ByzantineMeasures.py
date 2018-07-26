class ByzValidityWithoutSender:

    @staticmethod
    def measure(con):
        valid = True
        for x, y in con.output.items():
            if not con.is_corrupt(x) and y not in con.input:
                valid = False
        print("Validity : " + str(valid))
        if not valid:
            print("\033[1;31mOops! Validity is violated \033[0m")
        return bool(valid)


class ByzValidity:

    @staticmethod
    def measure(con):
        if con.is_corrupt(con.sender_id):
            valid = True
        else:
            valid = True
            for x, y in con.output.items():
                if not con.is_corrupt(x) and y != con.input:
                    valid = False
        print("Validity : " + str(valid))
        if not valid:
            print("\033[1;31mOops! Validity is violated \033[0m")
        return bool(valid)


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
        print("Consistency : " + str(consistent))
        if not consistent:
            print("\033[1;31mOops! Consistency is violated \033[0m")
        return bool(consistent)


class ByzUnanimity:
    
    @staticmethod
    def measure(con):
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
            print("Unanimity : " + str(unanimity))
            if not unanimity:
                print("\033[1;31mOops! Unanimity is violated \033[0m!")
            return bool(unanimity)
        else:
            print("Unanimity : " + str(True))
            return True
