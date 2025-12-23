import os
from math import ceil, log10
from pathlib import Path

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
with open(dir_path / "input", "r") as f:
    ranges = [tuple(int(e) for e in k.split("-")) for k in f.read().strip().split(",")]
    sum_invalid_ids_part1 = 0
    sum_invalid_ids_part2 = 0
    for x1, x2 in ranges:
        for num in range(x1, (x2 + 1)):
            # --- Part 1: sum numbers consisting of exactly two equal subsequences
            n_digits = int(log10(num)) + 1
            # Skip single numbers (they have no repeated sequences :D)
            if n_digits == 1:
                continue
            # The number must have even length! Otherwise it cannot be made of only 2 sequences
            if n_digits % 2 == 0:
                mask = 10 ** (n_digits // 2)  # Get left and right halves of the number
                left = num // mask
                right = num % mask
                if left == right:
                    sum_invalid_ids_part1 += num
            # --- Part 2: accepts numbers of odd length as well!
            s = str(num)
            mid = ceil(n_digits / 2)
            # Try subsequences of size 1, 2, ..., mid (maximal two subsequences!)
            for k in range(1, mid + 1):
                uniqe_subseq = set()
                # Only when subseq size perfectly divides the number string
                if n_digits % k == 0:
                    chunks = [s[i : (i + k)] for i in range(0, n_digits, k)]
                    uniqe_subseq.update(chunks)
                # If only one subseq is repeated in the number...
                if len(uniqe_subseq) == 1:
                    sum_invalid_ids_part2 += num
                    # If we found a match we quit the subseq size loop,
                    # because numbers like: 222222 could be found several times:
                    #    222-222, 22-22-22, 2-2-2-2-2-2.
                    break

    print(f"Part 1: Sum invalid IDs={sum_invalid_ids_part1} (should be 23701357374)")
    print(f"Part 2: Sum invalid IDs={sum_invalid_ids_part2} (should be 34284458938)")
