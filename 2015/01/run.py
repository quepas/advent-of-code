from itertools import accumulate


def count_floors_scan(line: str) -> tuple[int, int]:
    """Straight forward scan-line approach"""
    basement_entry = len(line)
    end_floor = 0
    for i in range(len(line)):
        end_floor += 1 if line[i] == "(" else -1
        if end_floor == -1:
            basement_entry = min(basement_entry, i + 1)
    return end_floor, basement_entry


def count_floors(line: str) -> tuple[int, int]:
    """A more functional-like approach with cumsum"""
    directions = map(lambda direction: 1 if direction == "(" else -1, line)
    cumulative_sum = list(accumulate(directions))
    return cumulative_sum[-1], cumulative_sum.index(-1) + 1


with open("input") as f:
    line = f.read()
    end_floor, first_basement_entry = count_floors_scan(line)
    print("----- Part one -----")
    print(f"The Santa ends on the {end_floor} floor")
    print("----- Part two -----")
    print(f"The Santa steps into the basement on {first_basement_entry}-th floor change")
