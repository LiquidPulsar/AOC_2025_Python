from collections import defaultdict
from pathlib import Path

HOME = Path(__file__).parent

data = (HOME/"test.txt").read_text().splitlines()

curr = {data[0].index("S"):1}
splits = 0
timelines = 1

for line in data[1:]:
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
print(splits, timelines)