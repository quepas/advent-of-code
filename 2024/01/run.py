from common.functional import compose


def parse_line(line: str) -> tuple[int, ...]:
    return tuple(map(int, line.split()))


with open("2024/01/input", "r") as f:
    left_column, right_column = [], []
    for l, r in map(parse_line, f.readlines()):
        left_column.append(l)
        right_column.append(r)

    left_column = sorted(left_column)
    right_column = sorted(right_column)

    # --- Part 1 ---
    total_distance = sum(
        map(compose(lambda x: x[0] - x[1], abs), zip(left_column, right_column))
    )
    print(f"Total distance (part 1): {total_distance}")

    # --- Part 2 ---
    similarity_score = sum(map(lambda l: l * right_column.count(l), left_column))
    print(f"Similarity score (part 2): {similarity_score}")
