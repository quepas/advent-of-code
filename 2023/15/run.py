import re
from typing import Optional

# Init step contains: label, operation [=,-], focal length [1-9]
InitStep = tuple[str, str, Optional[int]]


def compute_hash(text: str) -> int:
    """
    Compute a simple hash from a text
    """
    value = 0
    for ch in text:
        value += ord(ch)
        value *= 17
        value = value % 256
    return value


def read_init_sequence(text: str) -> list[str]:
    """
    Parse initialization sequence into tuples of label, operation, focal length
    """
    text = text.replace("\n", "")
    return text.split(",")


class LensBox:
    """
    Simple container of lenses able to add/remove lenses and compute their total focusing power.
    """

    def __init__(self, box_id: int):
        # We use the fact, that in recent Python the order of key insertion is maintained
        self.box = {}
        # Each box has an ID [0-255]
        self.box_id = box_id

    def add(self, label: str, focal_length: int):
        self.box[label] = focal_length

    def remove(self, label: str):
        self.box.pop(label, None)

    def focusing_power(self) -> int:
        # Multiply box number, lens ranks and their focal lengths
        return sum(map(lambda t: (self.box_id + 1) * t[0] * t[1], enumerate(self.box.values(), start=1)))

    def __len__(self):
        return len(self.box)


class LensConfiguration:
    """
    Collection of 256 lens boxes configured by repeated applying of initialization steps.
    Capable of computing total focusing power of all lenses across all boxes.
    It also creates and removes lens boxes when needed holding, at any time, only the necessary number of boxes.
    """

    def __init__(self):
        # Create/remove boxes on demand
        self.boxes: dict[int, LensBox] = {}

    def apply(self, init_step_text: str):
        label, operation, focal_length = self.parse_init_step(init_step_text)
        box_idx = compute_hash(label)
        if operation == "-":
            if box_idx in self.boxes:
                box = self.boxes[box_idx]
                box.remove(label)
                # If box is now empty => remove it
                if len(box) == 0:
                    self.boxes.pop(box_idx)
        elif operation == "=":
            # If requested box doesn't exist => create it
            if box_idx not in self.boxes:
                self.boxes[box_idx] = LensBox(box_idx)
            self.boxes[box_idx].add(label, focal_length)

    def focusing_power(self) -> int:
        return sum(map(lambda box: box.focusing_power(), self.boxes.values()))

    @staticmethod
    def parse_init_step(text: str) -> InitStep:
        match = re.match(r"([a-z]+)([-=])([1-9])?", text)
        return match.group(1), match.group(2), int(match.group(3)) if match.group(3) else None


with open("input") as f:
    init_sequence = read_init_sequence(f.read())
    print("----- Part one -----")
    sequence_hash = sum(map(compute_hash, init_sequence))
    print(f"Sum of hashed initialization sequence: {sequence_hash}")
    print("----- Part two -----")
    lens_config = LensConfiguration()
    for init_step in init_sequence:
        lens_config.apply(init_step)
    print(f"Total focusing power of lens configuration: {lens_config.focusing_power()}")
