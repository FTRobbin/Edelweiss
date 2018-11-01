
import unittest

# This is the class we want to test. So, we need to import it
from Tangle import Tangle
from Util import *


class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    TestTangle = Tangle(Tangle_Site.get_genesis_site(),
                        2)  # instantiate the TestTangle Class

    def test_weight_calculation(self):
        site2 = Tangle_Site([1], [], 1)
        site3 = Tangle_Site([1], [], 1)
        site4 = Tangle_Site([2, 3], [], 1)
        site5 = Tangle_Site([2, 3], [], 1)
        site6 = Tangle_Site([4, 5], [], 1)
        site7 = Tangle_Site([1, 6], [], 1)

        Test.TestTangle.insert_site(site2)
        self.TestTangle.insert_site(site3)
        self.TestTangle.insert_site(site4)
        self.TestTangle.insert_site(site5)
        self.TestTangle.insert_site(site6)
        self.TestTangle.insert_site(site7)

        # self.assertEquals(
            # 7, self.TestTangle.genesis_site.calculate_cumulative_weight())
        selected_tips=self.TestTangle.random_walk()
        tip_id_list=[]
        for tip in selected_tips:
            tip_id_list.append(tip.id)
        self.assertEquals([6,7],tip_id_list)

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
