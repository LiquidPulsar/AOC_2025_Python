from heapq import nlargest
from math import prod, dist
from pathlib import Path
from scipy.cluster.hierarchy import DisjointSet
from time import perf_counter_ns

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    points:list[tuple[int,int,int]] = [*map(eval,f)]

start = perf_counter_ns()
distances = sorted(
    (dist(p1, p2), p1, p2)
    for i,p1 in enumerate(points)
    for p2 in points[i+1:]
)
end = perf_counter_ns()
print(f"Distance calc took {(end-start)/1_000_000} ms")

def solve(points: list[tuple[int,int,int]]) -> tuple[int,int]:
    sets = DisjointSet(points)

    distances = sorted(
        (dist(p1, p2), p1, p2)
        for i,p1 in enumerate(points)
        for p2 in points[i+1:]
    )

    s = 0
    for i,(_,a,b) in enumerate(distances):
        sets.merge(a,b)
        if i == 1000:
            s = prod(nlargest(3, sets._sizes.values()))

        if sets.n_subsets == 1:
            return s, a[0]*b[0]
    assert False, "Shouldn't reach here"

N_RUNS = 10
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = solve(points)
    end = perf_counter_ns()
    total += end - start
print(f"Solution took {total/N_RUNS/1_000_000} ms, result {res}")