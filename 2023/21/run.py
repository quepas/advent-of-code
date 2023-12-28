from collections import deque

Position = tuple[int, int]


def parse_map(lines: list[str]) -> tuple[list[str], Position]:
    garden = list(map(str.strip, lines))
    row = 0
    for line in garden:
        if line.count("S"):
            return garden, (row, line.index("S"))
        row += 1


def get_neighbours(garden: list[str], position: Position) -> list[Position]:
    row, col = position
    neighbours = []
    if row > 0 and garden[row - 1][col] in [".", "S"]:
        neighbours.append((row - 1, col))
    if row < len(garden) - 1 and garden[row + 1][col] in [".", "S"]:
        neighbours.append((row + 1, col))
    if col > 0 and garden[row][col - 1] in [".", "S"]:
        neighbours.append((row, col - 1))
    if col < len(garden[0]) - 1 and garden[row][col + 1] in [".", "S"]:
        neighbours.append((row, col + 1))
    return neighbours


with open("input") as f:
    garden_map, start_pos = parse_map(f.readlines())

    max_generation = 63
    generation = 0

    current = [start_pos]
    while generation <= max_generation:
        print(f"Generation: {generation}")
        new_current = []
        for pos in current:
            new_current.extend(get_neighbours(garden_map, pos))
        current = new_current
        generation += 1
    print(len(set(current)))
    # Q = deque([(0, start_pos)])
    # visited = set()
    # counts = {}
    # last_steps = set()
    # while len(Q) > 0:
    #     num, pos = Q.popleft()
    #     if num == 6:
    #         last_steps.add((num, pos))
    #     # if num == 66:
    #     #     break
    #     if num not in counts:
    #         counts[num] = 0
    #     counts[num] += 1
    #     if pos in visited:
    #         continue
    #     visited.add(pos)
    #     neighbours = list(map(lambda x: (num + 1, x), get_neighbours(garden_map, pos)))
    #     Q.extend(neighbours)
    #     print(neighbours)
    # all_last_steps = set()
    # print("last steps=", sorted(last_steps))
    # for n, pos in last_steps:
    #     for neigh in get_neighbours(garden_map, pos):
    #         all_last_steps.add(neigh)
    # print(len(all_last_steps), len(last_steps))

# Too low! 1027
