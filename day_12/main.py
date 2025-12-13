from pathlib import Path
import re

HOME = Path(__file__).parent

*shapes,regions = (HOME/"test.txt").read_text().split("\n\n")
shapes = [
    shape.split("\n")[1:] # drop the index line
    for shape in shapes
]
areas = [sum(line.count("#") for line in shape) for shape in shapes]

def parse_region(region: str) -> tuple[int, int, list[int]]:
    match = re.match(r"(\d+)x(\d+): ((?:\d+ ?)*)", region)
    assert match is not None, f"Invalid region format: {region}"
    width, height, counts = match.groups()
    return int(width), int(height), list(map(int, counts.split()))

regions = list(map(parse_region, regions.splitlines()))
# 35x35 to 50x50 regions
regions.sort()

print(shapes)
print(regions)

tot = 0
fails = 0
for width, height, counts in regions:
    print(f"Region {width}x{height} with counts {counts}")
    if sum(map(int.__mul__, areas, counts)) > width * height:
        print("  No valid arrangement possible (area mismatch)")
    elif sum(len(s)*len(s[0])*c for s,c in zip(shapes, counts)) <= width * height:
        print(" Valid arrangement possible (maybe?)")
        tot += 1  # Placeholder for actual arrangement logic
    else:
        fails += 1
print(tot, fails)