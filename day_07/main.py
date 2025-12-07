from collections import defaultdict
from pathlib import Path

HOME = Path(__file__).parent

data = (HOME/"input.txt").read_text().splitlines()

# Bitset approach for p1
# Can numpy the same idea for p2 as well

# tab = str.maketrans('S^.','110')
# curr,*rest = [int(line.translate(tab), 2) for line in data]
# splits = 0
# for line in rest:
#     hits = curr & line
#     splits += hits.bit_count()
#     curr = (hits << 1) | (hits >> 1) | (curr & ~line)
# print(splits)

from time import perf_counter_ns

def solve(data):
    curr = {data[0].index("S"):1}
    splits = 0
    timelines = 1

    for line in data[2::2]:
        new_curr = defaultdict(int)
        for pos,v in curr.items():
            if line[pos] == "^":
                new_curr[pos-1] += v
                new_curr[pos+1] += v
                splits += 1
                # we had v timelines to start with, now each split into 2 so +v
                timelines += v
            else:
                new_curr[pos] += v
        curr = new_curr
    return splits, timelines

print(*solve(data))

N_RUNS = 1000
total = 0
for _ in range(N_RUNS):
    start = perf_counter_ns()
    solve(data)
    end = perf_counter_ns()
    total += end - start
print(f"Solved in {total/N_RUNS/1_000} micros")