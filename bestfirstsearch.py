from ast import arg
from datetime import timedelta
import itertools
from operator import itemgetter
import heapq
import sys
from time import time
from typing import List, Tuple, Callable

from heuristics import h_admissible, largest_pitcher_first_heuristic, simple_heuristic
from states import get_child_states



def is_goal(state, target):
    return state.state[-1] == target

def parse_file(filename):
    with open(filename, "r") as file:
        text = file.read()
    buckets, target = text.split("\n")
    buckets = [int(b) for b in buckets.split(",")]
    target = int(target)
    return tuple(buckets + [None]), target

class State:
    def __init__(self, state: Tuple[int], capacities: Tuple[int], path: List=None) -> None:
        self._state = state
        self.capacities = capacities
        if path is None:
            path = []
        self.path = path
        self.cost = len(self.path)
    
    @property
    def state(self):
        return self._state
    
    def __repr__(self) -> str:
        return f"<State: {self._state}>"

    def __lt__(self, other):
        return self._state < other._state

    def get_child_states(self, seen=set()):
        children = []
        states = get_child_states(self._state, self. capacities)
        for state in states:
            if state in seen:
                continue
            path = list(self.path)
            path.append(self._state)
            children.append(State(state, self.capacities, path))
        return children


class Search:
    def __init__(self, capacities: Tuple[int], target: int=None, heuristic: Callable=None) -> None:
        self.capacities = tuple(sorted([cap for cap in capacities if cap is not None]) + [None])
        self.target = target
        self.heuristic = heuristic
        self.visited = set()
        self.pq = []
        heapq.heappush(self.pq, (0, State((0,)*len(capacities), self.capacities)))
        self.solution_state = None
        self.time_elapsed = 0
        self.timedout = False
        self.shortest_path = None

    def __repr__(self) -> str:
        return f"<Search{self.solution_state or ''}>"
        
    def search(self, heuristic=None, target=None, timeout=None, max_iterations=None, check_admissible=True):
        if self.target is None and target is None :
            raise AttributeError("No target value specified. Pass the `target` argument to the search method.")
        if self.heuristic is None and heuristic is None:
            raise AttributeError("No heuristic specified. Pass the `heuristic` argument to the search method.")
        if heuristic is None:
            heuristic = self.heuristic
        elif self.heuristic is None:
            self.heuristic = heuristic
        target = target or self.target
        solution = -1
        start = time()
        iter_count = 0
        while self.pq:
            iter_count += 1
            if timeout and time() - start > timeout:
                self.time_elapsed = time() - start
                self.timedout = True
                break
            if max_iterations and iter_count > max_iterations:
                self.time_elapsed = time() - start
                break
            state = heapq.heappop(self.pq)[1]
            if is_goal(state, target):
                solution = state.cost
                self.solution_state = state
                self.time_elapsed = time() - start
                break
            for st in state.get_child_states():
                if not st.state in self.visited:
                    if is_goal(state, target) and check_admissible:
                        self.check_admissibility(state, heuristic, st.cost)
                    self.visited.add(st.state)
                    h = heuristic(st.state, self.capacities, target)
                    cost = h + st.cost
                    heapq.heappush(self.pq, (cost, st))
            self.visited.add(state.state)
        if solution != -1 and check_admissible:
            self.check_admissibility(self.solution_state, heuristic, solution)
        self.shortest_path = solution
        return solution
    
    @classmethod
    def from_file(cls, filename, heuristic=None):
        capacities, target = parse_file(filename)
        return cls(capacities=capacities, target=target, heuristic=heuristic)

    def check_admissibility(self, state, heuristic, solution):
        if heuristic(state.state, self.capacities, self.target) != 0: # Obvious case
            if __name__ == "__main__":
                print("WARNING: Heuristic is not admissible")
            return False
        for st in state.path:
            value = heuristic(st, self.capacities, self.target)
            if value > solution:
                if __name__ == "__main__":
                    print("WARNING: Heuristic is not admissible: ")
                    print(state, solution)
                return False
        if __name__ == "__main__":
            print("Heuristic seems admissible")
        return True
        
    def h_is_admissible(self):
        return self.check_admissibility(self.solution_state, self.heuristic, self.shortest_path)
    
    def print_problem(self):
        print('='*18)
        print(f"Capacities: {self.capacities[:-1]}")
        print(f"Target: {self.target}")
        print(f"Heuristic: {self.heuristic.__name__} -> {self.heuristic.__doc__}")
        print('='*18)
        print()


if __name__ == "__main__":
    import argparse
    import glob

    parser = argparse.ArgumentParser(description="Water pitcher search solver.")

    parser.add_argument('file',
                    help='File with pitcher capacities in first line (comma separated) and target in second line.',
                    default='*')
    parser.add_argument('-hn', '--heuristic',
                    choices=['default', 'lpf', 'simple'],
                    help="Heuristic",
                    default="default")
    args = parser.parse_args()

    heuristics = {
        "default": h_admissible,
        "lpf": largest_pitcher_first_heuristic,
        "simple": simple_heuristic
    }

    file = args.file
    heuristic = heuristics.get(args.heuristic, "default")
    if file != '*':
        print("Searching...")
        s = Search.from_file(file, heuristic=simple_heuristic)
        # See if a solution exists
        s.search(timeout=3, check_admissible=False)
        if s.timedout:
            print(-1)
            exit()
        s = Search.from_file(file, heuristic=heuristic)
        s.print_problem()
        result = s.search()
        print(f"Shortest Path = {result}")
        print(f"Time elapsed: {timedelta(seconds=s.time_elapsed)}")
    else:
        results = {}
        for file in glob.glob('*.txt'):
            s = Search.from_file(file, heuristic=heuristic)
            s.print_problem()
            result = s.search(timeout=30)
            if s.timedout:
                s.search(heuristic=simple_heuristic, timeout=10)
            results[file] = result
            print(f"Result: {result}")
            print(f"Time elapsed: {timedelta(seconds=s.time_elapsed)}")
        print(results)

