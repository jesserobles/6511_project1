from typing import Tuple
import itertools

def ucs(state, capacities, target):
    """h = 0 if target, else 1"""
    if state[-1] == target:
        return 0
    return 1


def simple_heuristic(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    """h = |X - t|"""
    return abs(state[-1] - target)


def largest_pitcher_first_heuristic(state: Tuple[int], capacities: Tuple[int], target: int):
    """h = d/v * s"""
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

def h_admissible(state: Tuple[int], capacities: Tuple[int], target: int):
    """h = max(2d/cmax - 1, 1)"""
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
