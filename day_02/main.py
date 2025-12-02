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
    return sum_of_section(l2, 10**l2) + total_section_to(l2 - 1) if l2 >= 1 else 0


def better_num_dupes(n: int):
    if n == 0:
        return 0
    s = str(n)
    length = len(s)
    if length % 2:
        return better_num_dupes(10 ** (length - 1) - 1)

    l_half = length // 2
    l, r = int(s[:l_half]), int(s[l_half:])

    return total_section_to(l_half - 1) + sum_of_section(l_half, l - (l > r) + 1)


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
def _build_pattern(rep: int, l2: int) -> int:
    res = 0
    for _ in range(rep):
        res = res * (10**l2) + 1
    return res


build_pattern: list[list[int]] = [
    [_build_pattern(rep, l2) for l2 in range(10)] for rep in range(11)
]  # rep -> l2 -> value


def sum_of_section_general(rep: int, l2: int, end: int) -> int:
    return fast_sum_range(10 ** (l2 - 1), end) * build_pattern[rep][l2]


@lru_cache
def _total_section_to_general(rep: int, l2: int) -> int:
    return (
        sum_of_section_general(rep, l2, 10**l2) + _total_section_to_general(rep, l2 - 1)
        if l2 >= 1
        else 0
    )


total_section_to_general: list[list[int]] = [
    [_total_section_to_general(rep, l2) for l2 in range(10)] for rep in range(11)
]  # rep -> l2 -> total

divmod_table: list[list[tuple[int, int]]] = [
    [rep and divmod(i, rep) for i in range(11)] for rep in range(11)  # type: ignore
]


def better_num_dupes_general(n: int, rep: int):
    if n == 0:
        return 0
    s = str(n)
    length = len(s)
    if length < rep:
        return 0

    l_part, rem = divmod_table[length][rep]
    if rem:
        return total_section_to_general[rep][l_part]

    l = int(s[:l_part])
    # e.g. 581 or 554 with rep=3
    # need x>=555
    pat = build_pattern[rep][l_part] * l

    return total_section_to_general[rep][l_part - 1] + sum_of_section_general(
        rep, l_part, l + (pat <= n)
    )


def better_num_dupes_general_wrapper(n: int):
    return (
        better_num_dupes_general(n, 2)
        + better_num_dupes_general(n, 3)
        + better_num_dupes_general(n, 5)
        + better_num_dupes_general(n, 7)
        - better_num_dupes_general(n, 6)
        - better_num_dupes_general(n, 10)
    )


def run_pair(p):
    return better_num_dupes_general_wrapper(p[1]) - better_num_dupes_general_wrapper(
        p[0] - 1
    )


from time import perf_counter_ns

# start = perf_counter_ns()
# r1=sum(map(lambda p: num_dupes_to_naive(p[1], p[0], part_2=True), parts))
# end = perf_counter_ns()
# print(f"Naive took {(end-start)/1_000_000} ms")
# r2=sum(map(lambda p: better_num_dupes_general_wrapper(p[1]) - better_num_dupes_general_wrapper(p[0] - 1), parts))
# assert r1 == r2

# naive_times = []
# better_times = []
# for l,r in parts:
#     tot = 0
#     for _ in range(100):
#         start = perf_counter_ns()
#         num_dupes_to_naive(r, l, part_2=True)
#         end = perf_counter_ns()
#         tot += end - start
#     naive_times.append(tot / 100)

#     tot = 0
#     for _ in range(100):
#         start = perf_counter_ns()
#         better_num_dupes_general_wrapper(r) - better_num_dupes_general_wrapper(l - 1)
#         end = perf_counter_ns()
#         tot += end - start
#     better_times.append(tot / 100)

# print("Naive times (micros):", [t/1000 for t in naive_times])
# print("Better times (micros):", [t/1000 for t in better_times])
# exit()

tot = 0
N_RUNS = 10000
for i in range(N_RUNS):
    start = perf_counter_ns()
    r2 = sum(
        map(
            run_pair,
            parts,
        )
    )
    end = perf_counter_ns()
    tot += end - start
print(f"Better took {tot/N_RUNS/1000} micros")
# print(total_section_to_general.cache_info())
