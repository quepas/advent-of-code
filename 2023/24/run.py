from dataclasses import dataclass
from itertools import combinations
from typing import Optional

Vector = tuple[int, int, int]
LinearEq = tuple[float, float]


@dataclass
class Hailstone:
    position: Vector
    velocity: Vector

    def as_linear_equation(self) -> LinearEq:
        px, py, _ = self.position
        vx, vy, _ = self.velocity
        x1, y1 = px, py
        x2, y2 = px + vx, py + vy
        slope = (y2 - y1) / (x2 - x1)
        b = slope * (-x1) + y1
        return slope, b

    def intersection(self, other: 'Hailstone') -> Optional[tuple[float, float]]:
        a, c = self.as_linear_equation()
        b, d = other.as_linear_equation()
        if a == b:
            return None
        px = (d - c) / (a - b)
        py = (a * (d - c)) / (a - b) + c
        return px, py

    def point_in_future(self, P: tuple[float, float]) -> bool:
        step_x = self.position[0] + self.velocity[0]
        step_y = self.position[1] + self.velocity[1]
        # If the first step brings us closer in each dimension to a given intersection point
        return abs(P[0] - self.position[0]) > abs(step_x - P[0]) \
            and abs(P[1] - self.position[1]) > abs(step_y - P[1])


def parse_hailstone(text: str) -> Hailstone:
    pos, vel = text.strip().split(" @ ")
    return Hailstone(
        position=list(map(int, pos.split(","))),
        velocity=list(map(int, vel.split(","))))


with open("input") as f:
    hailstones = list(map(parse_hailstone, f.readlines()))
    print(hailstones)
    # input_test_1
    # axis_min, axis_max = 7, 27
    axis_min, axis_max = 200000000000000, 400000000000000

    count = 0
    for h1, h2 in combinations(hailstones, r=2):
        P = h1.intersection(h2)
        if P is not None and axis_min <= P[0] <= axis_max and axis_min <= P[1] <= axis_max \
                and h1.point_in_future(P) and h2.point_in_future(P):
            print(f"\t* {h1} vs {h2}: intersection: {P}")
            count += 1
    print("Intersection count:", count)
