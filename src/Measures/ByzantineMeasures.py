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
