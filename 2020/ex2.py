from operator import xor
from typing import Tuple


def parse_data_entry(entry: str) -> Tuple[int, int, chr, str]:
    occurrences, character, password = entry.split(" ")
    min_occurrence, max_occurrence = occurrences.split("-")
    return int(min_occurrence), int(max_occurrence), character[0], password


def is_valid_password_policy_1(min_occurrence, max_occurrence, character, password) -> bool:
    return min_occurrence <= password.count(character) <= max_occurrence


def is_valid_password_policy_2(position_a, position_b, character, password) -> bool:
    return xor(password[position_a - 1] == character, password[position_b - 1] == character)


policy_1 = {
    "invalid": 0,
    "valid": 0
}
policy_2 = {
    "invalid": 0,
    "valid": 0
}
with open("input_2.txt", "r") as f:
    for line in f.readlines():
        if is_valid_password_policy_1(*parse_data_entry(line)):
            policy_1['valid'] += 1
        else:
            policy_1['invalid'] += 1
        if is_valid_password_policy_2(*parse_data_entry(line)):
            policy_2['valid'] += 1
        else:
            policy_2['invalid'] += 1

print('Password policy #1 [valid={}, invalid={}]'.format(policy_1['valid'], policy_1['invalid']))
print('Password policy #2 [valid={}, invalid={}]'.format(policy_2['valid'], policy_2['invalid']))
