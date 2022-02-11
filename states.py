from typing import List, Tuple


def get_child_states(state: Tuple[int], capacities=Tuple[int]) -> List[Tuple[int]]:
    """
    Method to generate child states from the given state.
    """
    child_states = []
    seen_child_states = {state}
    for ix, bx in enumerate(state):
        if bx != 0 or capacities[ix] is None: # Bucket has water, so we can empty it
            tmp_state = list(state)
            tmp_state[ix] = 0
            tmp_state = tuple(tmp_state)
            if not tmp_state in seen_child_states:
                seen_child_states.add(tmp_state)
                child_states.append(tmp_state)
        if capacities[ix] is not None and bx < capacities[ix]: # The current bucket can be filled
            tmp_state = list(state)
            tmp_state[ix] = capacities[ix]
            tmp_state = tuple(tmp_state)
            if not tmp_state in seen_child_states:
                seen_child_states.add(tmp_state)
                child_states.append(tmp_state)
        if bx == 0: # bx can't contribute to any other bucket, just skip it
            continue
        calc_diff_pitcher_combos(state, capacities,  child_states, seen_child_states, ix, bx)
    return child_states

def calc_diff_pitcher_combos(state, capacities,  child_states, seen_child_states, ix, bx):
    """
    Method to generate states that representing pouring from one pitcher to another.
    """
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