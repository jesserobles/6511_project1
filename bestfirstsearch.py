from datetime import timedelta
import itertools
from operator import itemgetter
import heapq
import sys
from time import time
from typing import List, Tuple, Callable

from heuristics import largest_bucket_first_heuristic, largest_bucket_first_heuristic2
from states import get_child_states

def bfs(state, capacities, target):
    if state[-1] == target:
        return 0
    return 1

def subset_sum(numbers, target):
    result = [seq for i in range(len(numbers), 0, -1)
          for seq in itertools.combinations(numbers, i)
          if not 0 in seq and sum(seq) <= target]
    
    return result

def get_max_subset(numbers, target):
    subsets = subset_sum(numbers, target)
    if not subsets:
        return None
    index, element = max(enumerate(map(sum, subsets)), key=itemgetter(0))
    return subsets[index]

def h(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    bt = state[-1]
    delta = target - bt
    water_available = sum(state[:-1])
    if delta == 0: # Solution
        return 0
    if delta < 0: 
        # The target bucket is above the value.
        # Best case is that a bucket has the correct amount missing and we pour the infinite bucket back
        # But a smarter approach is to check if any value has such capacity. If not, then
        # we need at least 2 pours: 1 to empty a destination bucket, and another from
        # the infinite bucket to the destination.
        if all([cap - st != delta for cap, st in zip(capacities[:-1], state[:-1])]):
            return 2
        return 1
    if delta > water_available:
        # The water needed exceeds the amount available in the non-infinite buckets.
        # then the best case is that a we can pour a bucket to bt, refill a bucket, and pour to bt
        return 3
    # Default case is when there is water available to fill the bucket.
    # Best case is that there is a single bucket with exactly the amount needed.
    # A smarter approach is 
    max_subset = get_max_subset(state[:-1], delta)
    if max_subset:
        print(f"State: {state}, Used subset {max_subset}")
        result = max(len(max_subset), 1)
        return result
    return 1

def closest(lst, k):
    highest_value = 0
    highest_index = -1
    for ix, item in enumerate(lst):
        if item > k:
            continue
        if item > highest_value:
            highest_index = ix
    return lst[highest_index]

def is_goal(state, target):
    return state.state[-1] == target
    # return simple_heuristic(state.state, target) == 0

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

    def __repr__(self) -> str:
        return f"<Search{self.solution_state or ''}>"
        
    def search(self, heuristic=None, target=None, timeout=None, max_iterations=None):
        if self.target is None and target is None :
            raise AttributeError("No target value specified. Pass the `target` argument to the search method.")
        if self.heuristic is None and heuristic is None:
            raise AttributeError("No heuristic specified. Pass the `heuristic` argument to the search method.")
        if heuristic is None:
            heuristic = self.heuristic
        target = target or self.target
        print(f"Capacities: {self.capacities[:-1]}")
        print(f"Target: {target}")
        print(f"Heuristic: {heuristic.__name__}")
        solution = -1
        start = time()
        iter_count = 0
        # while not self.pq.empty():
        while self.pq:
            iter_count += 1
            if timeout and time() - start > timeout:
                self.time_elapsed = time() - start
                break
            if max_iterations and iter_count > max_iterations:
                self.time_elapsed = time() - start
                break
            # state = self.pq.get()[1]
            state = heapq.heappop(self.pq)[1]
            if is_goal(state, target):
                print(f"Found a solution: {state.path + [state.state]}")
                solution = state.cost
                self.solution_state = state
                self.time_elapsed = time() - start
                break
            for st in state.get_child_states():
                if not st.state in self.visited:
                    if is_goal(state, target):
                        self.check_admissibility(state, heuristic, st.cost)
                    self.visited.add(st.state)
                    h = heuristic(st.state, self.capacities, target)
                    cost = h + st.cost
                    heapq.heappush(self.pq, (cost, st))
            self.visited.add(state.state)
        if solution != -1:
            self.check_admissibility(self.solution_state, heuristic, solution)
        return solution
    
    @classmethod
    def from_file(cls, filename, heuristic=None):
        capacities, target = parse_file(filename)
        return cls(capacities=capacities, target=target, heuristic=heuristic)

    def check_admissibility(self, state, heuristic, solution):
        if heuristic(state.state, self.capacities, self.target) != 0: # Obvious case
            print("WARNING: Heuristic is not admissible")
            return
        for st in state.path:
            value = heuristic(st, self.capacities, self.target)
            if value > solution:
                print("WARNING: Heuristic is not admissible")
                break
        else:
            print("Heuristic seems admissible")



if __name__ == "__main__":
    import glob
    file = None
    if len(sys.argv) > 1:
        file = sys.argv[1]
    if file is not None:
        print("Searching...")
        s = Search.from_file(file)
        result = s.search(heuristic=largest_bucket_first_heuristic2)
        print(result)
        print(f"Took: {s.time_elapsed}")
    else:
        results = {}
        for file in glob.glob('*.txt'):
            s = Search.from_file(file, heuristic=largest_bucket_first_heuristic)
            result = s.search(timeout=30)
            results[file] = result
            print(f"Result: {result}")
            print(f"Time elapsed: {s.time_elapsed}")
        print(results)

