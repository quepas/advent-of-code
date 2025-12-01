from time import time_ns
from functools import partial, cache
from multiprocessing.pool import ThreadPool as Pool

# from multiprocessing import Pool
from itertools import repeat 

PrefixMap = dict[int, list[str]]

@cache
def check_design(design: str, towels: list[str]) -> bool:
    if not design:
        return True
    for towel in towels:
        if design.startswith(towel):
            if check_design(design[len(towel):], towels):
                return True
    return False

def match_prefix_map(design: str, prefix_map: PrefixMap, index: int = 0) -> bool:
    print(f"Testing: {design}, index: {index}")
    if index == len(design):
        return True
    for prefix in prefix_map.get(index, []):
        if design[index:].startswith(prefix):
            if match_prefix_map(design, prefix_map, index + len(prefix)):
                return True
    return False

def prepare_prefix_map(design: str, towels: list[str]) -> PrefixMap:
    towels = sorted(towels)
    prefix_map = {}
    next_i = 0
    for i in range(len(design)):
        if i < next_i:
            continue
        for towel in towels:
            if design[i:].startswith(towel):
                if i in prefix_map:
                    prefix_map[i].append(towel)
                else:
                    prefix_map[i] = [towel]
        if i in prefix_map:
            min_prefix = min(map(len, prefix_map[i]))
            next_i += min_prefix


    return prefix_map


def test_design(design: str, towels: list[str]) -> int:
    @cache
    def check_design2(design: str) -> bool:
        if not design:
            return True
        for towel in towels:
            if design.startswith(towel):
                if check_design2(design[len(towel):]):
                    return True
        return False
    @cache
    def check_design3(design: str) -> int:
        if not design:
            return 1
        nums = 0
        for towel in towels:
            if design.startswith(towel):
                nums += check_design3(design[len(towel):])
        return nums
    t0 = time_ns()
    # prefix_map = prepare_prefix_map(design, towels)
    # available = check_design2(design)
    available = check_design3(design)
    # print(prefix_map)
    # available = match_prefix_map(design, prefix_map)
    t1 = time_ns()
    print(f"Testing design: {design}; available: {available}; took: {(t1 - t0) / 1e6}ms")
    return available



with open("input", "r") as f:
    lines = f.readlines()

    towels = lines[0].strip().split(", ")
    longest_towel = max(map(len, towels))
    print("Available towels:", towels)
    print("Longest towel:", longest_towel)
    designs = list(map(str.strip, lines[2:]))
    print("Required designs:", designs)
   
    possible_designs = 0
    for design in designs:
        if num := test_design(design, towels):
            possible_designs += num

    print("Possible designs: ", possible_designs)
