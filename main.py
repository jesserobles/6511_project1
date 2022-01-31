states = {}
target = 0
steps = -1


def run():
    print("Starting")
    read_input()

    print("Searching for solution")
    print(search())


def read_input():
    global target
    print("Reading input")
    state_array = [2,5] # TODO: pass in state array from file
    target = 8 # TODO: pass in target water unit from file
    set_states(state_array)


def set_states(state_array):
    global states
    print("Setting states")
    # TODO: create state memory object to include state costs and expanded states


def search():
    # TODO: implement A*
    return steps


run()
