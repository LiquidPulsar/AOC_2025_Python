from pathlib import Path
from math import prod

HOME = Path(__file__).parent

*lines_str,l = (HOME/"input.txt").read_text().splitlines()
lines = [*zip(*(map(int,line.split()) for line in lines_str))]
l = l.split()

funcs = {
    '+': sum,
    '*': prod
}

tot = sum(
    map(
        lambda l,sig: funcs[sig](l),
        lines, l
    )
)
print(tot)

lines_2 = [[]]
for i in range(len(lines_str[0])):
    num = 0
    for j in range(len(lines_str)):
        ch = lines_str[j][i]
        if ch != ' ':
            num = num * 10 + int(ch)
    if num:
        lines_2[-1].append(num)
    else: # no nums in this column so must be a split
        lines_2.append([])

tot_2 = sum(
    map(
        lambda l,sig: funcs[sig](l),
        lines_2, l
    )
)
print(tot_2)