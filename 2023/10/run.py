from collections import deque
from enum import Enum
from itertools import repeat
from typing import Optional


class Tile(str, Enum):
    VERTICAL_PIPE = "|"
    HORIZONTAL_PIPE = "-"
    TOP_RIGHT_BEND = "L"
    TOP_LEFT_BEND = "J"
    BOTTOM_LEFT_BEND = "7"
    BOTTOM_RIGHT_BEND = "F"
    GROUND = "."
    STARTING_POINT = "S"


Position = tuple[int, int]
MapSize = tuple[int, int]
PipeMap = tuple[MapSize, list[list[Tile]]]  # nrows, ncols, tiles!


def parse_map(lines: list[str]) -> tuple[Position, PipeMap]:
    pipe_map = []
    line_counter = 0
    map_line = []
    start_position = None
    for line in lines:
        map_line = list(map(Tile, line.strip()))
        try:
            start_position = (line_counter, map_line.index(Tile.STARTING_POINT))
        except ValueError:
            pass
        pipe_map.append(map_line)
        line_counter += 1
    return start_position, ((line_counter, len(map_line)), pipe_map)


def get_neighbours(position: Position, map_size: MapSize, pipe_map: PipeMap) -> list[Position]:
    (row, col) = position
    (nrow, ncol) = map_size

    # Based on current tile, check only possible tiles
    current_tile = pipe_map[row][col]
    check_top = current_tile in [Tile.VERTICAL_PIPE, Tile.TOP_RIGHT_BEND, Tile.TOP_LEFT_BEND]
    check_bottom = current_tile in [Tile.VERTICAL_PIPE, Tile.BOTTOM_LEFT_BEND, Tile.BOTTOM_RIGHT_BEND]
    check_left = current_tile in [Tile.HORIZONTAL_PIPE, Tile.TOP_LEFT_BEND, Tile.BOTTOM_LEFT_BEND]
    check_right = current_tile in [Tile.HORIZONTAL_PIPE, Tile.TOP_RIGHT_BEND, Tile.BOTTOM_RIGHT_BEND]

    if current_tile == Tile.STARTING_POINT:
        check_top, check_bottom, check_left, check_right = True, True, True, True
    values = []
    # Check top
    if row > 0 and check_top:
        tile = pipe_map[row - 1][col]
        if tile in [Tile.VERTICAL_PIPE, Tile.BOTTOM_LEFT_BEND, Tile.BOTTOM_RIGHT_BEND, Tile.STARTING_POINT]:
            values.append((row - 1, col))
    # Check right
    if col + 1 < ncol and check_right:
        tile = pipe_map[row][col + 1]
        if tile in [Tile.HORIZONTAL_PIPE, Tile.TOP_LEFT_BEND, Tile.BOTTOM_LEFT_BEND, Tile.STARTING_POINT]:
            values.append((row, col + 1))
    # Check bottom
    if row + 1 < nrow and check_bottom:
        tile = pipe_map[row + 1][col]
        if tile in [Tile.VERTICAL_PIPE, Tile.TOP_RIGHT_BEND, Tile.TOP_LEFT_BEND, Tile.STARTING_POINT]:
            values.append((row + 1, col))
    # Check left
    if col > 0 and check_left:
        tile = pipe_map[row][col - 1]
        if tile in [Tile.HORIZONTAL_PIPE, Tile.TOP_RIGHT_BEND, Tile.BOTTOM_RIGHT_BEND, Tile.STARTING_POINT]:
            values.append((row, col - 1))

    # print(values)
    if current_tile == Tile.STARTING_POINT:
        assert len(values) == 2, "Starting point should connect to two pipes!"

    return values


with open("input") as f:
    starting_position, (map_size, pipe_map) = parse_map(f.readlines())
    print(f"Starting position = {starting_position}")
    print(get_neighbours(starting_position, map_size, pipe_map))

    to_visit = deque([(starting_position, 0)])
    visited_positions = set()
    visited_tiles = {}
    max_steps = 0
    while len(to_visit) > 0:
        current, steps = to_visit.popleft()
        if current in visited_positions:
            continue
        max_steps = max(max_steps, steps + 1)
        visited_positions.add(current)
        visited_tiles[current] = steps
        new_positions = list(map(lambda p: (p, steps + 1), filter(lambda pos: pos not in visited_positions,
                                                                  get_neighbours(current, map_size, pipe_map))))
        to_visit.extend(new_positions)
    print(f"Max steps: {max_steps - 1}")
    # print(visited_tiles)
    #
    pipe_map_loop = pipe_map.copy()
    (nrow, ncol) = map_size
    for row in range(nrow):
        for col in range(ncol):
            if (row, col) not in visited_tiles:
                pipe_map_loop[row][col] = Tile.GROUND

    total_count = 0
    diagonal_start = list(zip(range(row, 0, -1), repeat(0)))
    diagonal_start.extend(zip(repeat(0), range(col + 1)))
    print("diagolan start: ", diagonal_start)


    def is_last_diag_move(position) -> bool:
        r, c = position
        return r + 1 > row or c + 1 > col


    def next_move(position) -> Optional[tuple[int, int]]:
        if is_last_diag_move(position):
            return None
        else:
            r, c = position
            return r + 1, c + 1


    for start in diagonal_start:
        current = start
        count = 0
        print("\nStart diag:")
        while current is not None:
            print(current, end=",")
            (nrow, ncol) = current
            tile = pipe_map_loop[nrow][ncol]
            if tile in [Tile.VERTICAL_PIPE, Tile.HORIZONTAL_PIPE, Tile.TOP_LEFT_BEND, Tile.BOTTOM_RIGHT_BEND,
                        Tile.STARTING_POINT]:
                count += 1
            elif tile == Tile.GROUND and count % 2 == 1:
                print(f" IN: {current} = {tile}")
                total_count += 1
            current = next_move(current)
    print(f"Total in: {total_count}")
