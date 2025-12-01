from collections import deque
from itertools import product

Position = tuple[int, int]

with open("input", "r") as f:
    lines = list(map(str.strip, f.readlines()))
    print(lines)
    to_visit = list(product(range(len(lines)), range(len(lines[0]))))
    print(to_visit)

    def get_plant(position: Position) -> str:
        row, col = position
        return lines[row][col]

    def in_map(position: Position) -> bool:
        row, col = position
        return 0 <= row < len(lines) and 0 <= col < len(lines[0])

    def candidates_around(position: Position) -> list[Position]:
        row, col = position
        return [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]

    def candidates_corner(
        position: Position,
    ) -> list[tuple[Position, Position, Position]]:
        row, col = position
        return [
            # Top-right
            ((row + 1, col), (row + 1, col + 1), (row, col + 1)),
            # Bottom-right
            ((row - 1, col), (row - 1, col + 1), (row, col + 1)),
            # Bottom-left
            ((row - 1, col), (row - 1, col - 1), (row, col - 1)),
            # Top-left
            ((row + 1, col), (row + 1, col - 1), (row, col - 1)),
        ]

    def explore_around(position: Position, plant: str) -> list[Position]:
        """Explore only valid position withing the map, not visited, and with given plant"""
        candidates = candidates_around(position)
        return list(
            filter(
                lambda pos: in_map(pos) and pos in to_visit and get_plant(pos) == plant,
                candidates,
            )
        )

    def area(positions: list[Position]) -> int:
        return len(positions)

    def perimeter(positions: list[Position]) -> int:
        permieter = 0
        for position in positions:
            candidates = candidates_around(position)
            num_shared = len(set(candidates).intersection(positions))
            permieter += 4 - num_shared
        return permieter

    def sides(positions: list[Position]) -> int:
        sides = 0
        for position in positions:
            for cand1, cand2, cand3 in candidates_corner(position):
                """
                External corners:
                      EE
                   ooooE
                E - test not part of region, o - region
                """
                if cand1 not in positions and cand2 not in positions and cand3 not in positions:
                    sides += 1
                """
                Reversed corners
                     o
                     RT
                   oooRo
                R - test part of region, T - test not part of region, o - region
                """
                if cand1 in positions and cand2 not in positions and cand3 in positions:
                    sides += 1
                """
                Touching corners
                     o
                     xR
                   ooTxo
                R - test part of region, T - test not part of region, o - region
                """
                if cand1 not in positions and cand2 in positions and cand3 not in positions:
                    sides += 1
        return sides

    def explore_region(start: Position) -> list[Position]:
        plant = get_plant(start)
        print(f">> Exploring: {start} with plant: {plant}")
        Q = deque([start])
        region = []
        while Q:
            current = Q.popleft()
            if current not in to_visit:
                continue
            to_visit.remove(current)
            region.append(current)
            Q.extend(explore_around(current, plant))
        return region

    total_perimeter_price = 0
    total_sides_price = 0
    while to_visit:
        start = to_visit[0]
        region = explore_region(start)
        area_size = area(region)
        perimeter_size = perimeter(region)
        sides_size = sides(region)
        total_perimeter_price += area_size * perimeter_size
        total_sides_price += area_size * sides_size
        print(
            "Region size:",
            area(region),
            "; permieter:",
            perimeter(region),
            "; sides:",
            sides(region),
        )
    print("Total permieter price:", total_perimeter_price, "; total sides price: ", total_sides_price)
