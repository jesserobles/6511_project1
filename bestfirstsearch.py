"""
Best-First-Search(Graph g, Node start)
    1) Create an empty PriorityQueue
       PriorityQueue pq;
    2) Insert "start" in pq.
       pq.insert(start)
    3) Until PriorityQueue is empty
          u = PriorityQueue.DeleteMin
          If u is the goal
             Exit
          Else
             Foreach neighbor v of u
                If v "Unvisited"
                    Mark v "Visited"                    
                    pq.insert(v)
             Mark u "Examined"                    
End procedure
"""

from queue import PriorityQueue
from typing import List, Tuple

from heuristics import simple_heuristic
from states import get_child_states

def is_goal(state, target):
    return simple_heuristic(state.state, target) == 0

def parse_file(filename):
    with open(filename, "r") as file:
        text = file.read()
    buckets, target = text.split("\n")
    buckets = [int(b) for b in buckets.split(",")]
    target = int(target)
    return tuple(buckets + [None]), target


class State:
    def __init__(self, state: Tuple[int], capacities: Tuple[int], path: List=None) -> None:
        self._state = state
        self.capacities = capacities
        if path is None:
            path = []
        self.path = path
        self.cost = max(1, len(self.path))
    
    @property
    def state(self):
        return self._state
    
    def __repr__(self) -> str:
        return f"<State: {self._state}>"

    def __lt__(self, other):
        return self._state < other._state

    def get_child_states(self, seen=set()):
        children = []
        states = get_child_states(self._state, self. capacities)
        for state in states:
            if state in seen:
                continue
            path = list(self.path)
            path.append(self._state)
            children.append(State(state, capacities, path))
        return children



# capacities = (2, 5, None)
# target = 100
# start = State((0, 0, 0), capacities)

capacities, target = parse_file('input4.txt')
start = State((0,)*len(capacities), capacities)

visited = set()

solution = -1
max_iterations = 10000
count = 0

pq = PriorityQueue()
pq.put((0, start))
while not pq.empty():
    count += 1
    if count >= max_iterations:
        break
    state = pq.get()[1]
    print(f"state: {state}")
    if is_goal(state, target):
        print(f"Found: {state}")
        solution = state.cost
        break
    for st in state.get_child_states():
        if not st.state in visited:
            visited.add(st.state)
            h = simple_heuristic(st.state, target)
            cost = h + st.cost
            pq.put((cost, st))
    visited.add(state.state)
    
    
print(solution)


