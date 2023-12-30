from collections import deque
from enum import Enum
from itertools import repeat
from typing import Optional


class DigMove(str, Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


class DigInstruction:

    def apply(self, start_hole):
        pass


DigInstruction = tuple[DigMove, int, str]
Hole = tuple[int, int]


def parse_dig_plan(lines: list[str]) -> list[DigInstruction]:
    instructions = []
    for line in lines:
        move, length, color = line.strip().split()
        instructions.append((DigMove(move), int(length), color))
    return instructions


def parse_dig_plan2(lines: list[str]) -> list[DigInstruction]:
    instructions = []
    for line in lines:
        _, _, color = line.strip().split()
        length = int(color.strip()[2:7], base=16)
        print(length)
        move = int(color[7:8])
        if move == 0:
            move = DigMove.RIGHT
        elif move == 1:
            move = DigMove.DOWN
        elif move == 2:
            move = DigMove.LEFT
        elif move == 3:
            move = DigMove.UP
        instructions.append((DigMove(move), int(length), color))
    return instructions


def dig(plan: list[DigInstruction]) -> list[Hole]:
    current_hole = (0, 0)  # The starting point
    holes = [current_hole]
    to_dig = deque(plan)
    while len(to_dig) > 0:
        move, length, color = to_dig.popleft()
        if move == DigMove.RIGHT:
            new_holes = list(zip(repeat(current_hole[0]), range(current_hole[1] + 1, current_hole[1] + length + 1)))
            current_hole = new_holes[-1]
            holes.extend(new_holes)
        elif move == DigMove.DOWN:
            new_holes = list(zip(range(current_hole[0] + 1, current_hole[0] + length + 1), repeat(current_hole[1])))
            current_hole = new_holes[-1]
            holes.extend(new_holes)
        elif move == DigMove.LEFT:
            new_holes = list(zip(repeat(current_hole[0]), range(current_hole[1] - 1, current_hole[1] - length - 1, -1)))
            current_hole = new_holes[-1]
            holes.extend(new_holes)
        elif move == DigMove.UP:
            new_holes = list(zip(range(current_hole[0] - 1, current_hole[0] - length - 1, -1), repeat(current_hole[1])))
            current_hole = new_holes[-1]
            holes.extend(new_holes)
        # holes.append()
        # Take out the duplicated end-start hole
    holes.pop()
    # Offset holes, so that the start point is at (0, 0)
    # rows = list(map(lambda t: t[0], holes))
    # cols = list(map(lambda t: t[1], holes))
    # print(f"Row offset: {-min(rows)}")
    # print(f"Col offset: {-min(cols)}")
    # holes = list(map(lambda hole: (hole[0] - min(rows), hole[1] - min(cols)), holes))
    # print(f"Produced holes: {sorted(holes)}")
    return sorted(holes)


def count_in_row(holes: list[Hole], all_holes) -> int:
    segments = divide_row_into_segments(holes)
    # filtered_segments = list(filter(partial(both_way_segment, all_holes=all_holes), segments))
    interior = 0
    in_interior = False
    filtered_segments = []
    for idx in range(len(segments)):
        segment = segments[idx]
        if in_interior:
            if both_way_segment(segment, all_holes):
                filtered_segments.append(segment)
                in_interior = False
            else:
                filtered_segments.append(segment)
            distance = segments[idx][0][1] - segments[idx - 1][-1][1] - 1
            interior += distance
        elif not in_interior:
            if not both_way_segment(segment, all_holes):
                continue
            else:
                in_interior = True
                filtered_segments.append(segment)
    # print(interior)
    # print(filtered_segments)
    # cols = set(map(lambda hole: hole[1], holes))
    # full_cols = set(range(min(cols), max(cols) + 1))
    # print(cols, full_cols, len(full_cols.difference(cols)))
    # return len(full_cols.difference(cols))
    return interior


def divide_row_into_segments(holes: list[Hole]) -> list[list[Hole]]:
    segments = []
    current = []
    for hole in holes:
        if not current:
            current.append(hole)
            continue
        distance = hole[1] - current[-1][1]
        if distance == 1:
            current.append(hole)
        else:
            segments.append(current)
            current = [hole]
    if current:
        segments.append(current)
    return segments


def both_way_segment(segment: list[Hole], all_holes: list[Hole]) -> bool:
    # Must be a part of a vertical wall
    if len(segment) == 1:
        return True
    first = segment[0]
    last = segment[-1]
    first_up_flag = (first[0] - 1, first[1]) in all_holes
    last_up_flag = (last[0] - 1, last[1]) in all_holes
    last_down_flag = (last[0] + 1, last[1]) in all_holes
    first_down_flag = (first[0] + 1, first[1]) in all_holes
    return first_up_flag and last_down_flag or first_down_flag and last_up_flag


def count_interior_holes(holes: list[Hole]) -> int:
    idx = 0
    current_idx = 1
    current_row = min(map(lambda hole: hole[0], holes))
    row = []
    interior_holes = 0
    while idx < len(holes):
        current = holes[idx]
        if current[0] != current_row:
            # print(f"Row {current_idx}: ", end="")
            interior_holes += count_in_row(row, holes)
            row = [current]
            current_row = current[0]
            current_idx += 1
        else:
            row.append(holes[idx])
        idx += 1
    interior_holes += count_in_row(row, holes)
    return interior_holes


def print_holes(holes: list[Hole]) -> None:
    rows = list(map(lambda hole: hole[0], holes))
    cols = list(map(lambda hole: hole[1], holes))

    for row in range(min(rows), max(rows) + 1):
        for col in range(min(cols), max(cols) + 1):
            if (row, col) in holes:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def next_diag_hole(hole: Hole, max_rows: int, max_cols: int) -> Optional[Hole]:
    if hole[0] < max_rows and hole[1] < max_cols:
        return hole[0] + 1, hole[1] + 1
    else:
        return None


def count_in(holes: list[Hole]):
    rows = list(map(lambda hole: hole[0], holes))
    cols = list(map(lambda hole: hole[1], holes))
    diagonal_start = list(zip(range(max(rows), min(rows) - 1, -1), repeat(min(cols))))
    diagonal_start.extend(zip(repeat(min(rows)), range(min(cols), max(cols) + 1)))
    total_count = 0
    prev = None
    for start in diagonal_start:
        current = start
        count = 0
        in_count = 0
        while current is not None:
            if current in holes and (current[0] + 1, current[1] + 1) not in holes:
                count += 1
            elif count % 2 == 1:
                in_count += 1
            prev = current
            current = next_diag_hole(current, max(rows), max(cols))
        total_count += in_count
        print(f"Diag {start}: {in_count}")
    return total_count


with open("input") as f:
    dig_plan = parse_dig_plan2(f.readlines())
    print(dig_plan)
    holes = dig(dig_plan)
    # print(holes)
    # print(len(holes))
    # print_holes(holes)
    interior_holes = count_interior_holes(holes)
    # interior_holes = count_in(holes)
    print(f"Total holes: {len(holes) + interior_holes}")

# input
# 44989 - too low
# 45060
# 45082
# 46359 -- good !
# 46539
# 46588 - too high
# 64303 - too high
#
