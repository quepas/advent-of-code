from collections import deque
from time import time_ns
from functools import partial

Point = tuple[int, ...]

MAP_SIZE = (6, 6)
MAP_SIZE = (70, 70)

NUM_ALLOWED_POINTS = 12
# NUM_ALLOWED_POINTS = 1024


def print_memory_space(memory_space: list[list[str]]) -> None:
    for row in memory_space:
        print("".join(row))


def in_memory_space(position, map_size: Point = MAP_SIZE) -> bool:
    row, col = position
    return 0 <= row < map_size[0] + 1 and 0 <= col < map_size[1] + 1


def neighbours(position: Point, map_size: Point = MAP_SIZE) -> list[Point]:
    row, col = position
    candidates = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
    return list(filter(partial(in_memory_space, map_size=map_size), candidates))


def find_exit(memory_space: list[list[str]]) -> int:
    start = (0, 0)
    end = MAP_SIZE
    explored = [start]
    Q = deque([(start, 0)])
    while Q:
        position, cost = Q.popleft()
        if position == end:
            return cost
        for neighbour in neighbours(position):
            if neighbour in explored:
                continue
            x, y = neighbour
            if memory_space[x][y] == "#":
                continue
            # memory_space[x][y] = "X"
            explored.append(neighbour)
            Q.append((neighbour, cost + 1))
            # print(neighbour)
            # print_memory_space(memory_space)


with open("input", "r") as f:
    points: list[Point] = list(
        map(lambda l: tuple(map(int, reversed(l.strip().split(",")))), f.readlines())
    )
    print("Number of all corrupted points:", len(points))
    memory_space = []
    for row in range(MAP_SIZE[0] + 1):
        memory_space.append(list("." * (MAP_SIZE[1] + 1)))

    for i in range(2900, len(points) + 1):
        t0 = time_ns()
        memory_space = []
        for row in range(MAP_SIZE[0] + 1):
            memory_space.append(list("." * (MAP_SIZE[1] + 1)))
        for j in range(i):
            x, y = points[j]
            memory_space[x][y] = "#"
        exit_steps = find_exit(memory_space)
        t1 = time_ns()
        if exit_steps:
            print("Points:", i, "; found exit in steps:", exit_steps, " in time: ", (t1 - t0) / 1e6, "ms")
        else:
            print(f"Couldn't find exit for point: {x},{y}")
            break
    # print_memory_space(memory_space)
    # print()
    # print_memory_space(memory_space)
