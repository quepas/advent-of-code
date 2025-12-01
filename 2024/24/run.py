from collections import deque


def parse_gates(content: str) -> tuple[dict, list[tuple]]:
    raw_inputs, raw_gates = content.strip().split("\n\n")
    inputs = {}
    gates = []
    for input in raw_inputs.split("\n"):
        gate, value = input.split(":")
        value = int(value)
        inputs[gate] = value
    for line in raw_gates.split("\n"):
        x1, op, x2, _, out = line.strip().split()
        gates.append((x1, op, x2, out))
    return inputs, gates


def collect_number(inputs: dict, register: str = "z") -> int:
    z_keys = list(
        reversed(sorted(filter(lambda x: x.startswith(register), inputs.keys())))
    )
    values = "".join(map(lambda k: str(inputs[k]), z_keys))
    return int(values, 2)


with open("input_test3", "r") as f:
    inputs, gates = parse_gates(f.read())

    Q = deque(gates)

    while Q:
        current = Q.popleft()
        print(current)
        x1, op, x2, out = current

        if x1 in inputs and x2 in inputs:
            match op:
                case "AND":
                    inputs[out] = int(inputs[x1] and inputs[x2])
                case "OR":
                    inputs[out] = int(inputs[x1] or inputs[x2])
                case "XOR":
                    inputs[out] = int(
                        (inputs[x1] and not inputs[x2])
                        or (not inputs[x1] and inputs[x2])
                    )
        else:
            # Leave it for later
            Q.append(current)
    print("X:", collect_number(inputs, "x"))
    print("Y:", collect_number(inputs, "y"))
    print("Result number:", collect_number(inputs))
