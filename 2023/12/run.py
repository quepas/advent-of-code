import re
from functools import partial
from itertools import product, pairwise
from multiprocessing import Pool

ConditionGroup = tuple[int, int]  # min, max
Control = list[int]


def get_minimal_group(line: str) -> int:
    return max([0, *list(map(len, re.findall(r"#+", line)))])


def analyse_spring_condition(line: str) -> tuple[list[ConditionGroup], Control]:
    conditions, control = line.split()
    control = list(map(int, control.split(",")))
    print(conditions)
    conditions = list(map(lambda x: (get_minimal_group(x), len(x)), filter(lambda x: len(x), conditions.split("."))))

    print(conditions, control)
    # In a group possible arrangments: len(group) - segment size + 1
    # ??? 1 -> 3
    # ?#? 1 -> 0
    assignments = []
    for cond_min, cond_max in conditions:
        selected_controls = []
        for c in control:
            if cond_min <= c <= cond_max:
                selected_controls.append(c)
        if selected_controls:
            assignments.append([(cond_min, cond_max), selected_controls])

    print(assignments)
    return conditions, control


def valid_indexes(indexes: tuple, control: list[int], length: int, line: str) -> bool:
    start = list(indexes)
    # Start indices must be monotonic
    for i in range(1, len(start)):
        if start[i - 1] >= start[i]:
            return False

    end = list(map(lambda t: t[0] + t[1], zip(start, control)))

    # No index higher than the end
    for e in end:
        if e > length:
            return False
    # Next index must be less than end
    for i in range(1, len(start)):
        if start[i] <= end[i - 1]:
            return False
    # print(start, end)

    mask = list(map(lambda t: t != ".", line))
    # print(mask)

    required_mask = list(map(lambda t: t == "#", line))
    # print(required_mask)

    for s, e in zip(start, end):
        if not all(mask[s:e]):
            return False
    for r in range(len(required_mask)):
        if required_mask[r]:
            any_covers = False
            for s, e in zip(start, end):
                if s <= r < e:
                    any_covers = True
            if not any_covers:
                return False

    return start < end


def analyse_spring_condition2(id: int, line: str) -> int:
    print(f"Processing: {id}")
    conditions, control = line.split()
    control = list(map(int, control.split(",")))
    # print(conditions, control)

    count = 0
    length = len(conditions)
    ranges = [range(length)]
    for i in range(1, len(control)):
        ranges.append(range(control[i] - 1, length))

    for p in product(*ranges):
        if valid_indexes(p, control, len(conditions), conditions):
            # print(p)
            count += 1
    # exit()
    return count


def read_spring_conditions(lines: list[str]):
    with Pool() as p:
        res = p.starmap(analyse_spring_condition2, enumerate(lines, start=1))
    print(f"result: {sum(res)}")


def is_available(text: str) -> bool:
    return all(map(lambda x: x in ["?", "#"], text))


def make_initial_placement(conditions, control):
    last_index = 0
    for c_idx in range(len(control)):
        c = control[c_idx]
        real_size = c + 1 if c_idx + 1 < len(control) else 0
        end_index = len(conditions) - real_size
        print(f"end_index: {end_index}")
        for try_idx in range(last_index, end_index):
            if is_available(conditions[try_idx:try_idx + c]):
                print(f"Found placement for {c}: ({try_idx}:{try_idx + c})")
                last_index = try_idx + real_size
                break


def find_usable_range_of_spring_groups(text: str) -> tuple[int, int]:
    """
    Find start (inclusive) and end (exclusive) indices of possible placement of damaged spring groups.
    In other words, on each end, find the first non-"." character
    """
    left, right = 0, len(text) - 1
    usable = (None, None)
    while left <= right:
        if text[left] == ".":
            left += 1
        elif usable[0] is None:
            usable = (left, usable[1])
        if text[right] == ".":
            right -= 1
        elif usable[1] is None:
            usable = (usable[0], right)
        # Early exit
        if usable[0] is not None and usable[1] is not None:
            break
    return usable[0], usable[1] + 1


