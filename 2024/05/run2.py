# X|Y -> Y has before X
from os import walk


has_before = {}
# X|Y -> X has after Y
has_after = {}
# Pages to update
page_updates = []


def put(key: int, value: int, ordering_map: dict) -> None:
    if key in ordering_map:
        ordering_map[key].append(value)
    else:
        ordering_map[key] = [value]


def check_order(update: list[int], has_before: dict, has_after: dict) -> bool:
    wrong_order = False
    for idx, page in enumerate(update):
        before = set(update[:idx])
        after = set(update[idx + 1 :])
        if before.intersection(has_after.get(page, [])) or after.intersection(
            has_before.get(page, [])
        ):
            wrong_order = True
            break
    return not wrong_order


def fix_order(update: list[int], has_before: dict, has_after: dict) -> None:
    new_update = []
    for idx, page in enumerate(update):
        before = update[:idx]
        after = update[idx+1:]
        for bpage in before:
            if bpage in has_after.get(page, p[):

        if set(before).intersection(has_after.get(page, [])):
            pass
        else:
            new_update.append(page)
    return new_update


    # print("fix_Order:", update)
    # if len(update) == 1:
    #     return update
    # if len(update) == 2:
    #     a, b = update
    #     if a in has_after.get(b, []) or b in has_before.get(a, []):
    #         return [b, a]
    #     else:
    #         return update
    # else:
    #     pair = fix_order(update[:2], has_before, has_after)
    #     tail = fix_order(update[2:], has_before, has_after)
    #     return pair + tail
        
                

with open("input_test", "r") as f:
    for line in f.readlines():
        if "|" in line:
            before, after = list(map(int, line.strip().split("|")))
            put(before, after, has_after)
            put(after, before, has_before)
        if "," in line:
            page_updates.append(list(map(int, line.strip().split(","))))
    print(has_before, has_after, page_updates)

    num_wrong_orders = 0
    right_order_sum = 0
    for single_update in page_updates:
        if not check_order(single_update, has_before, has_after):
            num_wrong_orders += 1
            print("Fixed: ", fix_order(single_update, has_before, has_after))
        else:
            print("Correct", single_update)
            median_elem = single_update[int(len(single_update) / 2)]
            right_order_sum += median_elem
    print("Wrong orders:", num_wrong_orders)
    print("Right order sum:", right_order_sum)
