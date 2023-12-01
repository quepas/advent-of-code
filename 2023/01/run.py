from math import ceil
from typing import Optional

def parse_numbers(line: str) -> list[str]:
    numbers = []
    idx = 0
    while idx < len(line):
        if line[idx].isnumeric():
            numbers.append(line[idx])
        elif line[idx] == "o": # Could be one
            if line[idx:idx+3] == "one":
                numbers.append("1")
        elif line[idx] == "t": # Could be two, three
            if line[idx:idx+3] == "two":
                numbers.append("2")
            elif line[idx:idx+5] == "three":
                numbers.append("3")
        elif line[idx] == "f": # Could be four, five
            if line[idx:idx+4] == "four":
                numbers.append("4")
            elif line[idx:idx+4] == "five":
                numbers.append("5")
        elif line[idx] == "s": # Could be six, seven
            if line[idx:idx+3] == "six":
                numbers.append("6")
            elif line[idx:idx+5] == "seven":
                numbers.append("7")
        elif line[idx] == "e": # Could be eight
            if line[idx:idx+5] == "eight":
                numbers.append("8")
        elif line[idx] == "n": # Could be nine
            if line[idx:idx+4] == "nine":
                numbers.append("9")
        idx += 1
    return numbers

def find_calibration_value(line: str) -> int:
    numbers = parse_numbers(line)
    print(f"Found numbers: {numbers}")
    first_num, last_num = numbers[0], numbers[-1]
    #first_num, last_num = None, None
    #for offset in range(len(line)):
    #    if first_num is None and line[offset].isnumeric():
    #        first_num = line[offset]
    #    if last_num is None and line[-(1+offset)].isnumeric():
    #        last_num = line[-(1+offset)]
    #    if first_num is not None and last_num is not None:
    #        break
    #print(f"Found calibration value: {int(first_num + last_num)}")
    return int(first_num + last_num)


with open("input", "r") as f:
    lines = f.readlines()
    print(sum(map(find_calibration_value, lines)))

