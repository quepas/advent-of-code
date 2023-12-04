from collections import deque
from time import time


def parse_scratchcard(line: str) -> tuple[int, set[int]]:
    chunks = line.split()
    card_number = int(chunks[1][:-1])
    split = chunks.index("|")
    winning_numbers = set(map(int, chunks[2:split]))
    scratched_numbers = set(map(int, chunks[split + 1:]))
    return card_number, winning_numbers & scratched_numbers


def scratched_numbers_to_points(winning_scratched_numbers: set[int]) -> int:
    """
    Compute number of points given a list of winning-scratched numbers
    """
    return 2 ** (len(winning_scratched_numbers) - 1) if len(winning_scratched_numbers) else 0


with open("input") as f:
    scratchcards = list(map(parse_scratchcard, f.readlines()))
    print("----- Part one -----")
    total_points = sum(map(scratched_numbers_to_points,
                           map(lambda scratchcard: scratchcard[1],
                               scratchcards)))
    print(f"Total points of scratchcards: {total_points}")
    print("----- Part two -----")
    # Start from 0, the index of the first scratchcard in the list
    to_process = deque(range(0, len(scratchcards)))
    total_num_scratchcards = 0
    t0 = time()
    while len(to_process):
        card_number, numbers = scratchcards[to_process.popleft()]
        # Start from card_number, which is +1 from the given's card index in the list;
        to_process.extend(range(card_number, card_number + len(numbers)))
        total_num_scratchcards += 1
    t1 = time()
    print(f"The computation took: {t1 - t0:.2f}s")
    print(f"Total num. of scratchcards: {total_num_scratchcards}")
