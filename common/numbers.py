from itertools import pairwise


def in_range(
    x, a, b, left_inclusive: bool = False, right_inclusive: bool = False
) -> bool:
    """Check if x is in range between a and b (left-right inclusive or not!)"""
    if left_inclusive and right_inclusive:
        return a <= x <= b
    elif left_inclusive:
        return a <= x < b
    else:  # right_inclusive:
        return a < x <= b


def difference(elements: list) -> list:
    return [y - x for x, y in pairwise(elements)]
