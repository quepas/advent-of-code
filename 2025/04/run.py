import os
from pathlib import Path
from itertools import product

def count_neighbour_paper_rolls(paper_map: list[list[str]], position: tuple[int, int]) -> int:
    nrow, ncol = len(paper_map), len(paper_map[0])
    # Clockwise
    offsets = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    count = 0
    for offset in offsets:
        x, y = position[0] + offset[0], position[1] + offset[1]
        if x < 0 or x >= ncol or y < 0 or y >= nrow:
            continue
        if paper_map[x][y] == "@":
            count += 1
    return count


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
with open(dir_path / "input") as f:
    paper_map = list(map(lambda x: list(x.strip()), f.readlines()))
    nrow, ncol = len(paper_map), len(paper_map[0])
    count = 0
    for x, y in product(range(nrow), range(ncol)):
        if paper_map[x][y] == "@" and count_neighbour_paper_rolls(paper_map, (x, y)) < 4:
            count += 1
    print(f"Part 1: number of accessible by forklift paper rolls = {count}")
    count = 0
    new_moves = True
    while new_moves:
        new_moves = False
        for x, y in product(range(nrow), range(ncol)):
            if paper_map[x][y] == "@" and count_neighbour_paper_rolls(paper_map, (x, y)) < 4:
                count += 1
                new_moves = True
                paper_map[x][y] = "."
    print(f"Part 2: number of disposable paper rolls = {count}")
