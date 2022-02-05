from typing import Tuple
import itertools
from operator import itemgetter

def simple_heuristic(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    return abs(state[-1] - target)

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
    return abs(state[-1] - target)

def h(state: Tuple[int], target: int) -> int:
    global capacities
    bt = state[-1]
    delta = target - bt
    water_available = sum(state[:-1])
    if delta == 0:
        return 0
    if delta > water_available:
        # The water needed exceeds the amount available in the non-infinite buckets.
        # then the best case is that a we can pour a bucket to bt, refill a bucket, and pour to bt
        # return 3
        if water_available > 0:
            return target//max(capacities)
        else:
            return 3
    if delta < 0: 
        # The target bucket is above the value.
        # Best case is that a bucket has the correct amount missing and we pour the infinite bucket back
        return 1
    target//max(capacities)
    raise ValueError(f"Case unaccounted for: {delta}")

