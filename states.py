from typing import List, Tuple
import itertools
from operator import itemgetter

def simple_heuristic(state: Tuple[int], target: int) -> int:
    return abs(sum(state) - target) 
​
def complicated_heuristic(state: Tuple[int], target: int) -> int:
    target_bucket_current = state[-1]
    delta = target - target_bucket_current
    if delta == 0: # This means we're at the solution, break early
        return 0
    if delta > 0: # Case when delta is positive, we need to add to target bucket
        subset_sums = [seq for i in range(len(state), 0, -1)
          for seq in itertools.combinations(state, i)
          if sum(seq) <= delta and not 0 in seq]
        if subset_sums: # Means that there is a subset whose sum is <= delta. How should we incorporate how close we are?
            index, element = max(enumerate(subset_sums), key=itemgetter(1))
            return abs(sum(element) - delta) * len(element) + 1
    return abs(sum(state) - target)


def get_child_states(state: Tuple[int], capacities=Tuple[int]) -> List[Tuple[int]]:
    child_states = []
    seen_child_states = {state}
    for ix, bx in enumerate(state):
        # First, consider just filling the jars that have capacity left and emptying any buckets with any water
        for i, bi in enumerate(state):
            if bi != 0 or capacities[i] is None: # Bucket has water, so we can empty it
                tmp_state = list(state)
                tmp_state[i] = 0
                tmp_state = tuple(tmp_state)
                if not tmp_state in seen_child_states:
                    seen_child_states.add(tmp_state)
                    child_states.append(tmp_state)
            if capacities[i] is not None and bi < capacities[i]: # The current bucket can be filled
                tmp_state = list(state)
                tmp_state[i] = capacities[i]
                tmp_state = tuple(tmp_state)
                if not tmp_state in seen_child_states:
                    seen_child_states.add(tmp_state)
                    child_states.append(tmp_state)
        # Now we can loop through the other buckets, and apply the rules: dump from bx to by
        if bx == 0: # bx can't contribute to any other bucket, just skip it
            continue
        for iy, by in enumerate(state):
            if ix == iy: # Don't consider pouring from the same bucket to itself.
                continue
            cap_y = capacities[iy]
            y_remaining = cap_y - by if cap_y is not None else bx # How much we can pour into by
            delta = min(y_remaining, bx) # We can only add up to the capacity for by buckets, and we can only take up to bx from bx
            if cap_y is None or by < cap_y: # bucket y has capacity to take cap_y - by from bx
                tmp_state = list(state)
                tmp_state[ix] = tmp_state[ix] - delta
                tmp_state[iy] = tmp_state[iy] + delta
                tmp_state = tuple(tmp_state)
                if not tmp_state in seen_child_states:
                    seen_child_states.add(tmp_state)
                    child_states.append(tmp_state)
    return child_states

def test_get_child_states(state, capacities, known_states):
    return set(known_states) == set(get_child_states(state, capacities))


# Tests
capacities = (2, 5, None)

state = (0, 0, 0)
known_states = [(2, 0, 0), (0, 5, 0)]
assert test_get_child_states(state, capacities, known_states)

state = (0, 5, 0)
known_states = [(2, 5, 0), (2, 3, 0), (0, 0, 5), (0, 0, 0)]
assert test_get_child_states(state, capacities, known_states)

state = (2, 0, 0)
known_states = [(0,0,0), (0,2,0), (0,0,2), (2,5,0)]
assert test_get_child_states(state, capacities, known_states)

state = (2, 5, 0)
known_states = [(0,5,0), (2,0,0), (0,5,2), (2,0,5)]
assert test_get_child_states(state, capacities, known_states)

state = (2, 3, 5)
known_states = [(0,3,5), (2,0,5), (2, 3, 0), (0,5,5), (0,3,7), (2, 0, 8), (2,5,3), (2,5,5)]
assert test_get_child_states(state, capacities, known_states)
