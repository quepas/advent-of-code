from collections import deque
from functools import partial
from itertools import product


def read_map(lines: list[str]) -> list[list[int]]:
    map_ints = []
    for line in lines:
        map_ints.append(list(map(int, line.strip())))
    (nrow, ncol) = len(map_ints), len(map_ints[0])
    dist = []
    prev = []

    for row in range(nrow):
        dist.append([int(1e30)] * ncol)
        prev.append([None] * ncol)

    return map_ints, dist, prev


def is_correct(position, nrow, ncol) -> bool:
    return 0 <= position[0] < nrow and 0 <= position[1] < ncol


def get_neighbours(map_ints: list[list[int]], position: tuple[int, int]) -> list[tuple[int, int]]:
    (nrow, ncol) = len(map_ints), len(map_ints[0])
    neighbours = [
        (position[0], position[1] - 1),  # left
        (position[0], position[1] + 1),  # right
        (position[0] - 1, position[1]),  # top
        (position[0] + 1, position[1])  # down
    ]
    return list(filter(partial(is_correct, nrow=nrow, ncol=ncol), neighbours))


def find_min(Q, dist: list[list[int]]) -> tuple[int, int]:
    (nrow, ncol) = len(dist), len(dist[0])
    min_val = int(1e30)
    min_pos = (-1, -1)
    for row, col in Q:
        if dist[row][col] < min_val:
            min_val = dist[row][col]
            min_pos = (row, col)
    return min_pos


with open("input_test_1") as f:
    heat_map, dist, prev = read_map(f.readlines())
    (nrow, ncol) = len(heat_map), len(heat_map[0])
    print(heat_map)

    Q = deque(product(range(nrow), range(ncol)))
    dist[0][0] = 0

    for d in dist:
        print(d)
    visited: list[tuple[int, int]] = []
    while len(Q) > 0:
        u = find_min(Q, dist)
        # Check if u is not third in use
        if len(visited) >= 2:
            last_two = visited[-2:]
            if last_two[0][0] == last_two[1][0] == u[0]:
                print("Third in row!")
                Q.remove(u)
                u1 = find_min(Q, dist)
                Q.append(u)
                u = u1
            if last_two[0][1] == last_two[1][1] == u[1]:
                print("Third in col!")
                Q.remove(u)
                u1 = find_min(Q, dist)
                Q.append(u)
                u = u1

        Q.remove(u)
        visited.append(u)

        for v in get_neighbours(dist, u):
            if v in Q:
                # print(f"Still in! {v}")
                alt = dist[u[0]][u[1]] + heat_map[v[0]][v[1]]
                # TODO: if 3 in the same way, find the second min !
                if alt < dist[v[0]][v[1]]:
                    dist[v[0]][v[1]] = alt
                    prev[v[0]][v[1]] = u
    for d in dist:
        print(d)
    for p in prev:
        print(p)
