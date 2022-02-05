import math
from typing import Tuple
import itertools
from operator import itemgetter

def simple_heuristic(state: Tuple[int], parent_state: Tuple[int], capacities: Tuple[int], largest_capacity: int, target: int) -> int:
    return abs(state[-1] - target)


def largest_bucket_first_heuristic(state: Tuple[int], parent_state: Tuple[int], capacities: Tuple[int], largest_capacity: int, target: int) -> int:
    delta = target - parent_state[-1]

    bucket_fills_required_to_repeat_state = 0
    volumetric_potential_of_current_state = 0
    capacity_closest_to_delta = capacities[-2]  # Start with 2nd to last bucket since that is biggest

    i = 0
    for bucket in state[:-1]:  # Loop through all except for target bucket
        if abs(delta - capacities[i]) < abs(delta - capacity_closest_to_delta):
            capacity_closest_to_delta = capacities[i]

        if bucket != 0:
            bucket_fills_required_to_repeat_state += 1
            volumetric_potential_of_current_state += bucket

        i += 1

    steps_required_to_repeat_state = bucket_fills_required_to_repeat_state * 2 - 1

    # Special case where last step we poured the only full bucket into the target bucket
    if volumetric_potential_of_current_state == 0:
        volumetric_potential_of_current_state = capacity_closest_to_delta
        bucket_fills_required_to_repeat_state = 1
        steps_required_to_repeat_state = bucket_fills_required_to_repeat_state * 2 # Extra step required to fill

    h = math.floor(abs(delta)/volumetric_potential_of_current_state * steps_required_to_repeat_state)

    # Case where pouring this bucket into INF would go over our target.
    # Switch to BFS since our largest bucket first algorithm is no longer useful at this point
    # This keeps the heuristic admissable
    if volumetric_potential_of_current_state > abs(delta):
        h = 1

    return h



def complicated_heuristic(state: Tuple[int], capacities: Tuple[int], largest_capacity: int, target: int) -> int:
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


