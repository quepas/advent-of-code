from itertools import pairwise

Position = tuple[int, int]


MOVES = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


class Map:

    def __init__(self, map_content: str, make_wider: bool = False) -> None:
        if make_wider:
            map_content = map_content.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.") 
        self.tiles = list(map(list, map_content.split()))
        self.robot = self.__find_tiles("@")[0]

    def __repr__(self) -> str:
        return "\n".join(map(lambda row: "".join(row), self.tiles))

    def __contains__(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < len(self.tiles) and 0 <= col < len(self.tiles[0])

    def __getitem__(self, position: Position) -> str:
        row, col = position
        return self.tiles[row][col]

    def __setitem__(self, position: Position, value: str) -> None:
        row, col = position
        self.tiles[row][col] = value

    def __find_tiles(self, value: str) -> list[Position]:
        tiles = []
        for row, line in enumerate(self.tiles):
            for col, char in enumerate(line):
                if char == value:
                    tiles.append((row, col))
        return tiles

    def swap_tiles(self, source: Position, target: Position) -> None:
        temp = self[source]
        self[source] = self[target]
        self[target] = temp
        self.robot = self.__find_tiles("@")[0]

    def get_boxes(self) -> list[Position]:
        return self.__find_tiles("O")

    def move_robot(self, move_sign: str) -> None:
        move = MOVES[move_sign]

        def collect_moves(position: Position) -> list[Position]:
            if self[position] == "#":
                return []
            if self[position] == ".":
                return [position]
            next_position = add(position, move)
            if result := collect_moves(next_position):
                return [position, *result]
        
        for m in collect_moves(self.robot)[1:]:
            print(m)
            self[m] = "@"
            self[self.robot] = "."
            self.robot = m
        input()

def parse_map(content: str) -> tuple[Map, str]:
    map_content, move_content = content.split("\n\n")
    moves = "".join(move_content.split())

    m = Map(map_content, make_wider=False)
    return m, moves


def add(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


with open("input_test1", "r") as f:
    m, map_moves = parse_map(f.read())
    print("Initial state. Start: ", m.robot)
    print(m)
    for move_sign in map_moves:
        move = MOVES[move_sign]
        next_pos = add(m.robot, move)
        candidate = m[next_pos]
        print(f"Move: {move_sign}")  # tile: {candidate}")
        if candidate == "#":
            pass
        elif candidate == ".":
            m.move_robot(move_sign)
        elif candidate in ["O", "[", "]"]:
            push_positions = [m.robot]
            current = next_pos
            while m[current] not in [".", "#"]:
                push_positions.append(current)
                current = add(current, move)
            print(push_positions)
            if m[current] == "#":
                # No space for the move
                continue
            elif m[current] == ".":
                push_positions.append(current)
                print("Perform!", push_positions)
                for pos1, pos2 in pairwise(reversed(push_positions)):
                    m.swap_tiles(pos1, pos2)
            # Check if possible to move stuff!
        # input()
        print(m)

sum_gps = 0
for box in m.get_boxes():
    sum_gps += 100 * box[0] + box[1]

print("Sum GPS", sum_gps)
        # input()
