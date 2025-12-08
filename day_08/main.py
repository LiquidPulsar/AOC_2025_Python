from collections import defaultdict
from heapq import nlargest, nsmallest
from math import prod
from pathlib import Path
from tqdm import tqdm
from ufds import DisjointSet

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    points:list[tuple[int,int,int]] = [*map(eval,f)]


sets = DisjointSet()
for p in points:
    sets.find(p)

distances = (
    ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2, p1, p2)
    for i,p1 in enumerate(points)
    for p2 in points[i+1:]
)

CUTOFF = 1000
distances = nsmallest(CUTOFF, distances)

for _,a,b in distances:
    sets.union(a,b)

sizes = defaultdict(int)
for p in points:
    sizes[sets.find(p)] += 1
    # print(a,b,sorted(sizes.vlues(), reverse=True))

# print(sets)
# print(sizes)
print(prod(nlargest(3, sizes.values())))

distances = (
    ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2, p1, p2)
    for i,p1 in enumerate(points)
    for p2 in points[i+1:]
)

distances = iter(sorted(distances)[CUTOFF+1:])
for _,a,b in tqdm(distances):
    sets.union(a,b)
    sizes = set()
    for p in points:
        sizes.add(sets.find(p))
        if len(sizes) > 2:
            break
    if len(sizes) == 2:
        break

for _,a,b in tqdm(distances):
    if sets.find(a) != sets.find(b):
        break
print(a[0]*b[0])