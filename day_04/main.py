from pathlib import Path
from unittest import result

HOME = Path(__file__).parent

data = (HOME/"input.txt").read_text().splitlines()

# tot = 0
# for i,row in enumerate(data):
#     for j,ch in enumerate(row):
#         if ch != '@':
#             continue
#         c = 0
#         for i2 in range(max(0,i-1), min(len(data),i+2)):
#             for j2 in range(max(0,j-1), min(len(row),j+2)):
#                 if data[i2][j2]==ch:
#                     c += 1
#         if c < 5: # incl. ourselves
#             tot += 1

# print(tot)

import numpy as np
from scipy.ndimage import convolve

kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
grid = np.array([[1 if ch=='@' else 0 for ch in line] for line in data])
first_n = grid.sum()
grid *= np.where(convolve(grid, kernel, mode='constant', cval=0) >= 4, 1, 0)
curr = grid.sum()
print(first_n - curr)
old_n = first_n
while curr != old_n:
    old_n = curr
    grid *= np.where(convolve(grid, kernel, mode='constant', cval=0) >= 4, 1, 0)
    # print(grid)
    curr = grid.sum()
print(first_n - curr)

