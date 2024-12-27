from common.numbers import difference
from common.parsing import parse_line_of_ints


def check_safe(elements: list[int]) -> bool:
    num_diff = difference(elements)
    return all(map(lambda e: 0 < e <= 3, num_diff)) or all(
        map(lambda e: -3 <= e < 0, num_diff)
    )


with open("2024/02/input", "r") as f:
    lines = f.readlines()
    num_safe, num_fixed = 0, 0
    for line in lines:
        row = parse_line_of_ints(line)
        # Part 1
        if check_safe(row):
            num_safe += 1
        # Part 2
        else:
            # Find Problem Dampener
            for i in range(len(row)):
                # Holdout one number and then try testing !
                new_row = row[:i] + row[i + 1 :]
                if check_safe(new_row):
                    num_fixed += 1
                    break

    print(f"Num safe (part 1)={num_safe}")
    print(f"Num safe (part 2)={num_safe + num_fixed}")
