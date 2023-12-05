from collections import deque
from time import time, time_ns


def parse_scratchcard(line: str) -> tuple[int, set[int]]:
    chunks = line.split()
    card_number = int(chunks[1][:-1])
    split = chunks.index("|")
    winning_numbers = set(map(int, chunks[2:split]))
    scratched_numbers = set(map(int, chunks[split + 1:]))
    return card_number, winning_numbers & scratched_numbers


def count_scratched_winning_points(winning_scratched_numbers: set[int]) -> int:
    """
    Compute number of points given a list of winning-scratched numbers
    """
    return 2 ** (len(winning_scratched_numbers) - 1) if len(winning_scratched_numbers) else 0


def count_scratchcards_fast(scratchcards: list[tuple]) -> int:
    # Number of winning numbers in each scratchcard
    num_wins_per_scratchcard = list(map(lambda x: len(x[1]), scratchcards))
    # At the beginning, we have 0 cards of each type
    num_scratchcards = [0] * len(scratchcards)
    for i in range(len(scratchcards)):
        # Visiting the i-th card
        num_scratchcards[i] += 1
        next_winning_card = i + 1
        last_winning_card = next_winning_card + num_wins_per_scratchcard[i]
        # Increment number of following cards (i+1, i+2, ...),
        # by the number of the current card (i) for all the following winners
        for j in range(next_winning_card, last_winning_card):
            num_scratchcards[j] += num_scratchcards[i]
    return sum(num_scratchcards)


def count_scratchcards_bfs(scratchcards: list[tuple]) -> int:
    # Start from 0, the index of the first scratchcard in the list
    to_process = deque(range(0, len(scratchcards)))
    total_num_scratchcards = 0
    while len(to_process):
        card_number, numbers = scratchcards[to_process.popleft()]
        # Start from card_number, which is +1 from the given's card index in the list;
        to_process.extend(range(card_number, card_number + len(numbers)))
        total_num_scratchcards += 1
    return total_num_scratchcards


with open("input") as f:
    scratchcards = list(map(parse_scratchcard, f.readlines()))
    print("----- Part one -----")
    total_points = sum(map(count_scratched_winning_points,
                           map(lambda scratchcard: scratchcard[1],
                               scratchcards)))
    print(f"Total points from all scratchcards: {total_points}")
    print("----- Part two [bfs] -----")
    t0 = time()
    total_num_scratchcards = count_scratchcards_bfs(scratchcards)
    t1 = time()
    print(f"Total num. of scratchcards: {total_num_scratchcards}")
    print(f"The computation took: {t1 - t0:.2f}s")
    print("----- Part two [fast] -----")
    t0 = time_ns()
    total_num_scratchcards = count_scratchcards_fast(scratchcards)
    t1 = time_ns()
    print(f"Total num. of scratchcards: {total_num_scratchcards}")
    print(f"The computation took: {(t1 - t0) / 1_000_000:.2f}ms")
