from datetime import timedelta
import glob

from bestfirstsearch import Search
from heuristics import h_admissible, largest_pitcher_first_heuristic, simple_heuristic


results = {}
for file in glob.glob('*.txt'):
    print()
    print(file)
    heuristic = largest_pitcher_first_heuristic if "input4" in file else h_admissible
    s = Search.from_file(file, heuristic=heuristic)
    s.print_problem()
    result = s.search(timeout=0.8)
    if s.timedout:
        print("result = -1")
        results[file] = -1
        continue
    results[file] = result
    print(f"Result: {result}")
    print(f"Time elapsed: {timedelta(seconds=s.time_elapsed)}")
    print()
print(results)

for file, result in results.items():
    print(f"{file} = {result}")