from collections import deque
from functools import partial
from itertools import pairwise, accumulate

History = list[int]


def parse_histories(lines: list[str]) -> list[History]:
    """Parse histories from strings"""
    return list(map(lambda numbers: list(map(int, numbers)), map(str.split, lines)))


def diff(numbers: list[int]) -> list[int]:
    """Compute difference between pairs of numbers from a list"""
    return list(map(lambda t: t[1] - t[0], pairwise(numbers)))


def extrapolate_history(history: History, backward: bool = False) -> int:
    """
    Extrapolate history by computing diffs of numbers until a diff is all zeros.
    Then, use edge values to compute the extrapolated history value (backward or forward).
    """
    selection_idx = 0 if backward else -1
    # We need the full diff values for the next iteration, but we can keep only the edge value!
    current_diffs = history
    # Collect edge values from the right (forward extrapolation) or from the left (backward extrapolation)
    edge_values = deque([current_diffs[selection_idx]])
    # Until all diffs are 0...
    while any(current_diffs):
        current_diffs = diff(current_diffs)
        # Keep edge values in reversed order, as we later use them starting from the bottom
        edge_values.appendleft(current_diffs[selection_idx])
    # Forward extrapolation is just a cumulative-sum of edge values from the right side
    if not backward:
        # Next history value is the last element of cumsum!
        return list(accumulate(edge_values))[-1]
    # Backward extrapolation is a bit more trickier than forward!
    next_history_value = edge_values[1]  # Skip the first 0
    for i in range(2, len(edge_values)):
        # Next backward history value is a value needed to obtain the current history edge value
        next_history_value = edge_values[i] - next_history_value
    return next_history_value


with open("input") as f:
    histories = parse_histories(f.readlines())
    print("----- Part one -----")
    summed_extrapolated_histories = sum(map(extrapolate_history, histories))
    print(f"Summed forward extrapolated histories: {summed_extrapolated_histories}")
    print("----- Part one -----")
    summed_extrapolated_histories = sum(map(partial(extrapolate_history, backward=True), histories))
    print(f"Summed backward extrapolated histories: {summed_extrapolated_histories} (should be 1019)")
