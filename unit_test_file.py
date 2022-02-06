import unittest
import bestfirstsearch
from heuristics import largest_bucket_first_heuristic


class FileTest(unittest.TestCase):

    def test(self):
        s = bestfirstsearch.Search.from_file('default.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, 5, "Should be 5")
        print("UNIT TEST: Test 1 Complete")

    def test_1(self):
        s = bestfirstsearch.Search.from_file('input.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, 19, "Should be 19")
        print("UNIT TEST: Test 2 Complete")

    def test_2(self):
        s = bestfirstsearch.Search.from_file('input1.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, 7, "Should be 7")
        print("UNIT TEST: Test 3 Complete")

    def test_3(self):
        s = bestfirstsearch.Search.from_file('input2.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")
        print("UNIT TEST: Test 4 Complete")

    def test_4(self):
        s = bestfirstsearch.Search.from_file('input3.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")
        print("UNIT TEST: Test 5 Complete")

    def test_5(self):
        s = bestfirstsearch.Search.from_file('input4.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, 36, "Should be 36")
        print("UNIT TEST: Test 6 Complete")

if __name__ == '__main__':

    unittest.main()