import unittest
import main
from heuristics import largest_bucket_first_heuristic


class TestProject(unittest.TestCase):

    def test_1(self):
        s = main.Search.from_file('input.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, 19, "Should be 19")

    def test_2(self):
        s = main.Search.from_file('input1.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")

    def test_3(self):
        s = main.Search.from_file('input2.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")

    def test_4(self):
        s = main.Search.from_file('input3.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")

    def test_5(self):
        s = main.Search.from_file('input4.txt')
        result = s.search(heuristic=largest_bucket_first_heuristic)
        self.assertEqual(result, -1, "Should be no solution")

if __name__ == '__main__':
    unittest.main()