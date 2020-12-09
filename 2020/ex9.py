from typing import List, Tuple


def find_end_XMAS(numbers: List[int], preamble_size: int) -> Tuple[int, int]:
    start_idx = preamble_size
    while start_idx < len(numbers):
        if not has_sum_pair(numbers[start_idx - preamble_size:start_idx], numbers[start_idx]):
            return numbers[start_idx], start_idx
        start_idx += 1


def has_sum_pair(numbers: List[int], number: int) -> bool:
    for k in range(len(numbers) - 1):
        for l in range(k, len(numbers)):
            if numbers[k] + numbers[l] == number:
                return True
    return False


def find_contiguous_range(numbers: List[int], number: int) -> List[int]:
    for k in range(len(numbers) - 1):
        for l in range(k, len(numbers)):
            sum_number = sum(numbers[k:l])
            if sum_number == number:
                return numbers[k:l]


preamble_size = 25
with open('input_9.txt', 'r') as f:
    numbers = list(map(lambda x: int(x.strip()), f.readlines()))
    invalid_number, invalid_index = find_end_XMAS(numbers, preamble_size)
    print("First invalid number in XMAS is = {}".format(invalid_number))

    invalid_range = find_contiguous_range(numbers[0:invalid_index], invalid_number)
    min_invalid_range = min(invalid_range)
    max_invalid_range = max(invalid_range)
    print("Invalid range [min: {}, max: {}], sum = {}".format(min_invalid_range, max_invalid_range, min_invalid_range + max_invalid_range))
