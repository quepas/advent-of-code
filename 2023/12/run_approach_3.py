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


def find_next_position(record: str, group_size: int, start: int = 0) -> Optional[int]:
    for i in range(start, len(record)):
        # Find first possible start position
        if record[i] in ["#", "?"]:
            # Then test if the group can fit nicely
            group_end = i + group_size
            group = record[i:group_end]
            # If there is at least one good spring, we look for another place!
            # Otherwise, check what is after the group
            if record[group_end:(group_end + 1)] != "#" and group.count(".") == 0 and len(group) == group_size:
                return i
            # if record[i] == "#":
            #     return None
    return None


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
        Move the last group to a legal position
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
        new_position = find_next_position(self.record, last_group_size, start=search_start)
        if new_position is None:
            return None
        new_positions = self.positions.copy()
        new_positions[-1] = new_position
        return Placement(record=self.record, groups=self.groups, positions=new_positions)

    def first(self) -> Optional["Placement"]:
        # If each each group has already an assigned position, there is no possible extension
        if self.accept():
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
        new_position = find_next_position(self.record, group_size, start=search_start)
        if new_position is None:
            return None
        # Check if at the end there is not #
        # if len(self.groups) == len(self.positions) + 1 and self.record[new_position+1:].count("#") > 0:
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
        return len(self.positions) == len(self.groups)

    def __len__(self) -> int:
        """
        Placement length is the number of assigned positions
        """
        return len(self.positions)

    def __repr__(self):
        return f"Placement(groups={self.groups}, positions={self.positions})"


def matches(placement: Placement, conditions: str) -> bool:
    required = [i for i in range(len(conditions)) if conditions[i] == "#"]
    for idx in range(len(placement.positions)):
        start = placement.positions[idx]
        length = placement.groups[idx]
        if len(required) > 0 and min(required) < start:
            return False
        if conditions.find(".", start, start + length) > -1:
            return False
        required = list(filter(lambda x: x >= start + length, required))
    return True

    # placement_mask = [False] * len(conditions)
    # for idx in range(len(placement)):
    #     start = placement.positions[idx]
    #     length = placement.controls[idx]
    #     end = start + length
    #     placement_mask[start:end] = [True] * length
    # conditions_mask = list(map(lambda c: c in ["?", "#"], conditions))
    # return all(starmap(lambda x, y: (x and y) or (not x), zip(placement_mask, conditions_mask)))


total_counter = 0
wrong = 0


# def reject(conditions: str, )
def backtrack(record, controls: list[int], c: Placement):
    global total_counter
    global wrong
    # if c.full():
    # print(f"Testing: {c}, {controls}")
    # if not matches(c, record):
    #     return
    # pass
    if c.accept():
        if test_product_placement(c.positions, controls, record):
            wrong += 1
        else:
            print(f"Wrong?: {c}")
        # print(f"* Found output: {c}")
        total_counter += 1
        return
    s = c.first()
    while s is not None:
        backtrack(record, controls, s)
        s = s.next()


with open("input") as f:
    lines = f.readlines()
    total_arrangements = 0
    mul_factor = 1
    counter = 1
    for line in lines:
        print(f"----- Case: {counter} -----")
        conditions, control = line.split()
        control = list(map(int, control.split(",")))
        # Extend !
        conditions = "?".join([conditions] * mul_factor)
        control = [*control] * mul_factor
        print(conditions, control)

        # for idx in range(0, len(conditions)):
        # TODO: parallelism?
        root = Placement(conditions, groups=control)
        backtrack(conditions, control, root)
        counter += 1

        print(f"Total counter={total_counter}")
        print(f"Wrong={wrong}")

        # exit()

# Input - 6958
