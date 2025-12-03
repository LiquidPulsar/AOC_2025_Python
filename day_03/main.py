from pathlib import Path

HOME = Path(__file__).parent

def combine(xs: list[int]) -> int:
    res = 0
    for x in xs:
        res = res * 10 + x
    return res

ints = tuple(range(9, -1, -1))
def best_combo(line: list[int]) -> int:
    ll = len(line)
    lim:int = ll - 11
    for c in ints:
        try:
            start = line.index(c, 0, lim)
            break
        except: pass
    
    stack = [0]*12
    p = 0
    last = -1
    for i in range(start, ll - 12):
        n = line[i]
        if p and last < n:
            p -= 1
            while p and stack[p-1] < n:
                p -= 1
            stack[p] = last = n
            p += 1
        elif p < 12:
            stack[p] = last = n
            p += 1

    l = 0
    for i in range(ll - 12, ll):
        n = line[i]
        if p and last < n:
            p -= 1
            while p > l and stack[p-1] < n:
                p -= 1
            stack[p] = last = n
            p += 1
        elif p < 12:
            stack[p] = last = n
            p += 1
        l += 1
    return combine(stack)

data = [list(map(int,line.strip())) for line in (HOME/"input.txt").open()]

from time import perf_counter_ns

N_RUNS = 4000
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = sum(map(best_combo, data))
    end = perf_counter_ns()
    total += end - start
print(f"Best combo took {total/N_RUNS/1_000_000} ms, result {res}")