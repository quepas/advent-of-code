from functools import partial, cache
from multiprocessing import Pool
from pathlib import Path
from time import time


def parse_record(text_record: str, multiply_factor: int = 1) -> tuple[str, tuple[int, ...]]:
    conditions, control = text_record.split()
    control = list(map(int, control.split(",")))
    conditions = "?".join([conditions] * multiply_factor)
    control = [*control] * multiply_factor
    return conditions, tuple(control)


@cache
def count_spring_groups(record, counts, explored_group_size=0) -> int:
    """
    In this function we don't recreate all possible arrangement of damaged spring groups
    instead, we count them. The difference is that, it is easier to cache some of the recursive calls.
    Otherwise, if we run it without cache'ing it would take similar time to our backtracing approach (I think).
    """
    # Analyse existing symbols and ongoing groups of damaged springs
    match (len(record), len(counts), explored_group_size):
        # Check if the record ends correctly without any present spring groups
        case (0, 0, 0):
            return 1
        # Check if the current spring group finishes correctly with the last symbol
        case (0, 1, group_size) if group_size == counts[0]:
            return 1
        # Otherwise, any ongoing spring group is invalid (it can't end correctly, we run out of symbols!)
        case (0, _, _):
            return 0
    count = 0
    symbols = ["#", "."] if record[0] == "?" else record[0]
    # Start (in_group_count == 0) or continue (in_group_count > 0) exploring a damaged spring group (#+)
    # In either case, we increase the size of the explored group
    if "#" in symbols:
        count += count_spring_groups(record[1:], counts, explored_group_size + 1)
    # Continue past a good spring (.)
    if "." in symbols and explored_group_size == 0:
        count += count_spring_groups(record[1:], counts)
    # Finish exploring a damaged spring group (#+); ready for the next group counting !
    if "." in symbols and counts and counts[0] == explored_group_size:
        count += count_spring_groups(record[1:], counts[1:])
    return count


def run_test(path: Path, mul_factor: int = 1):
    t0 = time()
    with open(path) as f:
        lines = f.readlines()
        records = list(map(partial(parse_record, multiply_factor=mul_factor), lines))
        with Pool() as p:
            total_arrangements = sum(p.starmap(count_spring_groups, records))
    print(f"Arrangements: {total_arrangements}")
    t1 = time()
    print(f"Took time: {t1 - t0}s")
    return total_arrangements


print("----- Part one -----")
run_test("input", 1)
print("----- Part two -----")
run_test("input", 5)
