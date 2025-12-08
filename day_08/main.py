from heapq import nlargest
from math import prod, dist
from pathlib import Path
from scipy.cluster.hierarchy import DisjointSet

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    points:list[tuple[int,int,int]] = [*map(eval,f)]


sets = DisjointSet(points)

distances = sorted(
    (dist(p1, p2), p1, p2)
    for i,p1 in enumerate(points)
    for p2 in points[i+1:]
)

for i,(_,a,b) in enumerate(distances):
    sets.merge(a,b)
    if i == 1000:
        print(prod(nlargest(3, sets._sizes.values())))

    if sets.n_subsets == 1:
        print(a[0]*b[0])
        break