from typing import List, Tuple


def move_by(map_grid: List[str], step_column: int, step_row: int) -> Tuple[int, int]:
    map_with_moves = map_grid.copy()
    start_column = -step_column
    trees = 0
    total_moves = 0
    for k in range(0, len(map_grid), step_row):
        line = map_grid[k].strip()
        start_column = (start_column + step_column) % len(line)
        if line[start_column] == '#':
            trees += 1
            map_with_moves[k] = replace_chr(line, start_column, 'X')
        else:
            map_with_moves[k] = replace_chr(line, start_column, 'O')
        total_moves += 1
    save_map(map_with_moves, "ex3_output/output_{}_{}.txt".format(step_column, step_row))
    return trees, total_moves


def replace_chr(line: str, position: int, char: chr) -> str:
    return line[:position] + char + line[position + 1:]


def save_map(map_grid: List[str], filename: str) -> None:
    with open(filename, "w") as f:
        for line in map_grid:
            f.write(line.strip() + "\n")
        f.close()


moves_to_check = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
encountered_trees = 1

with open("input_3.txt", "r") as f:
    map_data = f.readlines()
    for move_column, move_row in moves_to_check:
        num_trees, all_moves = move_by(map_data, move_column, move_row)
        print("Steps when moving {} x {} = {}/{}".format(move_column, move_row, num_trees, all_moves))
        encountered_trees *= num_trees

print("In total, we have encountered trees time = {}".format(encountered_trees))
