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


pq = PriorityQueue()
capacities = (2, 5, None)
target = 8
start = State((0, 0, 0), capacities)
pq.put((0, start))
visited = set()

while not pq.empty():
    state = pq.get()[1]
    print(f"state: {state}")
    if is_goal(state, target):
        print(f"Found: {state}")
        break
    for st in state.get_child_states():
        if not st.state in visited:
            visited.add(st.state)
            h = simple_heuristic(st.state, target)
            cost = h + st.cost
            pq.put((cost, st))
    visited.add(state.state)
    
    
    


