states = {}
target = 0
lowest_cost = None


def run(t):
    global target
    global lowest_cost

    # Reset globals (just for my internal testing without using files)
    target = t
    lowest_cost = None

    read_input()
    search(0, 0)

    if lowest_cost is None:
        print(-1)
    else:
        print(lowest_cost)


def read_input():
    global target
    state_array = [2,5] # TODO: pass in state array from file
    # TODO: pass in target water unit from file
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
    global lowest_cost
    state_to_heuristic_maps = []

    # Calculate heuristic for each sibling "leaf" of a "branch" to see which one to expand
    for state in states:
        # The goal is to reach 0, meaning the difference between our target and actual is 0.
        # Thus the state with the closest value to 0 is chosen as the best path.
        heuristic = (target - (state['value'] + inf_bucket_volume)) * state['cost']
        state_to_heuristic_maps.append(
            {
                "value": state['value'],
                "heuristic": heuristic,
                "cost": state['cost']
            }
        )

    # Recurse branches until
    for mapping in sorted(state_to_heuristic_maps, key=lambda k: k['heuristic']):
        if mapping['heuristic'] < 0:  # Dead end, this bucket is larger than needed volume
            continue
        elif mapping['heuristic'] == 0:  # Valid solution
            cost = steps + mapping['cost']
            if lowest_cost is None or cost < lowest_cost:
                lowest_cost = cost
            continue
        else:  # Branch a new set of child leaves and continue to approach goal
            search(inf_bucket_volume + mapping['value'], steps + mapping['cost'])


print("Target: 1")
run(1)
print("Target: 2")
run(2)
print("Target: 3")
run(3)
print("Target: 4")
run(4)
print("Target: 5")
run(5)
print("Target: 8")
run(8)