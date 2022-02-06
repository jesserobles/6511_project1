from typing import Tuple

def bfs(state, capacities, target):
    if state[-1] == target:
        return 0
    return 1


def simple_heuristic(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    return abs(state[-1] - target)


def largest_bucket_first_heuristic(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    delta = target - state[-1]
    space_available = [capacity - bucket for capacity, bucket in zip(capacities[:-1], state[:-1])]
    if delta == 0: # This is a solution state
        return 0
    if delta < 0: # There is more water in the infinite bucket than we need, so we need to pour to other buckets
        if delta not in space_available: 
            # There is no single bucket that can accomodate the excess water
            return 2
        return 1
    if delta in state[:-1]: # There is a bucket with exactly the amount needed
        return 1
    bucket_fills_required_to_repeat_state = len([bucket for bucket in state[:-1] if bucket != 0])
    volumetric_potential_of_current_state = sum(state[:-1])
    capacity_closest_to_delta = min(capacities[:-1], key=lambda x:abs(x-delta))
    steps_required_to_repeat_state = bucket_fills_required_to_repeat_state * 2 - 1
    # Special case where last step we poured the only full bucket into the target bucket
    if volumetric_potential_of_current_state == 0:
        volumetric_potential_of_current_state = capacity_closest_to_delta
        steps_required_to_repeat_state = 2 # Extra step required to fill
    return max(delta/volumetric_potential_of_current_state * steps_required_to_repeat_state, 1)

def h(state: Tuple[int], capacities: Tuple[int], target: int) -> int:
    delta = target - state[-1]
    space_available = [capacity - bucket for capacity, bucket in zip(capacities[:-1], state[:-1])]
    if delta == 0: # This is a solution state
        return 0
    if delta < 0: # There is more water in the infinite bucket than we need, so we need to pour to other buckets
        if delta not in space_available: 
            # There is no single bucket that can accomodate the excess water
            return 2
        return 1
    if delta in state[:-1]: # There is a bucket with exactly the amount needed
        return 1

    capacity_closest_to_delta = min([c for c in capacities[:-1]], key=lambda x:abs(x-delta))

    if capacity_closest_to_delta > delta:
        # This would overfill the bucket, so we need at least 2 steps: 1 to lower the volume, and a second to pour
        return 2
    # print(f"delta: {delta//capacity_closest_to_delta}")
    # capacity_closest_to_delta = min(capacities[:-1], key=lambda x:abs(x-delta))
    # Use this bucket to fill the capacity as many times as we can
    pours = 2 * delta/capacity_closest_to_delta - 1
    if state[capacities.index(capacity_closest_to_delta)] == 0:
        pours += 1
    # if pours > 36:
    #     print(f"pours: {pours}")
    print(max(pours, 1))
    return max(pours, 1)
    