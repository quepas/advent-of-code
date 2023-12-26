from collections import deque
from itertools import repeat


class BeamDirection:
    LEFT = 1
    RIGHT = 2
    UP = 4
    DOWN = 8


BeamVectors = {
    BeamDirection.LEFT: (0, -1),
    BeamDirection.RIGHT: (0, 1),
    BeamDirection.UP: (-1, 0),
    BeamDirection.DOWN: (1, 0)
}


def read_contraption(lines: list[str]) -> list[list[str]]:
    contraption = []
    for line in lines:
        contraption.append([k for k in line.strip()])
    return contraption


def follow_beam(contraption, current, direction, energized_fields):
    (nrow, ncol) = len(contraption), len(contraption[0])
    dir = BeamVectors[direction]
    current = (current[0] + dir[0], current[1] + dir[1])
    new_beams = []
    while 0 <= current[0] < nrow and 0 <= current[1] < ncol:
        ch = contraption[current[0]][current[1]]
        if current in energized_fields and direction in energized_fields[current]:
            break
        if current in energized_fields:
            energized_fields[current].append(direction)
        else:
            energized_fields[current] = [direction]
        if ch == ".":
            dir = BeamVectors[direction]
        if ch == "|":
            if direction in [BeamDirection.LEFT, BeamDirection.RIGHT]:
                new_beams.extend([(current, BeamDirection.UP), (current, BeamDirection.DOWN)])
                break
        if ch == "-":
            if direction in [BeamDirection.UP, BeamDirection.DOWN]:
                new_beams.extend([(current, BeamDirection.LEFT), (current, BeamDirection.RIGHT)])
                break
        if ch == "\\":
            if direction == BeamDirection.LEFT:
                new_beams.append((current, BeamDirection.UP))
            elif direction == BeamDirection.RIGHT:
                new_beams.append((current, BeamDirection.DOWN))
            elif direction == BeamDirection.DOWN:
                new_beams.append((current, BeamDirection.RIGHT))
            elif direction == BeamDirection.UP:
                new_beams.append((current, BeamDirection.LEFT))
            break
        if ch == "/":
            if direction == BeamDirection.LEFT:
                new_beams.append((current, BeamDirection.DOWN))
            elif direction == BeamDirection.RIGHT:
                new_beams.append((current, BeamDirection.UP))
            elif direction == BeamDirection.DOWN:
                new_beams.append((current, BeamDirection.LEFT))
            elif direction == BeamDirection.UP:
                new_beams.append((current, BeamDirection.RIGHT))
            break
        current = (current[0] + dir[0], current[1] + dir[1])
    return energized_fields, new_beams


def start_follow_beam(contraption, current, direction):
    to_follow = deque([(current, direction)])
    energized_fields = dict()

    while len(to_follow) > 0:
        current, direction = to_follow.popleft()
        energy, new_beams = follow_beam(contraption, current, direction, energized_fields)
        to_follow.extend(new_beams)
    return energized_fields


with open("input") as f:
    contraption = read_contraption(f.readlines())
    (nrow, ncol) = len(contraption), len(contraption[0])

    start_points = {
        BeamDirection.RIGHT: list(zip(range(nrow), repeat(-1))),
        BeamDirection.LEFT: list(zip(range(nrow), repeat(ncol))),
        BeamDirection.UP: list(zip(repeat(nrow), range(ncol))),
        BeamDirection.DOWN: list(zip(repeat(-1), range(ncol)))
    }
    # print(start_points)
    # exit()
    # print(contraption)
    max_fields = []
    for direction, starts in start_points.items():
        for start in starts:
            energized_fields = start_follow_beam(contraption, start, direction)
            print(f"energized: {sorted(energized_fields)}")
            max_fields.append(len(energized_fields))
    print(max(max_fields))

    # energy_map = contraption.copy()
    # for ef in energized_fields.keys():
    #     energy_map[ef[0]][ef[1]] = "#"

    # for line in energy_map:
    #     print("".join(line))

    # print(f"Total energies after: {len(energized_fields.keys())}")
