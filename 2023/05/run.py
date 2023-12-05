from functools import partial

Interval = tuple[int, int]
Mapping = tuple[int, int, int]


def parse_almanac(text: str) -> dict:
    """
    Parse almanac consisting of seeds and maps (collections of linear mappings).
    Warning: we are using the guaranteed behaviour of CPython 3.6 and later Python 3.7 specification
             requiring the key insertion order in dictionaries to be maintained. Otherwise, we can use
             additional list of map order (as read from the almanac).
    URL: https://stackoverflow.com/a/47849121/1319478
    """
    sections = text.split("\n\n")
    almanac = {
        "seeds": list(map(int, sections[0][7:].split())),
        "maps": []
    }
    # All subsequent sections are mappings (in a correct sequence)
    for section in sections[1:]:
        chunks = section.split("\n")

        def split_to_int(line) -> list[int]:
            return list(map(int, line.split()))

        almanac["maps"].append(list(map(split_to_int, chunks[1:])))
    return almanac


def find_lowest_location(interval: Interval, almanac: dict) -> int:
    """
    Apply subsequent maps to the input interval and find the lowest location in the set of obtained sub-intervals
    (the lowest location is one of the starting points of a sub-interval).
    """
    # During the application of mapping, a single interval might be split into two or three intervals
    # Hence, we start with single interval in a list
    intervals = [interval]
    for map in almanac["maps"]:
        processed_intervals = []
        for interval in intervals:
            # In each map, find the first mapping that applies to the interval, otherwise another mapping
            # from the same map might be applicable to the already processed interval.
            for mapping in map:
                applied, transformed_interval = apply_mapping(interval, mapping)
                # Warning: In general, this is a drawback of this simplistic approach, as in a single map there might be
                # two disjoint mappings that still apply to the same single interval. This code will miss such cases.
                if applied:
                    break
            processed_intervals.extend(transformed_interval)
        intervals = processed_intervals
    # min() is well-defined on ordered lists/tuples
    return min(min(intervals))


def apply_mapping(interval: Interval, mapping: Mapping) -> tuple[bool, list[Interval]]:
    """
    Apply a single mapping (linear transformation) to the whole or a part of an interval.
    First, figure out which part of an interval is affected by the mapping.
    For a single interval, this results in one of three cases:
    1. Mapping doesn't apply to the interval (its domain is out of the interval scope).
       This returns the original interval unchanged, but a list of one element.
    2. Mapping applies to the whole interval.
       This just adds the offset produced by the mapping to start-end points of the interval. Returns interval as a list.
    3. Mapping is partially applied to an interval.
       This requires dividing the initial interval into two (when mapping covers only the left or the right side)
       or three sub-intervals (when mapping applies to the inside of the interval, with gaps on both sides).
       Once the division is made, we apply offsets produced by the mapping to the concerned sub-intervals.
    """
    domain_start, domain_end = mapping[1], mapping[1] + mapping[2] - 1
    interval_start, interval_end = interval
    assert domain_start <= domain_end, "Invalid domain: start bigger than end"
    assert interval_start <= interval_end, "Invalid interval: start bigger than end"
    offset = mapping[0] - mapping[1]
    # 0. Mapping is not applicable to the interval
    if domain_end < interval_start or domain_start > interval_end:
        return False, [interval]
    # 1. Easy case: mapping applicable to the whole interval
    elif domain_start <= interval_start and interval_end <= domain_end:
        return True, [(interval_start + offset, interval_end + offset)]
    # 2A. Semi-easy case: mapping covers left part of the interval
    elif domain_start <= interval_start and domain_end < interval_end:
        return True, [(interval_start + offset, domain_end + offset), (domain_end + 1, interval_end)]
    # 2B. Semi-easy case: mapping covers right part of the interval
    elif interval_start < domain_start and interval_end <= domain_end:
        return True, [(interval_start, domain_start - 1), (domain_start + offset, interval_end + offset)]
    # 3. Mapping is entirely inside the interval
    elif interval_start < domain_start <= domain_end < interval_end:
        return True, [(interval_start, domain_start - 1), (domain_start + offset, domain_end + offset),
                      (domain_end + 1, interval_end)]
    assert False, "This should never happened! If it does, the mapping-to-interval matching is incorrect."


with open("input", "r") as f:
    almanac = parse_almanac(f.read().strip())
    seeds = almanac["seeds"]
    print("----- Part one -----")
    lowest_location = min(
        map(partial(find_lowest_location, almanac=almanac),
            # Use intervals of size 1, like (a, a)
            map(lambda seed: (seed, seed),
                seeds)))
    print(f"Lowest location number: {lowest_location}")
    print("----- Part two -----")
    lowest_location = min(
        map(partial(find_lowest_location, almanac=almanac),
            # -1 because seeds[idx+1] counts the number of seeds in an interval including the starting seeds[idx]
            map(lambda idx: (seeds[idx], seeds[idx] + seeds[idx + 1] - 1),
                range(0, len(seeds), 2))))
    print(f"Lowest location number: {lowest_location}")
