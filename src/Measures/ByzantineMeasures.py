

class ByzValidity:

    @staticmethod
    def measure(con):
        if (not con.has_sender) or (con.has_sender and not con.corf):
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
            return ("Validity",bool(valid))
        return ("Validity",True)
            



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
        return ("Consistency",bool(consistent))


class ByzUnanimity:
    
    @staticmethod
    def measure(con):
        if (not con.has_sender) or (con.has_sender and not con.corf):
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
                return ("Unanimity", bool(unanimity))
            else:
                return ("Unanimity", bool(True))
        return ("Unanimity", bool(True))
