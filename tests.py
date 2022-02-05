from states import get_child_states

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