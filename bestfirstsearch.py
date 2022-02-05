from datetime import timedelta
import itertools
from operator import itemgetter
from queue import PriorityQueue
import sys
from time import time
from typing import List, Tuple, Callable

from heuristics import simple_heuristic, largest_bucket_first_heuristic, complicated_heuristic
from states import get_child_states

def bfs(*args):
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

def h(state: Tuple[int], capacities: Tuple[int], largest_capacity: int, target: int) -> int:
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
        if all([st - cap != delta for st, cap in zip(state[:-1], capacities[:-1])]):
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
        self.cost = max(1, len(self.path))
    
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
            children.append(State(state, capacities, path))
        return children


class Search:
    def __init__(self, capacities: Tuple[int], heuristic: Callable) -> None:
        self.capacities = capacities
        self.heuristic = heuristic
        self.visited = set()
        self.pq = PriorityQueue()
        self.pq.put((0, State((0,)*len(capacities), self.capacities)))
        self.largest_capacity = capacities[len(capacities) - 2]

    def search(self, timeout=None, max_iterations=None):
        solution = -1
        start = time()
        iter_count = 0
        while not self.pq.empty():
            iter_count += 1
            if timeout and time() - start > timeout:
                break
            if max_iterations and iter_count > max_iterations:
                break
            state = self.pq.get()[1]
            print(f"state: {state}")
            if is_goal(state, target):
                print(f"Found: {state.path}")
                solution = state.cost
                break
            for st in state.get_child_states():
                if not st.state in self.visited:
                    self.visited.add(st.state)
                    h = self.heuristic(st.state, self.capacities, self.largest_capacity, target)
                    cost = h + st.cost
                    self.pq.put((cost, st))
            self.visited.add(state.state)
        print(f"Time: {str(time() - start)}s")
        return solution


if __name__ == "__main__":
    file = None
    if len(sys.argv) > 1:
        file = sys.argv[1]
    if file is not None:
        capacities, target = parse_file(file)
        s = Search(capacities, largest_bucket_first_heuristic)
        print("Searching...")
        result = s.search(max_iterations=300000)
        print(result)

