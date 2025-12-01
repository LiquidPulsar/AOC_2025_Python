from pathlib import Path

HOME = Path(__file__).parent

curr = 50
count = count_strict = 0
count_true = 0
for i,line in enumerate((HOME / "input.txt").read_text().splitlines()):
    d,dist = line[0], int(line[1:])

    old = curr
    q, dist = divmod(dist, 100)
    count += q # full rotations
    curr += dist if d=='R' else -dist
    count += old and not (0 < curr < 100)
    curr %= 100

    count_strict += not curr
print(count_strict, count)