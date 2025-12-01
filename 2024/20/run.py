import sys
from collections import deque

sys.setrecursionlimit(2000)

Point = tuple[int, int]
with open("input_test1", "r") as f:
    lines = list(map(str.strip, f.readlines()))
    start, end = None, None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                start = (row, col)
            if char == "E":
                end = (row, col)

    print(lines, start, end)

    def get(position: Point) -> str:
        row, col = position
        return lines[row][col]

    def in_map(position: Point) -> bool:
        row, col = position
        return 0 <= row < len(lines) and 0 <= col < len(lines[0])

    def neighbours(position: Point) -> list[Point]:
        row, col = position
        candidates = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
        return list(filter(in_map, candidates))

    all_costs = []

    def search(
        position: Point,
        visited: list[Point],
        cost: int = 0,
        first_cheat: Point = None,
        second_cheat: Point = None,
    ) -> None:
        if position in visited:
            return
        if position == end:
            print("Found end!", cost)
            all_costs.append(cost)
            return
        row, col = position
        for neighbour in neighbours(position):
            if get(neighbour) in [".", "E"]:
                search(
                    neighbour,
                    [*visited, position],
                    cost=cost + 1,
                    first_cheat=first_cheat,
                    second_cheat=second_cheat,
                )
            # Make cheat here
            if not first_cheat and get(neighbour) == "#":
                search(
                    neighbour,
                    [*visited, position],
                    cost=cost + 1,
                    first_cheat=position,
                    second_cheat=second_cheat,
                )
            if first_cheat == position and not second_cheat: #  and get(neighbour) == "#":
                search(
                    neighbour,
                    [*visited, position],
                    cost=cost + 1,
                    first_cheat=first_cheat,
                    second_cheat=position,
                )

    search(start, [])
    no_cheat_cost = max(all_costs)
    other_costs = list(map(lambda x: no_cheat_cost - x, all_costs))
    hist_costs = {}
    for cost in other_costs:
        if cost in hist_costs:
            hist_costs[cost] += 1
        else:
            hist_costs[cost] = 1
    print(hist_costs)
