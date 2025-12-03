from pathlib import Path

HOME = Path(__file__).parent

from functools import lru_cache

def combine(xs: list[int]) -> int:
    res = 0
    for x in xs:
        res = res * 10 + x
    return res

def best_combo(line: list[int]) -> int:
    # Do it backwards
    curr = [0]*13

    for n in line:
        for rem in range(12,0,-1):
            curr[rem] = max(
                curr[rem-1] * 10 + n,
                curr[rem]
            )
    return curr[12]


data = [list(map(int,line.strip())) for line in (HOME/"input.txt").open()]

from time import perf_counter_ns

N_RUNS = 100
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = sum(map(best_combo, data))
    end = perf_counter_ns()
    total += end - start
print(f"Best combo took {total/N_RUNS/1_000_000} ms, result {res}")