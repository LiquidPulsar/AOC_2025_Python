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

"""
Visible horizon:
...S...
..SSS..
.SSSSS.

let s0 be initial index S in line 0
line 1: width 3, s0-1 to s0+1
line 2: width 5, s0-2 to s0+2
...
line n: width 2n+1, s0-n to s0+n
"""

def solve(data):
    s = data[0].index("S")
    width = 1
    curr = [1]
    splits = 0
    timelines = 1

    for line in data[2::2]: # half the lines are empty!
        width += 2
        s -= 1
        new_curr = [0]*width
        for pos,v in enumerate(curr, start=s+1): # true index in prev row
            if v == 0:
                continue
            # print(line,pos,v)
            if line[pos] == "^":
                new_curr[pos-1-s] += v
                new_curr[pos+1-s] += v
                splits += 1
                # we had v timelines to start with, now each split into 2 so +v
                timelines += v
            else:
                new_curr[pos-s] += v
        curr = new_curr
    return splits, timelines

print(*solve(data))
# exit()

N_RUNS = 1000
total = 0
for _ in range(N_RUNS):
    start = perf_counter_ns()
    solve(data)
    end = perf_counter_ns()
    total += end - start
print(f"Solved in {total/N_RUNS/1_000} micros")