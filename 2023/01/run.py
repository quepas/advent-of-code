def parse_number(line: str, in_reverse: bool = False, with_words: bool = False) -> int:
    idx = len(line) - 1 if in_reverse else 0
    while len(line) > idx >= 0:
        if line[idx].isnumeric():
            return int(line[idx])
        elif with_words:
            if line[idx] == "o":  # Could be one
                if line[idx:idx + 3] == "one":
                    return 1
            elif line[idx] == "t":  # Could be two, three
                if line[idx:idx + 3] == "two":
                    return 2
                elif line[idx:idx + 5] == "three":
                    return 3
            elif line[idx] == "f":  # Could be four, five
                if line[idx:idx + 4] == "four":
                    return 4
                elif line[idx:idx + 4] == "five":
                    return 5
            elif line[idx] == "s":  # Could be six, seven
                if line[idx:idx + 3] == "six":
                    return 6
                elif line[idx:idx + 5] == "seven":
                    return 7
            elif line[idx] == "e":  # Could be eight
                if line[idx:idx + 5] == "eight":
                    return 8
            elif line[idx] == "n":  # Could be nine
                if line[idx:idx + 4] == "nine":
                    return 9
        idx += -1 if in_reverse else 1
    # This should not happened
    exit(-1)


def find_calibration_value(line: str, with_words: bool = False) -> int:
    first_num = parse_number(line, with_words=with_words)
    last_num = parse_number(line, in_reverse=True, with_words=with_words)
    return 10 * first_num + last_num


with open("input", "r") as f:
    lines = f.readlines()
    print("Part one:", sum(map(find_calibration_value, lines)))
    print("Part two:", sum(map(lambda line: find_calibration_value(line, with_words=True), lines)))
