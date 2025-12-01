import re
from math import prod

MAP_SIZE = 103, 101
Vector2D = tuple[int, int]

def parse_robot(line: str) -> tuple[Vector2D, Vector2D]:
    m = re.match(r"p=(\d+),(\d+) v=([\d-]+),([\d-]+)", line)
    return (int(m.group(2)), int(m.group(1))), (int(m.group(4)), int(m.group(3)))

def mul(s: int, b: Vector2D) -> Vector2D:
    return s * b[0], s*b[1]

def add(a: Vector2D, b: Vector2D) -> Vector2D:
    return a[0] + b[0], a[1] + b[1]

def mod(a: Vector2D) -> Vector2D:
    return a[0] % MAP_SIZE[0], a[1] % MAP_SIZE[1]


def print_map(positions: list[Vector2D]) -> None:
    for row in range(MAP_SIZE[0]):
        for col in range(MAP_SIZE[1]):
            if (row, col) in positions:
                print(positions.count((row, col)), end="")
            else:
                print(".", end="")
        print("")

def count_robots(current_pos) -> tuple[int, int, int, int]:
    horizontal = int(MAP_SIZE[0] / 2)
    vertical = int(MAP_SIZE[1] / 2)
    num_top_left = sum(map(lambda p: p[0] < horizontal and p[1] < vertical, current_pos))
    num_top_right = sum(map(lambda p: p[0] < horizontal and p[1] > vertical, current_pos))
    num_bottom_left = sum(map(lambda p: p[0] > horizontal and p[1] < vertical, current_pos))
    num_bottom_right = sum(map(lambda p: p[0] > horizontal and p[1] > vertical, current_pos))
    return num_top_left, num_top_right, num_bottom_right, num_bottom_left

def check_symmetry(positions) -> bool:
    all_symetrical = True
    vertical = int(MAP_SIZE[1] / 2)
    for row in range(MAP_SIZE[0]):
        col = list(filter(lambda p: p[0] == row, positions))
        if len(col[:vertical]) != len(col[vertical+1:]):
            return False
    return True

with open("input", "r") as f:
    robots = list(map(lambda x: parse_robot(x.strip()), f.readlines()))
    seconds = 50
    # robots = [robots[10]]
    while seconds <= 1000000:
        print("Seconds: ", seconds)
        current_pos = []
        for p, v in robots:
            # print("Current", p, v)
            new_pos = mod(add(p, mul(seconds, v)))
            current_pos.append(new_pos)
            # print("Next", new_pos)
        # tl, tr, br, bl= count_robots(current_pos)
        # if tl == bl and br == tr:
        # if check_symmetry(current_pos):
        print_map(current_pos)
        input()
        seconds += 103


    result = prod(count_robots(current_pos))
    # Too low: 100379268
    print("Result", result)
    # Too high: 1000001, 500000
    # Not 50, 97...
