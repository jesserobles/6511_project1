from typing import List, Tuple


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
