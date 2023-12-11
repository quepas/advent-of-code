from functools import partial
from itertools import combinations, starmap

Galaxy = tuple[int, int]


class GalaxyTracker:
    """
    As we are interested only in an area with any galaxies,
    we can easily skip all expansions outside this area
    """

    def __init__(self, initial_size: tuple[int, int]):
        self.galaxies: list[Galaxy] = []
        # We start with possible rows/columns, but each time we track a new galaxy, we remove its row/column
        self.unused_rows: list[int] = list(range(0, initial_size[0]))
        self.unused_columns: list[int] = list(range(0, initial_size[1]))

    def __len__(self):
        return len(self.galaxies)

    def track(self, galaxy: Galaxy) -> None:
        self.galaxies.append(galaxy)
        row, column = galaxy
        if row in self.unused_rows:
            self.unused_rows.remove(row)
        if column in self.unused_columns:
            self.unused_columns.remove(column)

    def calculate_distance_with_expansions(self, g1: Galaxy, g2: Galaxy, expansion_coefficient: int = 2) -> int:
        if g1 not in self.galaxies or g2 not in self.galaxies:
            return -1
        distance = calculate_manhattan_distance(g1, g2)
        row_expansion = self.count_expanded_rows(*sorted([g1[0], g2[0]])) * (expansion_coefficient - 1)
        column_expansion = self.count_expanded_columns(*sorted([g1[1], g2[1]])) * (expansion_coefficient - 1)
        return distance + row_expansion + column_expansion

    def positions(self) -> list[Galaxy]:
        return self.galaxies

    def count_expanded_rows(self, start: int, end: int) -> int:
        # Count expanded rows between [start, end]
        return sum(map(lambda row: start <= row <= end, self.unused_rows))

    def count_expanded_columns(self, start: int, end: int) -> int:
        return sum(map(lambda col: start <= col <= end, self.unused_columns))


def find_galaxies_in_row(text: str, row_index: int) -> list[Galaxy]:
    return [(row_index, column_idx) for column_idx, _ in enumerate(text) if text[column_idx] == "#"]


def calculate_manhattan_distance(g1: Galaxy, g2: Galaxy) -> int:
    g1_row, g1_column = g1
    g2_row, g2_column = g2
    return abs(g1_row - g2_row) + abs(g1_column - g2_column)


def read_galaxies(lines: list[str]) -> GalaxyTracker:
    image_size = len(lines), len(lines[0])
    tracker = GalaxyTracker(initial_size=image_size)
    row = 0
    for line in lines:
        for galaxy in find_galaxies_in_row(line, row):
            tracker.track(galaxy)
        row += 1
    return tracker


def compute_distance_between_galaxies(tracker: GalaxyTracker, expansion_coefficient: int) -> int:
    galaxies = tracker.positions()
    return sum(starmap(partial(tracker.calculate_distance_with_expansions, expansion_coefficient=expansion_coefficient),
                       combinations(galaxies, r=2)))


with open("input") as f:
    galaxy_tracker = read_galaxies(f.readlines())
    print("----- Part one -----")
    print(f"Total distance between pairs of galaxies (expansion coefficient: 2): "
          f"{compute_distance_between_galaxies(tracker=galaxy_tracker, expansion_coefficient=2)}")
    print("----- Part two -----")
    print(f"Total distance between pairs of galaxies (expansion coefficient: 1e6): "
          f"{compute_distance_between_galaxies(tracker=galaxy_tracker, expansion_coefficient=int(1e6))}")
