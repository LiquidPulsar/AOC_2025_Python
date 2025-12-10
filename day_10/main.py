from functools import cache
from pathlib import Path

from tqdm import tqdm

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    data: list[tuple[str, list[tuple[int,...]], list[int]]] = [
        (diag[1:-1], [tuple(map(int, button[1:-1].split(","))) for button in buttons], [*map(int, joltage[1:-1].split(','))])
        for diag,*buttons,joltage in map(str.split, f)
    ]

pat = str.maketrans('#.', '10')

def solve(data: list[tuple[str, list[tuple[int,...]], list[int]]]) -> int:
    tot = 0
    for diag, buttons, _ in data:
        l = len(diag)
        @cache
        def solve(tgt: int, free: frozenset[int]) -> int:
            if not tgt:
                return 0
            if not free:
                return 9999
            # check efficiency. maybe store the || of free as well?
            # Lets us check easily things like: cannot reach tgt as bits missing that cannot be set
            if tgt in free:
                return 1
            return 1 + min(
                solve(tgt ^ b, free - {b})
                for b in free
            )
        
        tgt = int(diag.translate(pat), 2)
        buttons = frozenset(sum((1 << (l - 1 - i)) for i in b) for b in buttons)
        tot += solve(tgt,  buttons)
    return tot

from time import perf_counter_ns

N_RUNS = 10
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = solve(data)
    end = perf_counter_ns()
    total += end - start
print(f"Solution took {total/N_RUNS/1_000_000} ms, result {res}")

import numpy as np
from scipy.optimize import linprog

def solve_2(data: list[tuple[str, list[tuple[int,...]], list[int]]]) -> int:
    tot = 0
    for _, buttons, joltage in tqdm(data):
        l = len(joltage)
        tgt = np.array(joltage, dtype=np.uint32)
        btns = np.array([[i in button for i in range(l)] for button in buttons], dtype=np.uint32)
        # tgt = btns @ x
        res = linprog( # milp would be better
            np.ones(len(buttons)),
            A_eq=btns.T,
            b_eq=tgt,
            bounds=(0, None),
            method='highs',
            integrality=np.ones(len(buttons), dtype=np.int8)
        ).fun
        tot += res
    return tot

N_RUNS = 1
total = 0
res = None
for _ in range(N_RUNS):
    start = perf_counter_ns()
    res = solve_2(data)
    end = perf_counter_ns()
    total += end - start
print(f"Solution 2 took {total/N_RUNS/1_000_000} ms, result {res}")