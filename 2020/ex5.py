from math import floor
from typing import Tuple


def compute_seat_num(boarding_pass: str) -> int:
    row = find_idx((0, 127), boarding_pass[0:7])
    column = find_idx((0, 7), boarding_pass[7:])
    return row * 8 + column


def find_idx(r: Tuple, cmd: str):
    for c in cmd:
        diff = r[1] - r[0]
        if c in ['F', 'L']:
            r = (r[0], r[0] + floor(diff / 2))
        if c in ['B', 'R']:
            r = (r[0] + round(diff / 2), r[1])
    if cmd[-1] in ['F', 'L']:
        return r[0]
    return r[1]


seat_numbers = []
with open('input_5.txt', 'r') as f:
    for line in f.readlines():
        seat_numbers.append(compute_seat_num(line))

print('Maximal seat number is {}'.format(max(seat_numbers)))

# 878 / 504
print(seat_numbers)
for k in range(min(seat_numbers) + 1, max(seat_numbers) - 1):
    if k not in seat_numbers and k - 1 in seat_numbers and k + 1 in seat_numbers:
        print('My seat number is {}'.format(k))
        break
