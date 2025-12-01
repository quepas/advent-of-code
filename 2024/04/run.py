Position = tuple[int, int]


with open("input", "r") as f:
    lines = list(map(str.strip, f.readlines()))

    sum = 0
    for row in range(len(lines)):
        for col in range(len(lines[0])):
            if row > 0 and row < len(lines) - 1 and col > 0 and col < len(lines[0])-1 and lines[row][col] == "A":
                top_left = lines[row-1][col-1]
                top_right = lines[row-1][col+1]
                bottom_left = lines[row+1][col-1]
                bottom_right = lines[row+1][col+1]
                def mors(c) -> bool:
                    return c in ["M", "S"]
                if mors(top_left) and mors(bottom_right) and top_left != bottom_right \
                    and mors(top_right) and mors(bottom_left) and top_right != bottom_left: 
                        sum += 1
    print(sum)
    # print(lines)
    # sum = 0
    # for line in lines:
    #     sum += line.count("XMAS")
    #     sum += line.count("SAMX")
    # for col in range(len(lines[0])):
    #     line = "".join([l[col] for l in lines])
    #     print(line)
    #     sum += line.count("XMAS")
    #     sum += line.count("SAMX")
    # # diagonals \
    # for row in range(len(lines)-3):
    #     new_lines = [lines[row][:-3]]
    #     new_lines.append(lines[row+1][1:-2])
    #     new_lines.append(lines[row+2][2:-1])
    #     new_lines.append(lines[row+3][3:])
    #     for col in range(len(new_lines[0])):
    #         line = "".join([l[col] for l in new_lines])
    #         sum += line.count("XMAS")
    #         sum += line.count("SAMX")
    # # diagonals /
    # for row in range(len(lines)-3):
    #     new_lines = [lines[row][3:]]
    #     new_lines.append(lines[row+1][2:-1])
    #     new_lines.append(lines[row+2][1:-2])
    #     new_lines.append(lines[row+3][0:-3])
    #     for col in range(len(new_lines[0])):
    #         line = "".join([l[col] for l in new_lines])
    #         sum += line.count("XMAS")
    #         sum += line.count("SAMX")
    #     print(new_lines)
    # print("sum=", sum)
