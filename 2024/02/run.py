from common.numbers import difference
from common.parsing import parse_line_of_ints


def check_safe(levels: list[int]) -> bool:
    """
    Check if level differences are all increasing or all decreasing
    and in a specific range!
    """
    levels_diff = difference(levels)
    return all(map(lambda e: 0 < e <= 3, levels_diff)) or all(
        map(lambda e: -3 <= e < 0, levels_diff)
    )


def can_be_fixed(levels: list[int]) -> bool:
    """Fix by finding Problem Dampener: one wrong number which can fix the whole sequence!"""
    for i in range(len(levels)):
        # Holdout one number and then try testing !
        new_row = levels[:i] + levels[i + 1 :]
        if check_safe(new_row):
            return True
    return False


with open("2024/02/input", "r") as f:
    lines = f.readlines()
    num_safe, num_fixed = 0, 0
    for line in lines:
        levels = parse_line_of_ints(line)
        # Part 1: count immediately safe reports
        if check_safe(levels):
            num_safe += 1
        # Part 2: count reports which could be fixed
        elif can_be_fixed(levels):
            num_fixed += 1

    print(f"Num. of safe reports (part 1): {num_safe}")
    print(f"Num. of safe and fixed reports (part 2): {num_safe + num_fixed}")
