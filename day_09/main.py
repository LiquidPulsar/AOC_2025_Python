from itertools import combinations
from pathlib import Path

from tqdm import tqdm

HOME = Path(__file__).parent

data = (HOME/"input.txt").read_text().splitlines()
positions = [tuple(map(int,line.split(","))) for line in data]

best_a = None
best_b = None
best_area = None

def area(p1, p2):
    dx = abs(p1[0]-p2[0]) + 1
    dy = abs(p1[1]-p2[1]) + 1
    return dx * dy

for i,p1 in enumerate(positions):
    for j,p2 in enumerate(positions):
        if i < j:
            break
        a = area(p1, p2)
        if best_area is None or a > best_area:
            best_area = a
            best_a = p1
            best_b = p2

print(best_area)

"""
..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............

All points linked to next, prev.
From a given point, go in 4 directions?
How to know smth is inside?


for a point x,y
can I go right to x' without hitting a .?
Sparse grid, so need efficient lookup
Store height of all boundaries at sorted x ascending

Then we binary search to the right for next boundary that crosses us
Repeat for left

Sweep a line horizontally across:
Currently, what options do we have to the left of us?
For each point left of us, store the min and max y it can hit


2 important points in the polygon:
can start solve from there
Then only need to check points inside the polygon
Kinda cheating tho, want general solution

Will leave thoughts here for now:
On a well-behaved polygon, do line sweep.
For each (point,dir) currently considered, where dir is TopLeft or BottomLeft
Store the boundary y value it is constrained by
Whenever this is shrunk (either up or down for TL, BL respectively), we can test a new area candidate

Ill-behaved polygons which go back on themselves may cause issues with this approach though,
so a more general approach will be needed.

Also note: Low number of unique x and y values, so can compress coordinates
and use a flood-fill style approach to knowing if we're in the polygon or not.
"""
# import matplotlib.pyplot as plt
# xs, ys = zip(*(positions + [positions[0]]))

# plt.figure(figsize=(10, 8))
# plt.plot(xs, ys, 'b-o')
# plt.fill(xs, ys, alpha=0.3)
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Polygon from Positions')
# plt.grid(True)
# plt.axis('equal')
# plt.show()

from shapely.geometry import Polygon
from math import comb

def tcombinations(iterable, r):
    return tqdm(combinations(iterable, r), total=comb(len(iterable), r))

polygon = Polygon(positions)
best_area = max(
    area(p1, p2)
    for p1, p2 in tcombinations(positions, 2)
    if polygon.covers(Polygon([p1, (p1[0],p2[1]), p2, (p2[0],p1[1])]))
)
print(best_area)
