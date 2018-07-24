class ByzValidityWithoutSender:

    @staticmethod
    def measure(con):
        valid = True
        for x, y in con.output.items():
            if not con.is_corrupt(x) and not y in con.input:
                valid = False
        print("Validity : " + str(valid))

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

class ByzUnanimity:
    
    @staticmethod
    def measure(con):
        if len(set(con.input))==0:
            raise RuntimeError
        if len(set(con.input)) == 1:
            output = -1
            Unanimity = True
            for x, y in con.output.items():
                if not con.is_corrupt(x):
                    if output == -1:
                        output = y
                    elif output != con.input[0]:
                        consistent = False
            print("Unanimity : " + str(Unanimity))
        else:
            print("Unanimity : " + str(True))
            



