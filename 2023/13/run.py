from enum import Enum
from functools import partial
from itertools import pairwise, starmap
from typing import Optional, Callable


class ReflectionType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


# Number of rows above and columns to the left from the middle of a reflection pattern
ReflectionNote = tuple[int, int]


def count_differences(str_a: str, str_b: str) -> int:
    """
    Count number of differences between two strings.
    *Assumption*: strings must have the same length.
    """
    return sum(1 for ca, cb in zip(str_a, str_b) if ca != cb)


class MirrorPattern:
    """
    Representation of a mirror pattern capable of finding its reflection with a note.
    """

    def __init__(self, pattern_text: str):
        self.pattern = pattern_text.split()
        self.height = len(self.pattern)
        self.width = len(self.pattern[0])

    def get_column(self, column_idx: int) -> str:
        return "".join([row[column_idx] for row in self.pattern])

    def get_row(self, row_idx: int) -> str:
        return self.pattern[row_idx]

    def find_reflection_note(self, with_smudge=False) -> ReflectionNote:
        """
        Find and return a reflection note (number of rows above and columns to the left from
        the middle of a reflection).

        *Assumption*: at most one type of a reflection exists (smudged or perfect).
        """
        columns_left = self._test_symetry(ReflectionType.VERTICAL, max_differences=1 if with_smudge else 0)
        rows_above = self._test_symetry(ReflectionType.HORIZONTAL, max_differences=1 if with_smudge else 0)
        return rows_above, columns_left

    def _test_symetry(self, reflection: ReflectionType, max_differences: int = 0) -> Optional[int]:
        """
        Test vertical or horizontal reflection with a maximal number of differences between single "pixels"
        (1 for smudges, 0 for perfect reflections).

        *Assumption*: at most one type of a reflection exists (smudged or perfect)
        """
        # Depending on the reflection, we will select rows (horizontal) or columns (vertical)
        select: Callable[[int], str] = self.get_column if reflection == ReflectionType.VERTICAL else self.get_row
        # Depending on the reflection, we can move no more than pattern height (horizontal) or width (vertical)
        max_index: int = self.width if reflection == ReflectionType.VERTICAL else self.height
        # Investigate each reflection point (middle)
        for middle in pairwise(range(max_index)):
            left, right = middle
            found_differences = 0
            # As long as we are in the pattern with no more than max_differences
            while left > -1 and right < max_index and found_differences <= max_differences:
                found_differences += count_differences(select(left), select(right))
                # Move by one to the edges on both ends
                left -= 1
                right += 1
            # Check if we have a reflection (it touches either end of the mirror pattern
            # and has no more than max_differences in total)
            if found_differences == max_differences and (left == -1 or right == max_index):
                # Because we are indexing from 0, the "right" row/column from a middle also represents the number
                # of rows above or columns to the left
                return middle[1]
        return 0


def read_patterns(content: str) -> list[MirrorPattern]:
    """
    Read content into a list MirrorPatterns created from multi-line text patterns.
    """
    return list(map(MirrorPattern, content.split("\n\n")))


def summarise_notes(reflection_notes: list[ReflectionNote]) -> int:
    """
    Summarise a list of reflection notes.
    """
    return sum(starmap(lambda rows_above, left_columns: rows_above * 100 + left_columns, reflection_notes))


with open("input") as f:
    patterns = read_patterns(f.read())
    print("----- Part one -----")
    perfect_reflections = list(map(partial(MirrorPattern.find_reflection_note, with_smudge=False), patterns))
    print(f"Summarized notes of perfect reflections: {summarise_notes(perfect_reflections)}")
    print("----- Part two -----")
    smudged_reflections = list(map(partial(MirrorPattern.find_reflection_note, with_smudge=True), patterns))
    print(f"Summarized notes of smudged reflections: {summarise_notes(smudged_reflections)}")
