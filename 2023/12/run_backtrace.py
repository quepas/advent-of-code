from functools import partial, cache
from multiprocessing import Pool
from pathlib import Path
from time import time
from typing import Optional


def can_match_spring_group(conditions: str, start_pos: int, length: int) -> bool:
    """
    Check if a spring group of given length matches conditions at the given start index.
    We assume, the gap between two spring groups is located at the end.
    """
    # Check if a spring group matches only # or ? characters
    masked_conditions = list(map(lambda cond: cond in ["#", "?"], conditions[start_pos: start_pos + length]))
    before_spring_group = conditions[:start_pos]
    # The last character before a spring group cannot be the "#", otherwise it would need to belong to the group
    if len(before_spring_group) > 0 and before_spring_group[-1] == "#":
        return False
    after_spring_group = conditions[start_pos + length:]
    # The first character after a spring group cannot be the "#", otherwise it would need to belong to the group
    if len(after_spring_group) > 0 and after_spring_group[0] == "#":
        return False
    return all(masked_conditions)


def test_product_placement(placement: list[int], control: list[int], conditions: str) -> bool:
    # print(f"Testing product placement: {placement}, {control}")
    for idx in range(len(control) - 1):
        if placement[idx] + control[idx] >= placement[idx + 1]:
            return False
    # Check if the whole placement applies nicely:
    for idx in range(len(control)):
        if not can_match_spring_group(conditions, placement[idx], control[idx]):
            return False
    # Check if all # are covered
    indices = set(i for i, _ in enumerate(conditions) if conditions[i] == '#')
    for idx in range(len(control)):
        for i in range(placement[idx], placement[idx] + control[idx]):
            try:
                indices.remove(i)
            except:
                pass
    if indices:
        # print(f"Still not empty! {indices}")
        return False
    return True


def find_next_position(record: str, group_size: int, start: int = 0, end: Optional[int] = None) -> Optional[int]:
    """
    Find first valid position of a group after a given start index
    """
    if end is None:
        end = len(record) - group_size + 1
    for i in range(start, end):
        # Find first possible start position
        if record[i] in ["#", "?"]:
            # Then test if the group can fit nicely
            group_end = i + group_size
            group = record[i:group_end]
            # If there is at least one good spring, we look for another place!
            # Otherwise, check what is after the group
            if record[group_end:(group_end + 1)] != "#" and group.count(".") == 0 and len(group) == group_size:
                return i
            if record[i] == "#":
                return None
    return None


def compute_used_space(control: list[int]) -> int:
    return sum(map(lambda value: value + 1, control))


class Placement:

    def __init__(self, record, groups, positions=None) -> None:
        self.record = record
        self.groups = groups
        if positions is None:
            positions = []
        self.positions = positions
        self.next_placement = 0

    def next(self) -> Optional["Placement"]:
        """
        Move the latest group to a legal position
        """
        # Placement with no positions cannot have a next state
        if len(self.positions) == 0:
            return None
        # If the last group starts with #, we can't jump beyond it because it must be included in some group
        if self.record[self.positions[-1]] == "#":
            return None
        # Otherwise, find the next legal position of the last group
        # Start from the +1 of the last position
        last_group_size = self.groups[len(self.positions) - 1]
        search_start = self.positions[-1] + 1
        assigned_groups = len(self.positions)
        end = len(self.record) - compute_used_space(self.groups[assigned_groups:])
        # print("[", search_start, ", ", end, "]")
        # if end <= search_start:
        #     end = None
        new_position = find_next_position(self.record, last_group_size, start=search_start, end=end)

        if new_position is None:
            return None
        new_positions = self.positions.copy()
        new_positions[-1] = new_position
        return Placement(record=self.record, groups=self.groups, positions=new_positions)

    def first(self) -> Optional["Placement"]:
        # If each each group has already an assigned position, there is no possible extension
        if len(self.positions) == len(self.groups):
            return None
        # Otherwise, find the next legal position of the last group
        if len(self.positions) > 0:
            # Start from the +1 of the last position
            last_group_size = self.groups[len(self.positions) - 1]
            search_start = self.positions[-1] + last_group_size + 1
            group_size = self.groups[len(self.positions)]
        else:
            search_start = 0
            group_size = self.groups[len(self.positions)]
        # End is next # + group_size
        try:
            end = self.record[search_start:].index("#") + search_start
            end += group_size + 1
        except:
            end = None
        new_position = find_next_position(self.record, group_size, start=search_start, end=end)
        if new_position is None:
            return None

        # Check if at the end there is not #
        # if len(self.groups) == len(self.positions) + 1 and self.record[new_position+group_size:].count("#") > 0:
        #     return None
        new_positions = self.positions.copy()
        new_positions.append(new_position)
        return Placement(record=self.record, groups=self.groups, positions=new_positions)

    def accept(self) -> bool:
        """
        Placement is accepted when each group has an assigned position.
        Because the invariant is that at each change first/next a correct position is placed, then
        when all of them are assigned the end result is a correct placement.
        """
        if len(self.positions) == len(self.groups):
            return self.record[self.positions[-1] + self.groups[-1]:].count("#") == 0
        return False

    def __len__(self) -> int:
        """
        Placement length is the number of assigned positions
        """
        return len(self.positions)

    def __repr__(self):
        return f"Placement(groups={self.groups}, positions={self.positions})"


total_finished = 0


# @cache
def backtrack(c: Placement) -> int:
    if c.accept():
        return 1
    s = c.first()
    count = 0
    while s is not None:
        count += backtrack(s)
        s = s.next()
    return count


def fill_record(counter: int, full_record: str) -> int:
    # Non-parallel version
    record, control = full_record
    root = Placement(record, groups=control)
    result = backtrack(root)
    print(f"Finished: {counter}")
    return result


def parse_record(record: str, mul_factor: int) -> tuple[str, list]:
    conditions, control = record.split()
    control = list(map(int, control.split(",")))
    # Extend !
    # mul_factor = 5
    conditions = "?".join([conditions] * mul_factor)
    # conditions = conditions + "?"
    control = [*control] * mul_factor
    return conditions, control


def run_test(path: Path, mul_factor: int = 1):
    print(f">> Testing: {path} with x factor: {mul_factor}")
    t0 = time()
    with open(path) as f:
        lines = f.readlines()
        records = list(map(partial(parse_record, mul_factor=mul_factor), lines))
        # print(f"----- Case: {counter} -----")
        # print(conditions, control)
        with Pool() as p:
            total_arrangements = p.starmap(fill_record, enumerate(records, start=1))
        print(f"Arrangements: {total_arrangements}")
        print(f"Num. of total arrangements: {sum(total_arrangements)}")
    t1 = time()
    print(f"Took time: {t1 - t0}s")
    return total_arrangements


# run_test("input_test_1", 5)
# run_test("input_test_hard", 3)
run_test("input", 1)
# run_test("input_test_hard", 1)
# Input - 6958

#    per-placement ; per-line ; cache
# factor x1 => 11s ; 0.1 s
# factor x2 => 21s ; 10.2 s ; 2s
# factor x3 =>     ;        ;
# factor x4 =>

# 3455501625284 - too low
