from functools import lru_cache
from pathlib import Path

HOME = Path(__file__).parent

parts = [
    tuple(map(int, p.split("-"))) for p in (HOME / "input.txt").read_text().split(",")
]

import re

pat1 = re.compile(r"(\d+)\1")
pat2 = re.compile(r"(\d+)\1+")

def num_dupes_to_naive(n: int, start=1, part_2=False):
    pat = pat2 if part_2 else pat1
    return sum(filter(lambda x: pat.fullmatch(str(x)), range(start, n + 1)))


# sum of 11*x for x in range(1,10)
# sum of 101*x for x in range(10,100)

def fast_sum_range(a, b):
    return (a + b - 1) * (b - a) // 2


# @lambda f: lambda x,y,z: (lambda res: print(f"{x,y,z} -> {res}") or res)(f(x,y,z))
def sum_of_section(l2: int, end: int) -> int:
    return fast_sum_range(10 ** (l2 - 1), end) * (10**l2 + 1)


@lru_cache
def total_section_to(l2: int) -> int:
    return (
        sum_of_section(l2,10**l2) + total_section_to(l2 - 1)
        if l2 >= 1
        else 0
    )


def better_num_dupes(n: int):
    if n == 0:
        return 0
    s = str(n)
    length = len(s)
    if length % 2 == 1:
        return better_num_dupes(10 ** (length - 1) - 1)

    l_half = length // 2
    l, r = map(int, (s[:l_half], s[l_half:]))

    return total_section_to(l_half - 1) + sum_of_section(
        l_half, l - (l > r) + 1
    )


# print(sum_of_section(4, 10, 100) + sum_of_section(2, 1, 10))
# print("="*10)
# # print([101*x for x in range(10,100)])
# print(num_dupes_to_naive(9900))
# print(better_num_dupes(9900))

# for n in [0,9,10,11,22,99,100,101,110,111,121,200,212,999,1000,9999,10000,12321,1234321,12344321]:
# # for n in [99]:
#     naive = num_dupes_to_naive(n)
#     better = better_num_dupes(n)
#     assert naive == better, f"Mismatch for {n}: {naive} != {better}"
#     print(f"{n}: {naive}")


from time import perf_counter_ns

# start = perf_counter_ns()
# r1=sum(map(lambda p: num_dupes_to_naive(p[1], p[0]), parts))
# end = perf_counter_ns()
# print(f"Naive took {(end-start)/1_000_000} ms")
# r2=sum(map(lambda p: better_num_dupes(p[1]) - better_num_dupes(p[0] - 1), parts))
# assert r1 == r2

# N_RUNS = 100000
# total = 0
# for _ in range(N_RUNS):
#     start = perf_counter_ns()
#     r2=sum(map(lambda p: better_num_dupes(p[1]) - better_num_dupes(p[0] - 1), parts))
#     end = perf_counter_ns()
#     total += end - start
# print(f"Better took {total/N_RUNS/1_000} micros")

# exit()

###################################

# 3 -> 111, 10101
@lru_cache
def build_pattern(rep: int, l2: int) -> int:
    res = 0
    for _ in range(rep):
        res = res * (10 ** l2) + 1
    return res

def sum_of_section_general(rep: int, l2: int, end: int) -> int:
    return fast_sum_range(10 ** (l2 - 1), end) * build_pattern(rep, l2)

@lru_cache
def total_section_to_general(rep: int, l2: int) -> int:
    return (
        sum_of_section_general(rep, l2, 10**l2) + total_section_to_general(rep, l2 - 1)
        if l2 >= 1
        else 0
    )

def better_num_dupes_general(n: int, rep: int):
    if n == 0:
        return 0
    s = str(n)
    length = len(s)
    if length < rep: return 0

    l_part, rem = divmod(length, rep)
    if rem:
        return total_section_to_general(rep, l_part)

    l = int(s[:l_part])
    # e.g. 581 or 554 with rep=3
    # need x>=555
    pat = build_pattern(rep, l_part) * l

    return total_section_to_general(rep, l_part - 1) + sum_of_section_general(
        rep, l_part, l + (pat <= n)
    )

def better_num_dupes_general_wrapper(n: int):
    return sum(better_num_dupes_general(n, rep) for rep in [2,3,5,7]) - sum(better_num_dupes_general(n, rep) for rep in [6,10])

# n = 581
# print(num_dupes_to_naive(n,part_2=True))
# print(*(better_num_dupes_general(n, x) for x in [2,3,5,6,7,10,15]))
# print(better_num_dupes_general_wrapper(n))

# print(sum(11*n for n in range(1,10))+sum(111*n for n in range(1,6)))
# exit()

# # for n in [0,9,10,11,22,99,100,101,110,111,121,200,212,999,1000,9999,10000,12321,1234321,12344321]:
# # # for n in [99]:
# #     naive = num_dupes_to_naive(n,part_2=True)
# #     better = better_num_dupes_general_wrapper(n)
# #     assert naive == better, f"Mismatch for {n}: {naive} != {better}"
# #     print(f"{n}: {naive}")

# # print(max(len(str(b)) for a,b in parts)) # 10 digits max

# for a,b in parts:
#     r1 = num_dupes_to_naive(b, a, part_2=True)
#     r2 = better_num_dupes_general_wrapper(b) - better_num_dupes_general_wrapper(a - 1)
#     if r1 != r2:
#         print(f"Mismatch for {a}-{b}: {r1} != {r2}")
#     else:
#         print(f"{a}-{b}: {r1}")


from time import perf_counter_ns

# start = perf_counter_ns()
# r1=sum(map(lambda p: num_dupes_to_naive(p[1], p[0], part_2=True), parts))
# end = perf_counter_ns()
# print(f"Naive took {(end-start)/1_000_000} ms")
# r2=sum(map(lambda p: better_num_dupes_general_wrapper(p[1]) - better_num_dupes_general_wrapper(p[0] - 1), parts))
# assert r1 == r2

tot = 0
N_RUNS = 10000
for i in range(N_RUNS):
    start = perf_counter_ns()
    build_pattern.cache_clear()
    total_section_to_general.cache_clear()

    r2=sum(map(lambda p: better_num_dupes_general_wrapper(p[1]) - better_num_dupes_general_wrapper(p[0] - 1), parts))
    end = perf_counter_ns()
    tot += end - start
print(f"Better took {tot/N_RUNS/1000} micros")
# print(total_section_to_general.cache_info())