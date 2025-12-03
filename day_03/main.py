from pathlib import Path

HOME = Path(__file__).parent

def combine(xs: list[int]) -> int:
    res = 0
    for x in xs:
        res = res * 10 + x
    return res

def best_combo(line: list[int]) -> int:
    stack = [0]*12
    l = 12 - len(line)
    p = 0
    
    for n in line:
        while p and stack[p-1] < n and p > l:
            p -= 1
        if p < 12:
            stack[p] = n
            p += 1
        l += 1
    return combine(stack)

data = [list(map(int,line.strip())) for line in (HOME/"input.txt").open()]

from time import perf_counter_ns

N_RUNS = 2000
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = sum(map(best_combo, data))
    end = perf_counter_ns()
    total += end - start
print(f"Best combo took {total/N_RUNS/1_000_000} ms, result {res}")