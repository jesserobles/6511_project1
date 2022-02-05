import time

states = {}
target = 0
lowest_cost = None
bucket_fill_cost = 1


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
        heuristic = (target - (state['value'] + inf_bucket_volume)) * state['cost']
        state_to_heuristic_maps.append(
            {
                "value": state['value'],
                "heuristic": heuristic,
                "cost": state['cost'] + bucket_fill_cost  # Include cost of filling bucket from water source
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
            return
        else:  # Branch a new set of child leaves and continue to approach goal
            if lowest_cost is None or (steps + mapping['cost']) < lowest_cost:
                search(inf_bucket_volume + mapping['value'], steps + mapping['cost'])

t = 1
while t < 9:
    print("########## START RUN #############")
    print("Target: "+str(t)+", Buckets: 2,5")
    start = time.time()
    run(t)
    end = time.time()
    print("Time: "+str(end - start)+"s")
    print("########## END RUN #############")
    t+=1