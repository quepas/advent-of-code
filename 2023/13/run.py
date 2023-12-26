from enum import Enum
from itertools import pairwise
from typing import Optional


class SymmetryType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class MirrorPattern:

    def __init__(self, pattern_text: str):
        self.initial_pattern = pattern_text.split()
        self.working_pattern = self.initial_pattern.copy()
        self.height = len(self.working_pattern)
        self.width = len(self.working_pattern[0])
        self.smudges = {
            SymmetryType.VERTICAL: None,
            SymmetryType.HORIZONTAL: None
        }

    def get_column(self, column_idx: int) -> str:
        return "".join([row[column_idx] for row in self.working_pattern])

    def get_row(self, row_idx: int) -> str:
        return self.working_pattern[row_idx]

    def restore(self):
        self.working_pattern = self.initial_pattern.copy()

    def fix_smudge(self, smudge: tuple[int]):
        row = self.get_row(smudge[0])
        marker = "#" if row[smudge[1]] == "." else "."
        new_row = row[:smudge[1]] + marker + row[smudge[1] + 1:]
        self.working_pattern[smudge[0]] = new_row

    def find_symmetry(self) -> list[tuple[SymmetryType, int]]:
        """
        Find and return the first valid symmetry type and symmetry value
        """
        columns_left = self._test_symetry(SymmetryType.VERTICAL)
        rows_above = self._test_symetry(SymmetryType.HORIZONTAL)
        # assert not (columns_left is not None and rows_above is not None), ("Cannot find both types of symmetries "
        #                                                                    "in one pattern")
        symmetries = []
        if columns_left is not None:
            # self.smudges.pop(SymmetryType.HORIZONTAL)
            symmetries.append((SymmetryType.VERTICAL, columns_left[1]))
        if rows_above is not None:
            # self.smudges.pop(SymmetryType.VERTICAL)
            symmetries.append((SymmetryType.HORIZONTAL, rows_above[1]))
        return symmetries

    def _test_symetry(self, symmetry_type: SymmetryType) -> Optional[int]:
        """
        Test vertical or horizontal symmetry and find any smudges at the same time
        """
        select = self.get_column if symmetry_type == SymmetryType.VERTICAL else self.get_row
        max_index: int = self.width if symmetry_type == SymmetryType.VERTICAL else self.height
        # all_smudges = []
        for middle in pairwise(range(max_index)):
            left, right = middle
            symmetry_size = 0
            while left >= 0 and right < max_index and select(left) == select(right):
                symmetry_size += 1
                left -= 1
                right += 1
            # At a first occurrence of an inequality, we might have a smudge
            if left >= 0 and right < max_index:
                #     # print(f"middle{middle}")
                smudges = find_smudge(select(left), select(right))
                if smudges is not None:
                    idx = None
                    if symmetry_type == SymmetryType.VERTICAL:
                        idx = (smudges, right)
                    else:
                        idx = (right, smudges)
                    print(f"Found smudge {left} : {right} : {symmetry_type}")
                    self.smudges[symmetry_type] = idx
            # Check if real reflection pattern (if it touches either end)
            elif symmetry_size > 0 and (left == -1 or right == max_index):
                # print(f"Symmetry: {symmetry_size}, {middle}, {left}, {right}")
                return middle
        return None

    def __str__(self):
        return "\n".join(self.working_pattern)


def read_patterns(content: str) -> list:
    patterns = content.split("\n\n")
    # patterns = list(map(str.split, patterns))
    return patterns


# If there are no smudges => a == b
def find_smudge(a, b) -> Optional[int]:
    smudges = []
    for i in range(len(a)):
        if a[i] != b[i]:
            smudges.append(i)
    if len(smudges) == 1:
        # print(f"Smudges: {smudges}")
        return smudges[0]
    return None


def plot_pattern(pattern: list[str], idx: tuple[int, int], vertical=False) -> None:
    (nrow, ncol) = len(pattern), len(pattern[0])
    counter = 1
    # Prepare header
    if vertical:
        print("".join(map(str, range(1, ncol + 1))))
        s = "*" * idx[0] + "><"
        print(s)
        for line in pattern:
            print(line)
    else:
        counter = 1
        for line in pattern:
            marker = " "
            if counter == idx[0] + 1:
                marker = "v"
            if counter == idx[1] + 1:
                marker = "^"
            print(f"{counter:2}{marker}{line}")
            counter += 1


with open("input") as f:
    patterns = read_patterns(f.read())
    print("----- Part one -----")
    total_sum = 0
    new_total_sum = 0
    counter = 1
    for pattern in patterns:
        print(f"--- Pattern: {counter} ---")
        used_new = False
        mirror_pattern = MirrorPattern(pattern)
        # symmetry_type, symmetry_value = mirror_pattern.find_symmetry()
        symmetry_type, symmetry_value = mirror_pattern.find_symmetry()[0]
        print(f"Original symmetry: {symmetry_type}:{symmetry_value}")
        if symmetry_type == SymmetryType.VERTICAL:
            total_sum += symmetry_value
        elif symmetry_type == SymmetryType.HORIZONTAL:
            total_sum += symmetry_value * 100
        smudges = mirror_pattern.smudges
        if smudges[SymmetryType.VERTICAL] is not None:
            mirror_pattern.fix_smudge(smudges[SymmetryType.VERTICAL])
            for new_symmetry in mirror_pattern.find_symmetry():
                stype, svalue = new_symmetry
                if stype == symmetry_type and svalue == symmetry_value:
                    continue
                print(f"New symmetry: {new_symmetry}, old: {symmetry_type}:{symmetry_value}")
                used_new = True
                if stype == SymmetryType.VERTICAL:
                    new_total_sum += svalue
                elif stype == SymmetryType.HORIZONTAL:
                    new_total_sum += svalue * 100
            mirror_pattern.restore()
        if smudges[SymmetryType.HORIZONTAL] is not None:
            mirror_pattern.fix_smudge(smudges[SymmetryType.HORIZONTAL])
            for new_symmetry in mirror_pattern.find_symmetry():
                stype, svalue = new_symmetry
                if stype == symmetry_type and svalue == symmetry_value:
                    continue
                print(f"New symmetry: {new_symmetry}, old: {symmetry_type}:{symmetry_value}")
                used_new = True
                if stype == SymmetryType.VERTICAL:
                    new_total_sum += svalue
                elif stype == SymmetryType.HORIZONTAL:
                    new_total_sum += svalue * 100
            mirror_pattern.restore()
        if not used_new:
            if symmetry_type == SymmetryType.VERTICAL:
                new_total_sum += symmetry_value
            elif symmetry_type == SymmetryType.HORIZONTAL:
                new_total_sum += symmetry_value * 100
        counter += 1
        # exit()
    print(f"Total symmetry value across all mirror patterns: {total_sum}")
    print(f"New total symmetry value across all mirror patterns: {new_total_sum}")

# Part 2
# 18984 -- too low
# 27161 -- too low
