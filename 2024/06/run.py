from enum import Enum

Position = tuple[int, int]


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


with open("input", "r") as f:
    lines = list(map(str.strip, f.readlines()))

    start_pos: Position = (0, 0)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "^":
                start_pos = (row, col)
                break

    print(f"Found starting point: {start_pos}")

    def is_out(position: Position) -> bool:
        x, y = position
        return x < 0 or x >= len(lines) or y < 0 or y >= len(lines[0])

    def turn_right(direction: Direction) -> Direction:
        match direction:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    def get_line(start: Position, direction: Direction) -> list[tuple[str, Position]]:
        line = []
        current_pos = start
        while not is_out(current_pos):  # and get_char(current_pos) != "#":
            line.append((get_char(current_pos), current_pos))
            current_pos = move(current_pos, direction)
        return line

    def move(current: Position, direction: Direction) -> Position:
        x, y = current
        x += direction.value[0]
        y += direction.value[1]
        return (x, y)

    def get_char(position: Position) -> str:
        x, y = position
        return lines[x][y]

    current_pos = start_pos
    current_dir = Direction.UP
    visited = {}

    def plot_map() -> None:
        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                if (row, col) in visited:
                    print("X", end="")
                else:
                    print(c, end="")
            print("")
        input()

    def visit_position(position: Position, direction: Direction) -> None:
        if position in visited:
            visited[position].append(direction)
        else:
            visited[position] = [direction]

    num_obstacles = 0
    while not is_out(current_pos):
        visit_position(current_pos, current_dir)
        line = get_line(current_pos, current_dir)

        has_end = True
        for step in line:
            # plot_map()
            c, pos = step
            if c in [".", "^"]:
                # Test obstacle at pos!
                right_dir = turn_right(current_dir)
                right_line = get_line(current_pos, right_dir)
                could_be_obstacle = False
                # print("Right: ", right_line)
                current_step = current_pos
                for right_step in right_line:
                    c_step, pos_step = right_step
                    if c_step == "#":
                        break
                    elif c_step in [".", "^"] and pos_step in visited and right_dir in visited[pos_step]:
                        could_be_obstacle = True
                        break
                if could_be_obstacle:
                    print("Found obstacle!", pos)
                    num_obstacles += 1


                visit_position(pos, current_dir)
                current_pos = pos
            elif c == "#":
                has_end = False
                current_dir = turn_right(current_dir)
                break

        if has_end:
            break

    # 5318
    print(len(visited))
    # 543 - to low!
    print("Num obstacles", num_obstacles)