def find_known_partial_spring_groups(text: str) -> list[int]:
    partial_spring_groups = []
    candidate = None
    for idx in range(len(text)):
        ch = text[idx]
        if ch == "#" and candidate is None:
            candidate = idx
        elif ch != "#" and candidate is not None:
            partial_spring_groups.append(candidate)
            candidate = None
    return partial_spring_groups


def compute_used_space(control: list[int]) -> int:
    return sum(map(lambda value: value + 1, control))


def find_possible_placement_of_spring_groups(conditions: str, control: list[int]) -> list[list[int]]:
    # This is incorrect, because later, the compute_used_space() doesn't take into consideration
    # the usable range computed by the following line
    start_pos, end_pos = find_usable_range_of_spring_groups(conditions)
    # start_pos, end_pos = start_pos, end_pos + 1
    possible_placements = []
    for idx in range(len(control)):
        group_length = control[idx]
        num_left_controls = len(control[:idx])
        min_start_pos = compute_used_space(control[:idx]) + start_pos
        max_end_pos = end_pos - compute_used_space(control[idx + 1:])
        num_right_controls = len(control[idx + 1:])
        max_start_pos = max_end_pos - group_length
        num_left_dots = conditions[:min_start_pos].count(".")
        # print(num_left_controls, num_left_dots)
        if num_left_dots > num_left_controls:
            old = min_start_pos
            min_start_pos -= (num_left_dots - num_left_controls)
            print(f"Min_start_pos: {old} --> {min_start_pos}")
        num_right_dots = conditions[max_end_pos:].count(".")
        if num_right_dots > num_right_controls:
            old = max_end_pos
            max_end_pos -= (num_right_dots - num_right_controls)
            print(f"Max_end_pos: {old} --> {max_end_pos}")
            # min_start_pos

        # Recompute the min_start_pos by taking into account dots .
        # Increase min_start_pos by uncounted dots
        # Decrease max_end_pos by uncounted dots

        # print(min_start_pos, max_start_pos)
        # num_movements = max(0, max_end_pos - group_length)
        # print(
        #     f"control={group_length}; min-start-pos={min_start_pos}; "
        #     f"max-start-pos={max_start_pos};")
        if min_start_pos == max_start_pos:
            can_match = can_match_spring_group(conditions, min_start_pos, group_length)
            assert can_match, "When no movements available, the group must match to the only available position"
            possible_placements.append([min_start_pos])
            continue
        start_pos_range = []
        for start_idx in range(min_start_pos, max_start_pos + 1):
            can_match = can_match_spring_group(conditions, start_idx, group_length)
            if can_match:
                start_pos_range.append(start_idx)
                # print(f"\tstart_idx={start_idx}; can_match?={can_match}")
        possible_placements.append(start_pos_range)
    return possible_placements


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
        print(f"Still not empty! {indices}")
        return False
    return True


def filter_placements(placements: list[list[int]], control) -> list[list[int]]:
    index = 0
    for p1, p2 in pairwise(placements):
        current_control = control[index]
        # Remove current placement position incompatible with the next placement positions
        for pos in p1:
            if not any(filter(lambda x: pos + current_control <= x, p2)):
                print(f"Removing: {pos}")
                p1.remove(pos)
        index += 1
    return placements


# def compute_

with open("input_test_1") as f:
    # read_spring_conditions(f.readlines())
    lines = f.readlines()
    total_arrangements = 0
    mul_factor = 5
    for line in lines:
        conditions, control = line.split()
        control = list(map(int, control.split(",")))
        # conditions += "?"
        conditions = "?".join([conditions] * mul_factor)
        control = [*control] * mul_factor
        print(conditions, control)
        # find_possible_placement_of_spring_groups(conditions, control)
        possible_placements = find_possible_placement_of_spring_groups(conditions, control)
        possible_placements = filter_placements(possible_placements, control)
        print(f"Possible placements: {possible_placements}")
        working_placements = list(
            filter(partial(test_product_placement, control=control, conditions=conditions),
                   product(*possible_placements)))
        print(f"product={working_placements}")
        total_arrangements += len(working_placements)
        print(f"Total arrangements so far: {total_arrangements}")
    print(f"Total arrangements: {total_arrangements}")

    # make_initial_placement(conditions, control)

# 6389 to low (day 1)
# To high 8882
