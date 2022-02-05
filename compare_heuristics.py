import bestfirstsearch
from bestfirstsearch import parse_file, bfs, Search
from heuristics import simple_heuristic, largest_bucket_first_heuristic, complicated_heuristic


files = ["default.txt", "input.txt", "input1.txt", "input2.txt", "input3.txt", "input4.txt"]
for file in files:
    if file is not None:
        bestfirstsearch.capacities, bestfirstsearch.target = parse_file(file)
        capacities = bestfirstsearch.capacities
        target = bestfirstsearch.target
        print(f"File: {file}, Capacities: {capacities}, Target: {target}")

        s = Search(capacities, bfs)
        print("\nSearching bfs...")
        result = s.search(timeout=30)
        print(result)

        iter_count = 0
        s = Search(capacities, simple_heuristic)
        print("\nSearching simple_heuristic...")
        result = s.search(timeout=30)
        print(result)

        iter_count = 0
        s = Search(capacities, complicated_heuristic)
        print("\nSearching complicated_heuristic...")
        result = s.search(timeout=30)
        print(result)

        iter_count = 0
        s = Search(capacities, largest_bucket_first_heuristic)
        print("\nSearching largest_bucket_first_heuristic...")
        result = s.search(timeout=30)
        print(result)

