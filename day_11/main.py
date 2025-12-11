from functools import cache
from pathlib import Path

HOME = Path(__file__).parent

data = {}
with open(HOME/"input.txt") as f:
    for line in f:
        a,b = line.split(":")
        data[a] = b.split()

@cache
def paths(curr: str) -> int:
    if curr == "out":
        return 1
    return sum(paths(nxt) for nxt in data[curr])

print(paths("you"))

@cache
def paths2(curr: str, dac: bool, fft: bool) -> int:
    if curr == "dac":
        dac = True
    if curr == "fft":
        fft = True
    if curr == "out":
        return dac and fft
    return sum(paths2(nxt, dac, fft) for nxt in data[curr])

print(paths2("svr", False, False))