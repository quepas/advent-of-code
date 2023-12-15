def compute_hash(text: str) -> int:
    """
    Compute a simple hash of a text
    """
    value = 0
    for ch in text:
        value += ord(ch)
        value *= 17
        value = value % 256
    return value


def parse_initialization_sequence(text: str) -> list[str]:
    """
    Parse initialization sequence
    """
    text = text.replace("\n", "")
    sequence = text.split(",")
    return sequence


with open("input") as f:
    init_sequence = parse_initialization_sequence(f.read())
    print("----- Part one -----")
    sequence_hash = sum(map(compute_hash, init_sequence))
    print(f"Sum of hashed initialization sequence: {sequence_hash}")
