def parse_first_number(line: str, in_reverse: bool = False, with_words: bool = False) -> list[str]:
    numbers = []
    idx = len(line) if in_reverse else 0
    while idx < len(line):
        if line[idx].isnumeric():
            numbers.append(line[idx])
        elif with_words:
            if line[idx] == "o":  # Could be one
                if line[idx:idx + 3] == "one":
                    numbers.append("1")
            elif line[idx] == "t":  # Could be two, three
                if line[idx:idx + 3] == "two":
                    numbers.append("2")
                elif line[idx:idx + 5] == "three":
                    numbers.append("3")
            elif line[idx] == "f":  # Could be four, five
                if line[idx:idx + 4] == "four":
                    numbers.append("4")
                elif line[idx:idx + 4] == "five":
                    numbers.append("5")
            elif line[idx] == "s":  # Could be six, seven
                if line[idx:idx + 3] == "six":
                    numbers.append("6")
                elif line[idx:idx + 5] == "seven":
                    numbers.append("7")
            elif line[idx] == "e":  # Could be eight
                if line[idx:idx + 5] == "eight":
                    numbers.append("8")
            elif line[idx] == "n":  # Could be nine
                if line[idx:idx + 4] == "nine":
                    numbers.append("9")
        idx += -1 if in_reverse else 1
    return numbers


def find_calibration_value(line: str, with_words: bool = False) -> int:
    numbers = parse_first_number(line, with_words=with_words)
    # print(f"Found numbers: {numbers}")
    first_num, last_num = numbers[0], numbers[-1]
    return int(first_num + last_num)


with open("input", "r") as f:
    lines = f.readlines()
    print("Part one:", sum(map(find_calibration_value, lines)))
    print("Part two:", sum(map(lambda line: find_calibration_value(line, with_words=True), lines)))
