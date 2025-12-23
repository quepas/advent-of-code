import os
from pathlib import Path


def find_max_joltage(bank: str, digits: int = 2) -> int:
    """
    Traverse a subset of a bank of batteries, choosing at each step the largest
    battery possible. So that, when juxtaposed side by side, the batteries give
    the maximal joltage.
    """
    left_index = 0  # inclusive
    num = 0
    for i in range(digits, 0, -1):
        # Our next maximal battery cannot exceed the index of batteries that
        # need to be included anyway to fullfil the `digits` number
        right_index = len(bank) - i + 1  # exclusive
        # Look for the next maximal battery in a bank subset
        sub_bank = bank[left_index:right_index]
        # Find max battery
        max_battery = max(sub_bank)
        # Modify the left index of the bank subset
        left_index += sub_bank.index(max_battery) + 1
        # Convert current max battery to a number!
        num += int(max_battery) * (10 ** (i - 1))
    return num


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
with open(dir_path / "input") as f:
    joltages = list(map(str.strip, f.readlines()))
    # --- Part 1: find the largest joltage by chosing exactly two batteries
    result = sum(map(lambda x: find_max_joltage(x, digits=2), joltages))
    print(f"Part 1: total output joltage = {result} (should be 17408)")
    # --- Part 2: find the largest joltage by chosing exactly twelve batteries
    result = sum(map(lambda x: find_max_joltage(x, digits=12), joltages))
    print(f"Part 2: total output joltage = {result} (should be 172740584266849)")
