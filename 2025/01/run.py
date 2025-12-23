import os
from math import floor
from pathlib import Path


def convert_rotation(instruction) -> int:
    direction = 1 if instruction[0] == "R" else -1
    distance = int(instruction[1:])
    return direction * distance


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
with open(dir_path / "input") as f:
    instructions = [convert_rotation(inst.strip()) for inst in f.readlines()]
    current = 50
    count_zero_part1 = 0
    count_zero_part2 = 0
    # Each instruction contains an offset
    for offset in instructions:
        # --- This is part 2: We care about landing and crossing 0!
        # We compute a raw current position before applying modulo arithmetic
        raw_current = current + offset
        # If L move that touched or crossed 0
        if raw_current <= 0:
            # If we weren't already at 0, count that 0!
            if current != 0:
                count_zero_part2 += 1
            # Check the rest of the raw position and find out how many 100s is in there!
            count_zero_part2 += floor(abs(raw_current) / 100)
        # Otherwise it was R move with a straightforward formula
        else:
            count_zero_part2 += floor((offset + current) / 100)
        # --- This is part 1: We don't care about crossing 0, we only care if we land at 0
        # Apply modulo arithmetic for part 1 and 2
        current = raw_current % 100
        count_zero_part1 += 1 if current == 0 else 0

    print(f"Part 1: Count zeros={count_zero_part1}")
    print(f"Part 2: Count zeros={count_zero_part2}")
