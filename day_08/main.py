from heapq import nlargest, heapify, heappop, heappush
from math import prod
from pathlib import Path
from itertools import count, starmap
from scipy.spatial import KDTree
from scipy.cluster.hierarchy import DisjointSet
from time import perf_counter_ns

HOME = Path(__file__).parent

with open(HOME / "input.txt") as f:
    points: list[tuple[int, int, int]] = [*map(eval, f)]

N = 18 # Prefetch distance
def shortest_dists(pos):
    # Returns generator of (distance, i, j) in order of increasing distance
    # O(log n) per yielded distance
    tree = KDTree(pos)
    distheap = []

    # For a given point, generate its nearest neighbours in order
    def gen_ns(i, p):
        for k in count(2):
            ds, inds = tree.query(p, k=[*range(k, k+N)])  # type: ignore (scipy stubs bad)
            for j in range(N):
                yield ds[j], i, int(inds[j])  # type: ignore

    gens = [*starmap(gen_ns, enumerate(pos))]
    distheap = [*map(next, gens)]  # Prime with first neighbour of each point

    heapify(distheap)
    while distheap:
        distance, i, j = heappop(distheap) # O(log n)
        if j > i:  # dedupe
            yield distance, i, j
        next_neighb = next(gens[i])  # Get next neighbour for point i, O(log n) amortized
        if next_neighb[0] < 1e100:
            heappush(distheap, next_neighb)

# from collections import deque
# from itertools import islice
# consumer = deque(maxlen=0)
# for N in range(15, 26):
#     N_RUNS = 1000
#     total = 0
#     for _ in range(N_RUNS):
#         start = perf_counter_ns()
#         consumer.extend(islice(shortest_dists(points), 4603)) # By inspection, we need 4602 edges for my input
#         end = perf_counter_ns()
#         total += end - start
#     print(f"Solution {N} took {total/N_RUNS/1_000_000} ms)


def solve(points: list[tuple[int, int, int]]) -> tuple[int, int]:
    sets = DisjointSet(range(len(points)))

    distances = shortest_dists(points)

    s = 0
    for i, (_, j, k) in enumerate(distances):
        sets.merge(j, k)
        if i == 1000:
            s = prod(nlargest(3, sets._sizes.values()))

        if sets.n_subsets == 1:
            return s, points[j][0] * points[k][0]
    assert False, "Shouldn't reach here"

N_RUNS = 100
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = solve(points)
    end = perf_counter_ns()
    total += end - start
print(f"Solution {N} took {total/N_RUNS/1_000_000} ms, result {res}")
