from functools import reduce
from math import ceil, sqrt, floor
from operator import mul

Race = tuple[int, int]


def parse_race_data(rows: list[str]) -> tuple[list[Race], Race]:
    """
    Parse race data as: 1) a collection of smaller sub-races, and 2) as one big race (no whitespaces!)
    """
    time_str = rows[0].split()[1:]
    time = list(map(int, time_str))
    record_distance_str = rows[1].split()[1:]
    record_distance = list(map(int, record_distance_str))
    big_race_time = int("".join(time_str))
    big_race_record_distance = int("".join(record_distance_str))
    return list(zip(time, record_distance)), (big_race_time, big_race_record_distance)


def find_winning_race_plans(race: Race) -> int:
    """
    Find how many race strategies are winning.
    It is enough to solve a quadratic inequality: -push_time^2 + time * push_time - record_distance > 0
    Where time and record_distance are given, and we solve for push_time. Then, we take the points of intersection
    with 0, and find the whole integers around. Once we have it, we can count up the number of integer solutions.
    """
    time, record_distance = race
    # +/- 1 is necessary, because we are interested in only distances bigger than the current records (>)
    lower = floor(
        (-time + sqrt(time * time - 4 * record_distance)) / -2) + 1
    upper = ceil(
        (-time - sqrt(time * time - 4 * record_distance)) / -2) - 1
    return upper - lower + 1


with open("input") as f:
    small_races, big_race = parse_race_data(f.readlines())
    print("----- Part one -----")
    num_winning_strategies = reduce(mul, map(find_winning_race_plans, small_races), 1)
    print(f"Number of winning strategies multiplied: {num_winning_strategies}")
    print("----- Part two -----")
    num_winning_strategies = find_winning_race_plans(big_race)
    print(f"Number of winning strategies for the big race: {num_winning_strategies}")
