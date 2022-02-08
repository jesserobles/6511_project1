import unittest

import bestfirstsearch
from heuristics import h_admissible, largest_pitcher_first_heuristic, simple_heuristic
from states import get_child_states



class StateGenerator(unittest.TestCase):
    def test_state_generator(self):
        capacities = (2, 5, None)
        state = (0, 0, 0)
        known_states = [(2, 0, 0), (0, 5, 0)]
        self.assertEqual(set(known_states),set(get_child_states(state, capacities)))

        state = (0, 5, 0)
        known_states = [(2, 5, 0), (2, 3, 0), (0, 0, 5), (0, 0, 0)]
        self.assertEqual(set(known_states),set(get_child_states(state, capacities)))

        state = (2, 0, 0)
        known_states = [(0,0,0), (0,2,0), (0,0,2), (2,5,0)]
        self.assertEqual(set(known_states),set(get_child_states(state, capacities)))

        state = (2, 5, 0)
        known_states = [(0,5,0), (2,0,0), (0,5,2), (2,0,5)]
        self.assertEqual(set(known_states),set(get_child_states(state, capacities)))

        state = (2, 3, 5)
        known_states = [(0,3,5), (2,0,5), (2, 3, 0), (0,5,5), (0,3,7), (2, 0, 8), (2,5,3), (2,5,5)]
        self.assertEqual(set(known_states),set(get_child_states(state, capacities)))


class FileTest(unittest.TestCase):

    def test_0(self):
        s = bestfirstsearch.Search.from_file('input.txt')
        # First use non-admissible heuristic to check if a
        # solution exists
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            s = bestfirstsearch.Search.from_file('input.txt', heuristic=h_admissible)
            s.print_problem()
            result = s.search()
            self.assertEqual(result, 19, "Should be 19")
            self.assertTrue(s.h_is_admissible(), "Heuristic not admissible")
        else:
            self.assertEqual(result,-1, "Should be no solution")

    def test_1(self):
        s = bestfirstsearch.Search.from_file('input1.txt')
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            s = bestfirstsearch.Search.from_file('input1.txt', heuristic=h_admissible)
            s.print_problem()
            result = s.search()
            self.assertEqual(result, 7, "Should be 7")
            self.assertTrue(s.h_is_admissible(), "Heuristic not admissible")
        else:
            self.assertEqual(result,-1, "Should be no solution")

    def test_2(self):
        s = bestfirstsearch.Search.from_file('input2.txt')
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            s = bestfirstsearch.Search.from_file('input2.txt', heuristic=h_admissible)
            s.print_problem()
            result = s.search()
            self.assertEqual(result, -1, "Should be no solution")
        else:
            print("No solution exists")
            self.assertEqual(result,-1, "Should be no solution")

    def test_3(self):
        s = bestfirstsearch.Search.from_file('input3.txt')
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            raise AttributeError("This problem shouldn't have a solution")
        else:
            print("No solution exists")
            self.assertEqual(result, -1, "Should be no solution")

    def test_4(self):
        s = bestfirstsearch.Search.from_file('input4.txt')
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            s = bestfirstsearch.Search.from_file('input4.txt', heuristic=largest_pitcher_first_heuristic)
            s.print_problem()
            result = s.search()
            self.assertEqual(result, 36, "Should be 36")
            self.assertTrue(s.h_is_admissible(), "Heuristic not admissible")
        else:
            self.assertEqual(result, -1, "Should be no solution")
    
    def test_5(self):
        s = bestfirstsearch.Search.from_file('input5.txt')
        result = s.search(heuristic=simple_heuristic, timeout=5)
        if not s.timedout:
            s = bestfirstsearch.Search.from_file('input5.txt', heuristic=h_admissible)
            s.print_problem()
            result = s.search()
            self.assertEqual(result, 5, "Should be 5")
            self.assertTrue(s.h_is_admissible(), "Heuristic not admissible")
        else:
            self.assertEqual(result, -1, "Should be no solution")
    

if __name__ == '__main__':
    unittest.main()