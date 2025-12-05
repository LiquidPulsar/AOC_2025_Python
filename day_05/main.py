from bisect import bisect_right
from pathlib import Path

HOME = Path(__file__).parent

ranges,ids = (HOME/"input.txt").read_text().split("\n\n")
ranges = [list(map(int,line.split('-'))) for line in ranges.splitlines()]
ids = [*map(int, ids.splitlines())]

ranges.sort()

merged_ranges = []
current_start, current_end = ranges[0]
for start, end in ranges[1:]:
    if start <= current_end + 1:
        current_end = max(current_end, end)
    else:
        merged_ranges.append((current_start, current_end))
        current_start, current_end = start, end
merged_ranges.append((current_start, current_end))

def is_in_ranges(x: int):
    return (i := bisect_right(merged_ranges, (x, x))) and x <= merged_ranges[i-1][1]

tot = sum(map(is_in_ranges, ids))
print(tot) # part 1

print(sum(end - start + 1 for start, end in merged_ranges)) # part 2