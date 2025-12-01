from functools import partial

Position = tuple[int, int]
Trail = list[Position]
Map = list[list[int]]


def parse_line(line: str) -> list[int]:
    parsed = []
    for c in line.strip():
        if c == ".":
            parsed.append(-1)
        else:
            parsed.append(int(c))
    return parsed


def find_scores(map: Map, score: int) -> list[Position]:
    positions = []
    for row, line in enumerate(map):
        for col, value in enumerate(line):
            if value == score:
                positions.append((row, col))
    return positions


def in_map(position: Position, map_size: tuple[int, int]) -> bool:
    return 0 <= position[0] < map_size[0] and 0 <= position[1] < map_size[1]


def get_value(map: Map, position: Position) -> int:
    return map[position[0]][position[1]]


def get_neighbours(position: Position, map: Map) -> list[Position]:
    """Only in the map and with value +1 of the current position"""
    x, y = position
    value = get_value(map, position)
    map_size = len(map), len(map[0])
    return list(
        filter(
            lambda pos: get_value(map, pos) == value + 1,
            filter(
                partial(in_map, map_size=map_size),
                [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)],
            ),
        )
    )

def print_map(map: Map, visited: list[Position]) -> None:
    for row, line in enumerate(map):
        for col, value in enumerate(line):
            if (row, col) in visited:
                print("X", end="")
            elif value == -1:
                print("-", end="")
            else:
                print(value, end="")
        print("")
    input()


def find_trails(map: Map, start: Position, visited: list[Position]) -> int:
    num_trails = []
    if start in visited:
        return 0
    new_visited = [*visited, start]
    # print_map(map, new_visited)
    if get_value(map, start) == 9:
        print("Found end!")
        return [*num_trails, start]
    for next_position in get_neighbours(start, map):
        print(next_position, new_visited)
        if next_position in new_visited:
            continue
        num_trails.extend(find_trails(map, next_position, new_visited))
    return num_trails



with open("input") as f:
    map = list(map(parse_line, f.readlines()))
    starts = find_scores(map, 0)
    all_trails = 0
    all_unique_trails = 0
    for start in starts:
        trails = find_trails(map, start, [])
        print(f"Start: {start} has {trails} trails")
        print(trails)
        all_trails += len(set(trails))
        all_unique_trails += len(trails)
    print("All trails", all_trails)
    print("All unique trails", all_unique_trails)
