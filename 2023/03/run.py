from functools import reduce
from operator import itemgetter, mul


def parse_line(line: str) -> tuple[list[tuple], list[tuple]]:
    idx = 0
    tokens = []
    symbols = []
    while idx < len(line):
        ch = line[idx]
        if ch == "." or ch == "\n":
            idx += 1
        elif ch.isnumeric():
            start = idx
            while ch.isnumeric() and idx + 1 < len(line):
                idx += 1
                ch = line[idx]
            end = idx
            tokens.append((int(line[start:end]), start, end))
        else:
            symbols.append((ch, idx))
            idx += 1
    return symbols, tokens


with open("input") as f:
    parsed = []
    for line in f.readlines():
        line_width = len(line) - 1
        parsed.append(parse_line(line))

    engine_parts = []
    shared_gears = {}
    for i in range(len(parsed)):
        all_symbols1, numbers = parsed[i]
        # print(i, all_symbols1)
        symbols = list(map(itemgetter(1), all_symbols1))
        # Check before-after number
        for num, start, end in numbers:
            adj_symbols = list(filter(lambda sym: max(0, start - 1) == sym[1], all_symbols1))
            if len(adj_symbols) > 0:
                engine_parts.append(num)
                shared_gears.setdefault((i, max(0, start - 1)), []).append(num)
            adj_symbols = list(filter(lambda sym: sym[1] == min(line_width, end), all_symbols1))
            if len(adj_symbols) > 0:
                engine_parts.append(num)
                shared_gears.setdefault((i, min(line_width, end)), []).append(num)
            # Check previous line
            if i > 0:
                all_symbols2, _ = parsed[i - 1]
                prev_symbols = list(map(itemgetter(1), all_symbols2))
                adj_symbols = list(
                    filter(lambda sym: sym[1] >= max(0, start - 1) and sym[1] < min(line_width, end + 1), all_symbols2))
                # if any(symbol >= max(0, start - 1) and symbol < min(line_width, end + 1) for symbol in prev_symbols):
                if len(adj_symbols):
                    engine_parts.append(num)
                    for sym, idx in adj_symbols:
                        shared_gears.setdefault((i - 1, idx), []).append(num)
            # Check next line
            if i + 1 < len(parsed):
                all_symbols3, _ = parsed[i + 1]
                next_symbols = list(map(itemgetter(1), all_symbols3))
                adj_symbols = list(
                    filter(lambda sym: sym[1] >= max(0, start - 1) and sym[1] < min(line_width, end + 1), all_symbols3))
                # if any(symbol >= max(0, start - 1) and symbol < min(line_width, end + 1) for symbol in next_symbols):
                if len(adj_symbols):
                    engine_parts.append(num)
                    for sym, idx in adj_symbols:
                        shared_gears.setdefault((i + 1, idx), []).append(num)
    print(engine_parts)

    print(shared_gears)
    gear_sum = 0
    for k, v in shared_gears.items():
        if len(v) > 1:
            gear_sum += reduce(mul, v, 1)
    print("Results: ", sum(engine_parts), gear_sum)
