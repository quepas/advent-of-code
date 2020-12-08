from typing import List, Dict


def execute_program(program: List[Dict[str, int]]):
    execution_trace = []
    pc = 0
    acc = 0
    while pc not in execution_trace and pc < len(program):
        execution_trace.append(pc)
        cmd = program[pc]
        if cmd['inst'] == "nop":
            pc += 1
        elif cmd['inst'] == "acc":
            acc += cmd['arg']
            pc += 1
        elif cmd['inst'] == "jmp":
            pc += cmd['arg']
    if pc == len(program):
        last_instruction = None
    else:
        last_instruction = program[pc]
    return acc, pc, last_instruction, execution_trace


program = []
with open("input_8.txt", "r") as f:
    for line in f.readlines():
        cmd, arg = line.strip().split(" ")
        program.append({"inst": cmd, "arg": int(arg)})

acc, pc, inst, trace = execute_program(program)  # Execute infinite program and check where it
print("Partial execution of an infinite program [acc: {}, steps: {}/{}, pc: {}, inst: {}]".format(acc, len(trace), len(program), pc, inst))

# Modify the program
for k in range(len(program)):
    new_program = program.copy()
    old_instruction = new_program[k]
    if old_instruction['inst'] == 'nop':
        new_program[k] = {"inst": "jmp", "arg": old_instruction['arg']}
    elif old_instruction['inst'] == "jmp":
        new_program[k] = {"inst": "nop", "arg": old_instruction['arg']}
    else:
        continue
    acc, pc, inst, trace = execute_program(new_program)  # Execute infinite program and check where it
    if pc == len(program):
        print("Execution of a modified program [acc: {}, steps: {}/{}, pc: {}, inst: {}]".format(acc, len(trace), len(new_program), pc, inst))
