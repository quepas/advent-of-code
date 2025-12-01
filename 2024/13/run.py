import re
from dataclasses import dataclass
from functools import partial

Displacement = tuple[int, int]


@dataclass
class Machine:
    a: Displacement
    b: Displacement
    prize: Displacement


def parse_machine(machine_str: str, offset: int = 0) -> Machine:
    lines = machine_str.split("\n")
    print(lines)
    assert len(lines) == 3
    m1 = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
    a = int(m1.group(1)), int(m1.group(2))
    m2 = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
    b = int(m2.group(1)), int(m2.group(2))
    m3 = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[2])
    prize = int(m3.group(1)) + offset, int(m3.group(2)) + offset
    return Machine(a, b, prize)


def play_machine(machine: Machine) -> int | None:
    # Cramer's rule (URL: https://en.wikipedia.org/wiki/Cramer%27s_rule)
    a1, a2 = machine.a
    b1, b2 = machine.b
    c1, c2 = machine.prize
    x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
    if x.is_integer() and y.is_integer():
        return int(x) * 3 + int(y) * 1
    return None


with open("input", "r") as f:
    # Part 1: offset = 0
    # Part 2
    offset = 10000000000000
    machines = list(
        map(
            partial(parse_machine, offset=offset),
            map(str.strip, f.read().split("\n\n")),
        )
    )
    sum_tokens = 0
    for machine in machines:
        if tokens := play_machine(machine):
            print("Possible win!", machine)
            sum_tokens += tokens
    print("Total number of tokens: ", sum_tokens)
