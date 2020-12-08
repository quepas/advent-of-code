from typing import Dict
import re

expected_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']  # 'cid' is optional
eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def prepare_passport(passport_entry: str) -> Dict:
    passport = {}
    entry = passport_entry.replace('\n', ' ').strip()  # Normalise the passport to one line
    for prop in entry.split(' '):
        key, value = prop.split(':')
        passport[key] = value
    return passport


def validate_hgt(hgt: str) -> bool:
    g = re.match("^([1-9][0-9]{1,2})(cm|in)$", hgt)
    if g is None:
        return False

    if g.group(2) == "cm":
        return 150 <= int(g.group(1)) <= 193
    if g.group(2) == "in":
        return 59 <= int(g.group(1)) <= 76


def is_valid_passport_policy_1(passport_dict: Dict) -> bool:
    return all(key in passport_dict for key in expected_fields)


def is_valid_passport_policy_2(passport_dict: Dict) -> bool:
    if not is_valid_passport_policy_1(passport_dict):
        return False
    # Validate
    if not (1920 <= int(passport_dict['byr']) <= 2002):
        return False
    if not (2010 <= int(passport_dict['iyr']) <= 2020):
        return False
    if not (2020 <= int(passport_dict['eyr']) <= 2030):
        return False
    # Height
    hgt = passport_dict['hgt']
    if not validate_hgt(hgt):
        return False
    if not re.search("^#[0-9a-f]{6}$", passport_dict["hcl"]):
        return False
    if passport_dict['ecl'] not in eye_colors:
        return False
    if not re.search("^[0-9]{9}$", passport_dict['pid']):
        return False
    print(passport_dict)
    return True


with open('input_4.txt', 'r') as f:
    data = "".join(f.readlines())
    passports = data.split("\n\n")  # Passports are separated by a blank line

    valid_passports_policy_1 = 0
    valid_passports_policy_2 = 0
    for single_passport in passports:
        if is_valid_passport_policy_1(prepare_passport(single_passport)):
            valid_passports_policy_1 += 1
        if is_valid_passport_policy_2(prepare_passport(single_passport)):
            valid_passports_policy_2 += 1
    print("Valid passports by policy #1: {}".format(valid_passports_policy_1))
    print("Valid passports by policy #2: {}".format(valid_passports_policy_2))
