def parse_register(line: str) -> int:
    return int(line.split(":")[1])


def parse_program(line: str) -> list[int]:
    raw_program = line.split(":")[1]
    return list(map(int, raw_program.split(",")))


instructions = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}

def print_state() -> None:
    print("\n-------- Computer state -------")
    print("Reg A:", register_a)
    print("Reg B:", register_b)
    print("Reg C:", register_c)

def run_program(reg_a: int, reg_b: int, reg_c: int, program: list[int]) -> list[int]:
    ip = 0
    register_a, register_b, register_c = reg_a, reg_b, reg_c
    output = []
    def literal_operand(ip: int, program: list[int]) -> int:
        return program[ip]

    def combo_operand(ip: int, program: list[int]) -> int:
        value = program[ip]
        if 0 <= value <= 3:
            return value
        if value == 4:
            return register_a
        if value == 5:
            return register_b
        if value == 6:
            return register_c
        assert value != 7, "Combo operand can't be 7"
        return -1
    def division(ip, program) -> int:
        numerator = register_a
        arg = combo_operand(ip, program)
        denominator = 2 ** arg
        return int(numerator / denominator) # TODO: or % 8 ? 
    try:
        while ip < len(program):
            opcode = program[ip]
            ip += 1
            match instructions[opcode]:
                case "adv":
                    register_a = division(ip, program)
                    ip += 1
                case "bxl":
                    register_b = register_b ^ literal_operand(ip, program)
                    ip += 1
                case "bst":
                    register_b = combo_operand(ip, program) % 8
                    ip += 1
                case "jnz":
                    if register_a != 0:
                        ip = literal_operand(ip, program)
                case "bxc":
                    register_b = register_b ^ register_c
                    _ = literal_operand(ip, program)
                    ip += 1
                case "out":
                    arg = combo_operand(ip, program) % 8
                    ip += 1
                    output.append(arg)
                case "bdv":
                    register_b = division(ip, program)
                    ip += 1
                case "cdv":
                    register_c = division(ip, program)
                    ip += 1
    finally:
        return output


with open("input", "r") as f:
    lines = list(map(str.strip, f.readlines()))
    register_a = parse_register(lines[0])
    register_b = parse_register(lines[1])
    register_c = parse_register(lines[2])
    program = parse_program(lines[4])
    output = []
    print("Input program: ", program)
    print_state()
    try:
        # for i in range(int(1e15), int(1e16)):
        s = int(1e14)
        while True:
            i = int(input("Give reg_a: "))
            s += i
            output = run_program(s, register_b, register_c, program)
            print(s, ": ", output)
            if output == program:
                break
    finally:
        print_state()
        print("Output: ", ",".join(map(str, output)))
