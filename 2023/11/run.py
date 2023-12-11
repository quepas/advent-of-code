from functools import partial
from itertools import combinations, starmap

Galaxy = tuple[int, int]


class GalaxyTracker:
    """
    A simple tracker of galaxies which is capable of computing distance between galaxies in an expandable universe.
    The universe expansion is found by analysing which coordinates on x,y-axes haven't been used by galaxies.
    Then, each unused coordinate represents a single "line" of the universe expansion which is then multiplied
    by the rate of expansion (the expansion coefficient).
    """

    def __init__(self, initial_size: tuple[int, int]):
        self.galaxies: list[Galaxy] = []
        # We start with possible rows/columns, but each time we track a new galaxy, we remove its row/column
        self.unused_rows: list[int] = list(range(0, initial_size[0]))
        self.unused_columns: list[int] = list(range(0, initial_size[1]))

    def track(self, galaxy: Galaxy) -> None:
        """
        Track a single galaxy. Keep track of unused coordinates so far.
        """
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
        """
        Return all tracked so far galaxies
        """
        return self.galaxies

    def count_expanded_rows(self, start: int, end: int) -> int:
        """
        Count number of expanded rows between [start, end] positions
        """
        return sum(map(lambda row: start <= row <= end, self.unused_rows))

    def count_expanded_columns(self, start: int, end: int) -> int:
        """
        Count number of expanded columns between [start, end] positions
        """
        return sum(map(lambda col: start <= col <= end, self.unused_columns))


def find_galaxies_in_row(text: str, row_index: int) -> list[Galaxy]:
    """
    Convert galaxy position in a row to a full (row, column) position withing an universe image
    """
    return [(row_index, column_idx) for column_idx, _ in enumerate(text) if text[column_idx] == "#"]


def calculate_manhattan_distance(g1: Galaxy, g2: Galaxy) -> int:
    """
    Compute manhattan distance of two galaxies (sum of absolute differences between corresponding axes)
    URL: https://en.wikipedia.org/wiki/Taxicab_geometry
    """
    g1_row, g1_column = g1
    g2_row, g2_column = g2
    return abs(g1_row - g2_row) + abs(g1_column - g2_column)


def read_galaxies(lines: list[str]) -> GalaxyTracker:
    """
    Read galaxies by parsing the "image" file line-by-line.
    Each time a galaxy is found it is tracked by the Galaxy Tracker class.
    """
    image_size = len(lines), len(lines[0])
    tracker = GalaxyTracker(initial_size=image_size)
    row = 0
    for line in lines:
        for galaxy in find_galaxies_in_row(line, row):
            tracker.track(galaxy)
        row += 1
    return tracker


def compute_distance_between_galaxies(tracker: GalaxyTracker, expansion_coefficient: int) -> int:
    """
    Compute distance of all combinations of galaxy pairs by taking into account the universe expansion
    (given by expansion_coefficient)
    """
    galaxies = tracker.positions()
    return sum(  # Sum the distances!
        # Calculate distance of each pair of galaxies
        starmap(partial(tracker.calculate_distance_with_expansions, expansion_coefficient=expansion_coefficient),
                # Creates combinations of galaxy pairs
                combinations(galaxies, r=2)))


with open("input_test_1") as f:
    galaxy_tracker = read_galaxies(f.readlines())
    print("----- Part one -----")
    print(f"Total distance between pairs of galaxies (expansion coefficient: 2): "
          f"{compute_distance_between_galaxies(tracker=galaxy_tracker, expansion_coefficient=2)}")
    print("----- Part two -----")
    print(f"Total distance between pairs of galaxies (expansion coefficient: 1e6): "
          f"{compute_distance_between_galaxies(tracker=galaxy_tracker, expansion_coefficient=int(1e6))}")
