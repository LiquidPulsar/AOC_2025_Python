from pathlib import Path

HOME = Path(__file__).parent

twelve = tuple(range(100 - 12, 100)) # locks us into 100 digits but ah well
def best_combo(line: list[int]) -> int:
    stack = 0
    start = 0
    c = 9
    for lim in twelve:
        # The limit has increased by 1 each time
        # This means that it is sometimes possible to find a higher digit later on
        # But this digit must be found in the 1 new position that has opened up
        lim_1 = lim + 1
        while c >= 0:
            try:
                start = line.index(c, start, lim_1) + 1
                break
            except:
                c -= 1
        if line[lim] > c:
            for i in line[lim:]: # using indexing is slower than direct slicing!
                stack = stack * 10 + i
            return stack
        stack = stack * 10 + c
    return stack

data = [list(map(int,line.strip())) for line in (HOME/"input.txt").open()]

from time import perf_counter_ns

N_RUNS = 10_000
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = sum(map(best_combo, data))
    end = perf_counter_ns()
    total += end - start
print(f"Best combo took {total/N_RUNS/1_000_000} ms, result {res}")