from operator import add
Pattern = list[int]


def count_in_column(rows: list[str], column: int, char: str = "#") -> int:
    return sum(map(lambda row: row[column] == char, rows))


def parse_schematics(content: str) -> tuple[list[Pattern], list[Pattern]]:
    schematics = content.split("\n\n")
    locks = []
    keys = []
    for scheme in schematics:
        lines = scheme.strip().split("\n")
        pattern = list(map(lambda column: count_in_column(lines, column) - 1, range(5)))
        # Check if pattern represents a lock or a key
        if lines[0] == "#" * 5:
            locks.append(pattern)
        else:
            keys.append(pattern)
    return locks, keys

def overlap(lock: Pattern, key: Pattern, overlap_threshold: int = 6) -> bool:
    return max(map(lambda x: x[0] + x[1], zip(lock, key))) >= overlap_threshold


with open("input", "r") as f:
    locks, keys = parse_schematics(f.read())

    from itertools import pairwise, product
    
    num_no_overlap = 0
    for l, k in product(locks, keys):
        does_overlap = overlap(l, k)
        print(l, k, does_overlap)
        num_no_overlap += not does_overlap
    print("Num. no overlap:", num_no_overlap)
