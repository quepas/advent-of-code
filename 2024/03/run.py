import re
with open("input", "r") as f:
    content = f.read()
    mul_inst = list(re.findall(r"(don't)|(do)|mul\((\d+),(\d+)\)", content))
    print(mul_inst)
    sum = 0
    skip = False
    for inst in mul_inst:
        dont, do, x, y = inst
        if do:
            skip = False
        elif dont:
            skip = True
        elif not skip:
            print("adding: ", inst)
            x, y = int(x), int(y)
            sum += x * y
    print("Sum=", sum)

