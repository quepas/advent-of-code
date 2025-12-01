from itertools import cycle
import sys

sys.setrecursionlimit(2000)
Position = tuple[int, int]

MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIRECTION = {"up": (-1, 0), "right": (0, 1), "down": (1, 0), "left": (0, -1)}
NUM_ROTATIONS = {
    ("up", "down"): 2,
    ("left", "right"): 2,
    ("up", "right"): 1,
    ("right", "down"): 1,
    ("down", "left"): 1,
    ("left", "up"): 1,
}


def num_rotations(start_direction: str, end_direction: str) -> int:
    if start_direction == end_direction:
        return 0
    if (start_direction, end_direction) in NUM_ROTATIONS:
        return NUM_ROTATIONS[(start_direction, end_direction)]
    else:
        return NUM_ROTATIONS[(end_direction, start_direction)]


with open("input", "r") as f:
    # Load map
    lines = list(map(str.strip, f.readlines()))
    start, end = None, None
    # Find start
    for row, line in enumerate(lines):
        if "S" in line:
            start = (row, line.index("S"))
        if "E" in line:
            end = (row, line.index("E"))
    print(start, end)

    def get_tile(position: Position) -> str:
        row, col = position
        return lines[row][col]

    def add(a: Position, b: Position) -> Position:
        return a[0] + b[0], a[1] + b[1]

    def get_next_moves(position: Position) -> list[Position]:
        return list(
            filter(
                lambda x: get_tile(x) == ".",
                map(lambda pos: (pos[0] + position[0], pos[1] + position[1]), MOVES),
            )
        )

    def print_map(visited: list[Position]) -> None:
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if (row, col) in visited:
                    print("X", end="")
                else:
                    print(char, end="")
            print("")

    all_costs = []
    min_cost =  {}
    best_nodes = []
    # best_path = 7036
    # best_path = 11048
    best_path = 143580
 
    def solve_maze(position: Position, visited: list[Position], direction: str ="right", cost: int = 0) ->  None:
        if cost > best_path:
            return
        if position not in min_cost:
            min_cost[position] = cost
        else:
            if cost > 2000 + min_cost[position]:
                return
            min_cost[position] = min(min_cost[position], cost)
        # print("Position: ", position)
        # print_map(visited)
        # input()
        if position == end:
            print("Position: ", position, "; visited=", visited, "; cost=", cost)
            all_costs.append(cost)
            if cost == best_path:
                best_nodes.extend(visited)
            return

        move_up = add(position, DIRECTION["up"])
        if get_tile(move_up) in [".", "E"] and move_up not in visited:
            new_cost = num_rotations(direction, "up") * 1000 + 1
            # new_cost = new_cost if new_cost > 0 else 1
            solve_maze(move_up, [*visited, move_up], "up", cost + new_cost)
        move_right = add(position, DIRECTION["right"])
        if get_tile(move_right) in [".", "E"] and move_right not in visited:
            new_cost = num_rotations(direction, "right") * 1000 + 1
            # new_cost = new_cost if new_cost > 0 else 1
            solve_maze(move_right, [*visited, move_right], "right", cost + new_cost)
        move_down = add(position, DIRECTION["down"])
        if get_tile(move_down) in [".", "E"] and move_down not in visited:
            new_cost = num_rotations(direction, "down") * 1000 + 1
            # new_cost = new_cost if new_cost > 0 else 1
            solve_maze(move_down, [*visited, move_down], "down", cost + new_cost)
        move_left = add(position, DIRECTION["left"])
        if get_tile(move_left) in [".", "E"] and move_left not in visited:
            new_cost = num_rotations(direction, "left") * 1000 + 1
            # new_cost = new_cost if new_cost > 0 else 1
            solve_maze(move_left, [*visited, move_left], "left", cost + new_cost)

    solve_maze(start, [])
    print("All paths cost: ", all_costs)
    print("Min path cost: ", min(all_costs))
    # print(min_cost)
    # 637 too low
    print("Best tiles:", len(set(best_nodes)) + 1)

    # print_map(best_nodes)
