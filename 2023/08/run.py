from functools import reduce, partial


def parse_network_connection(line: str) -> tuple[str, tuple[str, str]]:
    """Parse single network connection of the form NODE_IN = (NODE_LEFT, NODE_RIGHT)"""
    return line[0:3], (line[7:10], line[12:15])


def parse_map(lines: list[str]) -> dict:
    return {
        "instruction": lines[0].strip(),
        "network": dict(map(parse_network_connection, lines[2:]))
    }


def gcd(a: int, b: int) -> int:
    """
    Compute Greatest Common Divisor (GCD) of two integers with Euclidean algorithm
    URL: https://en.wikipedia.org/wiki/Euclidean_algorithm#Implementations
    """
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def least_common_multiple(numbers: list[int]) -> int:
    """
    Least common multiple using GCD!
    URL: https://en.wikipedia.org/wiki/Least_common_multiple#Using_the_greatest_common_divisor
    """
    return reduce(lambda a, b: int(abs(a * b) / gcd(a, b)), numbers)


def find_num_path_steps(start_node: str, desert_map: dict, z_ending: bool = False) -> int:
    instruction_counter = 0
    node = start_node
    # Follow map until we stumble upon the end node (ZZZ or **Z)
    while not node.endswith("Z") if z_ending else node != "ZZZ":
        instruction = desert_map["instruction"][instruction_counter % len(desert_map["instruction"])]
        network_direction = desert_map["network"][node]
        node = network_direction[0] if instruction == "L" else network_direction[1]
        instruction_counter += 1
    return instruction_counter


with open("input") as f:
    desert_map = parse_map(f.readlines())
    print("----- Part one -----")
    required_steps = find_num_path_steps('AAA', desert_map)
    print(f"Required number of steps (AAA -> ZZZ): {required_steps}")
    print("----- Part two -----")
    start_nodes = list(filter(lambda node: node.endswith("A"), desert_map["network"].keys()))
    # Instead of following all the paths simultaneously ad infinitum,
    # We assume that in each path, there is only one ending node **Z, then the moment when
    # all paths finish at the same time is the least common multiple of their respective steps
    required_steps = least_common_multiple(
        list(map(partial(find_num_path_steps, desert_map=desert_map, z_ending=True), start_nodes)))
    print(f"Required number of steps for all simultaneous paths (**A -> **Z): {required_steps}")
