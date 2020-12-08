from typing import List, Dict


def execute(program: List[Dict[str, int]]):
    visited_instructions = set()
    pc = 0
    acc = 0
    while pc not in visited_instructions:
        visited_instructions.add(pc)
        cmd = program[pc]
        if cmd['inst'] == "nop":
            pc += 1
        elif cmd['inst'] == "acc":
            acc += cmd['arg']
            pc += 1
        elif cmd['inst'] == "jmp":
            pc += cmd['arg']
    return acc


program = []
with open("input_8.txt", "r") as f:
    for line in f.readlines():
        cmd, arg = line.strip().split(" ")
        program.append({"inst": cmd, "arg": int(arg)})

print("Accumulator before the inifite loop is = {}".format(execute(program)))
