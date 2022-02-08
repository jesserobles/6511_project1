from typing import Tuple
import itertools

def bfs(state, capacities, target):
    if state[-1] == target:
        return 0
    return 1


def simple_heuristic(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    return abs(state[-1] - target)


def largest_bucket_first_heuristic(state: Tuple[int], capacities: Tuple[int], target: int):
    delta = target - state[-1]
    space_available = [capacity - bucket for capacity, bucket in zip(capacities[:-1], state[:-1])]
    if delta == 0: # This is a solution state
        return 0
    if delta in state[:-1]: # There is a bucket with exactly the amount needed
        return 1
    if delta < 0: # There is more water in the infinite bucket than we need, so we need to pour to other buckets
        if delta not in space_available: 
            # There is no single bucket that can accomodate the excess water
            return 2
        return 1
    bucket_fills_required_to_repeat_state = len([bucket for bucket in state[:-1] if bucket != 0])
    volumetric_potential_of_current_state = sum(state[:-1])
    capacity_closest_to_delta = min(capacities[:-1], key=lambda x:abs(x-delta))
    steps_required_to_repeat_state = bucket_fills_required_to_repeat_state * 2 - 1
    # Special case where last step we poured the only full bucket into the target bucket
    if volumetric_potential_of_current_state == 0:
        # The best case is to use the closest bucket repeatedly until we reach the target.
        # We need to fill and pour the closest bucket, and since the closest bucket is 
        # initially empty we don't subtract 1.
        return max(2*(delta/capacity_closest_to_delta), 2)
    h = max(delta/volumetric_potential_of_current_state * steps_required_to_repeat_state, 1)
    return h

def h(state: Tuple[int], capacities: Tuple[int], target: int):
    delta = target - state[-1]
    st = state[:-1]
    space_available = [capacity - bucket for capacity, bucket in zip(capacities[:-1], st)]
    if delta == 0: # This is a solution state
        return 0
    if delta in st: # There is a bucket with exactly the amount needed
        return 1
    if delta < 0: # There is more water in the infinite bucket than we need, so we need to pour to other buckets
        if delta not in space_available: 
            # There is no single bucket that can accomodate the excess water
            return 2
        return 1
    bucket_fills_required_to_repeat_state = len([bucket for bucket in st if bucket != 0])
    volumetric_potential_of_current_state = sum(st)
    capacity_closest_to_delta = min(capacities[:-1], key=lambda x:abs(x-delta))
    steps_required_to_repeat_state = bucket_fills_required_to_repeat_state
    if volumetric_potential_of_current_state > delta:
        # Find any combinations whose sum is >= delta
        subsets = [(sum(seq), len(seq), seq) for i in range(len(st), 0, -1)
          for seq in itertools.combinations(st, i)
          if sum(seq) >= delta and not 0 in seq]
        min_len = None
        candidates = [] # There might be multiple candidates whose sum==delta
        for s in subsets:
            if s[0] == delta:
                candidates.append(s)
            if min_len is None:
                min_len = s[1]
            else:
                min_len = min(min_len, s[1])
        if candidates:
            return min(candidates, key=lambda x: x[1])[1] # Return size of smallest subset
        return min(subsets, key=lambda x: x[1])[1]
    # Special case where last step we poured the only full bucket into the target bucket
    if volumetric_potential_of_current_state == 0:
        # The best case is to use the closest bucket repeatedly until we reach the target.
        # We need to fill and pour the closest bucket, and since the closest bucket is 
        # initially empty we don't subtract 1.
        return max(2*(delta/capacity_closest_to_delta), 2)
    # This is for cases where the delta is much larger than the current volume available
    # return max(2*delta/capacity_closest_to_delta - 1, 1)
    return max(delta/volumetric_potential_of_current_state * steps_required_to_repeat_state, 1)

def largest_bucket_first_heuristic3(state: Tuple[int], capacities: Tuple[int], target: int):
    delta = target - state[-1]
    st = state[:-1]
    space_available = [capacity - bucket for capacity, bucket in zip(capacities[:-1], st)]
    if delta == 0: # This is a solution state
        return 0
    if delta in st: # There is a bucket with exactly the amount needed
        return 1
    if delta < 0: # There is more water in the infinite bucket than we need, so we need to pour to other buckets
        if delta not in space_available: 
            # There is no single bucket that can accomodate the excess water
            return 2
        return 1
    volumetric_potential_of_current_state = sum(st)
    capacity_closest_to_delta = min(capacities[:-1], key=lambda x:abs(x-delta)) 
    if volumetric_potential_of_current_state > delta:
        return 2
    # Special case where last step we poured the only full bucket into the target bucket
    if volumetric_potential_of_current_state == 0:
        # The best case is to use the closest bucket repeatedly until we reach the target.
        # We need to fill and pour the closest bucket, and since the closest bucket is 
        # initially empty we don't subtract 1.
        return max(2*(delta/capacity_closest_to_delta), 2)
    return max(2*(delta/capacity_closest_to_delta) - 1, 1)
