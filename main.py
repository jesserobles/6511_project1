states = {}
target = 0


def run():
    read_input()
    print(search(0, 0))


def read_input():
    global target
    state_array = [2,5] # TODO: pass in state array from file
    target = 1 # TODO: pass in target water unit from file
    set_states(state_array)


def set_states(state_array):
    global states
    # TODO: create state memory object to include state costs and expanded states
    states = [
        {
            "value": 2,
            "cost": 1
        },
        {
            "value": 3,
            "cost": 2
        },
        {
            "value": 5,
            "cost": 1
        }
    ]


def search(inf_bucket_volume, steps):
    for state in states:
        # The goal is to reach 0, meaning the difference between our target and actual is 0.
        # Thus the state with the closest value to 0 is chosen as the best path.
        heuristic = (target - (state['value'] + inf_bucket_volume)) * state['cost']

        if heuristic == 0:  # Valid solution
            return steps + state['cost']
        elif heuristic < 0:  # Dead end, this bucket is larger than needed volume
            return -1


run()
