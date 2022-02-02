from typing import Tuple
import itertools
from operator import itemgetter

def simple_heuristic(state: Tuple[int], target: int) -> int:
    return abs(sum(state) - target) 

def complicated_heuristic(state: Tuple[int], target: int) -> int:
    target_bucket_current = state[-1]
    delta = target - target_bucket_current
    if delta == 0: # This means we're at the solution, break early
        return 0
    if delta > 0: # Case when delta is positive, we need to add to target bucket
        subset_sums = sorted([seq for i in range(len(state), 0, -1)
          for seq in itertools.combinations(state, i)
          if sum(seq) <= delta and not 0 in seq], key=lambda x: (-sum(x), len(x)))
        if subset_sums: # Means that there is a subset whose sum is <= delta. How should we incorporate how close we are?
            # index, element = max(enumerate(subset_sums), key=itemgetter(1))
            element = subset_sums[0] # First element gets us closest
            return abs(sum(element) - delta) * len(element) + 1
    return abs(sum(state) - target)