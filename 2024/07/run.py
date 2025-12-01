from itertools import product, repeat

def parse_line(line) -> list[int]:
    sum2, nums = line.split(":")
    nums = map(int, nums.strip().split()) 
    return [int(sum2), *nums]

def is_computable(sum2: int, nums: list[int]) -> bool:
    num_ops = len(nums) - 1
    for ops in product(*repeat("+*|", num_ops)):
        mn = [*nums]
        mops = [*ops]
        while len(mn) > 1:
            a = mn.pop(0)
            b = mn.pop(0)
            o = mops.pop(0)
             
            if o == "+":
                t = a + b
                mn.insert(0, t)
            elif o == "*":
                t = a * b
                mn.insert(0, t)
            elif o == "|":
                t = int(str(a)+str(b))
                mn.insert(0, t)
        acc = mn[0]
        # acc = nums[0] 
        # for idx, op in enumerate(ops):
        #     if op == "+":
        #         acc += nums[idx+1]
        #     elif op == "*":
        #         acc *= nums[idx+1]
        if acc == sum2:
            return True
    return False


with open("input", "r") as f:
    lines = map(parse_line, f.readlines())
    total_sum = 0
    for line in lines:
        sum2, nums = line[0], line[1:]
        if is_computable(sum2, nums):
            print("True expr: ", line)
            total_sum += sum2
    print("Total sum:", total_sum)
