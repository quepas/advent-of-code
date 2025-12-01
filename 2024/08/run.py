from itertools import combinations
from math import sqrt

Position = tuple[int, int]
with open("input", "r") as f:
    lines = list(map(str.strip, f.readlines()))

    def is_in(position: Position) -> bool:
        return 0 <= position[0] < len(lines) and 0 <= position[1] < len(lines[0])

    def distance(a: Position, b: Position) -> int:
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def diff(a: Position, b: Position) -> Position:
        return a[0] - b[0], a[1] - b[1]

    def add(a: Position, b: Position) -> Position:
        return a[0] + b[0], a[1] + b[1]

    def sub(a: Position, b: Position) -> Position:
        return a[0] - b[0], a[1] - b[1]

    antenas = {}
    # Find where are antenas
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                position = (row, col)
                if char in antenas:
                    antenas[char].append(position)
                else:
                    antenas[char] = [position]
    # For each pair of the same freq antenas, find their antinodes
    antinodes = []
    for freq, positions in antenas.items():
        for pair in combinations(positions, 2):
            disp = diff(*pair)
            antinode1 = add(pair[0], disp)
            while is_in(antinode1):
                antinodes.append(antinode1)
                antinode1 = add(antinode1, disp)
            antinode2 = sub(pair[1], disp)
            while is_in(antinode2):
                antinodes.append(antinode2)
                antinode2 = sub(antinode2, disp)
            print(freq, pair, disp)
    print(antenas)

    for freq, positions in antenas.items():
        antinodes.extend(positions)
    antinodes = set(antinodes)
    print(len(antinodes))
    print(antinodes)

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                print(char, end="")
            elif (row, col) in antinodes:
                print("#", end="")
            else:
                print(".", end="")
        print("")
