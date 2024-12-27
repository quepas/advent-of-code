def parse_line_of_ints(line: str, sep: str | None = None) -> list[int]:
    return list(map(int, line.split(sep)))
