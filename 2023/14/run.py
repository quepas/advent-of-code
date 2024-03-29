class Move:
    UNKNOWN = 0
    UP = 1
    LEFT = 2
    DOWN = 4
    RIGHT = 8
    STUCK = 16

    @staticmethod
    def can_fall(flag: int, direction) -> bool:
        return bool(flag & direction)


# Given a grid with (0, 0) coordinates in the top-left corner,
# connect moves with their corresponding displacement vectors
MoveVector = {
    Move.LEFT: (0, -1),
    Move.RIGHT: (0, 1),
    Move.UP: (-1, 0),
    Move.DOWN: (1, 0)
}


class MirrorPlatform:

    def __init__(self):
        self.rocks = []

    def move_rocks(self, direction: Move):
        pass


def create_empty_move_field(platform: list[list[str]]) -> list[list[int]]:
    move_field = []
    for line in platform:
        move_field.append(list(map(lambda x: Move.STUCK if x == "#" else Move.UNKNOWN, line)))
    # Start from the top to propagate the UP move
    nrow, ncol = len(platform), len(platform[0])
    for row in range(nrow):
        for col in range(ncol):
            if platform[row][col] == "#":
                continue
            # Check left
            if col == 0 or platform[row][col - 1] != "#":
                move_field[row][col] |= Move.LEFT
            # Check right
            if col == ncol - 1 or platform[row][col + 1] != "#":
                move_field[row][col] |= Move.RIGHT
            # Check up
            if row == 0 or platform[row - 1][col] != "#":
                move_field[row][col] |= Move.UP
            # Check down
            if row == nrow - 1 or platform[row + 1][col] != "#":
                move_field[row][col] |= Move.DOWN
    # print(move_field)
    return move_field


def outside_of_platform(position, nrow, ncol) -> bool:
    row, col = position
    return row < 0 or row >= nrow or col < 0 or col >= ncol


def move_rocks(rocks, move_field: list[list[int]], move: Move, nrow, ncol):
    vec = MoveVector[move]
    moved_rocks = []
    in_reverse = move in [Move.DOWN, Move.RIGHT]
    # We need to apply moves to sorted rocks
    for current in sorted(rocks, reverse=in_reverse):
        while move_field[current[0]][current[1]] & int(move):
            test_current = (current[0] + vec[0], current[1] + vec[1])
            if test_current in moved_rocks or outside_of_platform(test_current, nrow, ncol):
                break
            current = test_current
        moved_rocks.append(current)

    return sorted(moved_rocks)


def read_platform(lines: list[str]) -> list[list[str]]:
    platform = []
    rocks = []
    row = 0
    for line in lines:
        platform.append([c for c in line.strip()])
        rocks.extend(list(map(lambda x: (row, x), [i for i, c in enumerate(line.strip()) if c == "O"])))
        row += 1
    return platform, rocks


def compute_total_load(rocks, nrow) -> int:
    return sum(map(lambda t: nrow - t[0], rocks))


with open("input") as f:
    platform, rocks = read_platform(f.readlines())
    nrow, ncol = len(platform), len(platform[0])
    move_field = create_empty_move_field(platform)
    unique_rocks = list()
    max_cycles = 1000000000
    # In the Part Two, instead of iterating up to max_cyles, we make an assumption that the movement of rocks
    # follows a cycle, all we need to do is to find such a cycle and extrapolate the result for the max_cycles value
    for i in range(1, max_cycles):
        rocks = move_rocks(rocks, move_field, Move.UP, nrow, ncol)
        rocks = move_rocks(rocks, move_field, Move.LEFT, nrow, ncol)
        rocks = move_rocks(rocks, move_field, Move.DOWN, nrow, ncol)
        rocks = move_rocks(rocks, move_field, Move.RIGHT, nrow, ncol)
        print(f"#{i} Computed: {compute_total_load(rocks, nrow)}")
        if rocks in unique_rocks:
            mini_cycle_start = unique_rocks.index(rocks) + 1
            mini_cycle_end = i
            mini_cycle_length = mini_cycle_end - mini_cycle_start
            print(
                f"Already there after {i} cycles, mini-cycle-start={mini_cycle_start}, mini-cycle-end={mini_cycle_end}; length={mini_cycle_length}; {compute_total_load(rocks, nrow)}")
            print(
                f"Found: {compute_total_load(unique_rocks[mini_cycle_start + ((max_cycles - mini_cycle_start) % mini_cycle_length) - 1], nrow)}")
            break
        unique_rocks.append(rocks)
