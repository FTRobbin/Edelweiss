
import unittest

# This is the class we want to test. So, we need to import it
from Tangle import *


class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    TestTangle = Tangle(Tangle_Site.get_genesis_site(),
                        2)  # instantiate the TestTangle Class

    def test_weight_calculation(self):
        site2 = Tangle_Site([1], [], 1, 1)
        site3 = Tangle_Site([1], [], 1, 1)
        site4 = Tangle_Site([2], [], 1, 1)
        site5 = Tangle_Site([2], [], 1, 1)
        site6 = Tangle_Site([2], [], 1, 1)
        site7 = Tangle_Site([4,5], [], 1, 1)

        Test.TestTangle.insert_site(site2)
        self.TestTangle.insert_site(site3)
        self.TestTangle.insert_site(site4)
        self.TestTangle.insert_site(site5)
        self.TestTangle.insert_site(site6)
        self.TestTangle.insert_site(site7)
        # self.assertEqual(site2.calculate_cumulative_weight(),5)
        # self.assertEqual(site3.calculate_cumulative_weight(),5)
        # self.assertEqual(site4.calculate_cumulative_weight(),3)
        # self.assertEqual(site5.calculate_cumulative_weight(),3)
        # self.assertEqual(site6.calculate_cumulative_weight(),2)
        # self.assertEqual(site7.calculate_cumulative_weight(),1)
        # self.assertEqual(self.TestTangle.genesis_site.calculate_cumulative_weight(),7)
        print(' ')
        print(self.TestTangle.random_walk()[0].id)
        print(self.TestTangle.random_walk()[1].id)



    
    def print_test(self):
        print("lalala")
        



class SimpleTest:
    """
    The basic class that inherits unittest.TestCase
    """
    TestTangle = Tangle(Tangle_Site.get_genesis_site(),2)
    @staticmethod
    def print_test():
        site2 = Tangle_Site([1], [], 1, 1)
        site3 = Tangle_Site([1], [], 1, 1)
        site4 = Tangle_Site([2,3], [], 1, 1)
        site5 = Tangle_Site([2,3], [], 1, 1)
        site6 = Tangle_Site([4,5], [], 1, 1)
        site7 = Tangle_Site([6], [], 1, 1)

        SimpleTest.TestTangle.insert_site(site2)
        SimpleTest.TestTangle.insert_site(site3)
        SimpleTest.TestTangle.insert_site(site4)
        SimpleTest.TestTangle.insert_site(site5)
        SimpleTest.TestTangle.insert_site(site6)
        SimpleTest.TestTangle.insert_site(site7)
        assert(site2.calculate_cumulative_weight()==4)
        # assert(site2.calculate_cumulative_weight()==4)
        # assert(site2.calculate_cumulative_weight()==4)
        # assert(site2.calculate_cumulative_weight()==4)
        # assert(site2.calculate_cumulative_weight()==4)




if __name__ == '__main__':
    # begin the unittest.main()
    # assert(SimpleTest.TestTangle1.check_identical(SimpleTest.TestTangle2))
    SimpleTest.print_test()
    # print(SimpleTest.TestTangle1.check_identical(SimpleTest.TestTangle2))
    # pass