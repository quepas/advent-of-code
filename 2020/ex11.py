seats = []


def copy_seats(seats):
    new_seats = []
    for row in seats:
        new_seats.append(row.copy())
    return new_seats


def count_occupied(seats):
    occupied = 0
    for row in seats:
        occupied += row.count('#')
    return occupied


def apply_rules_policy_1(in_seats, height, width):
    num_changes = 0
    seats = copy_seats(in_seats)
    for row_idx in range(height):
        for col_idx in range(width):
            seat = in_seats[row_idx][col_idx]
            elements = find_adjacent_elements(in_seats, row_idx, col_idx, height, width)
            # If empty L and no occupied
            if seat == 'L' and elements.count('#') == 0:
                seats[row_idx][col_idx] = '#'
                num_changes += 1
            if seat == '#' and elements.count('#') >= 4:
                seats[row_idx][col_idx] = 'L'
                num_changes += 1
    return num_changes, seats


def apply_rules_policy_2(in_seats, height, width):
    num_changes = 0
    seats = copy_seats(in_seats)
    for row_idx in range(height):
        for col_idx in range(width):
            seat = in_seats[row_idx][col_idx]
            # TODO: see here in a direction!
            elements = find_visible_elements(in_seats, row_idx, col_idx, height, width)
            # If empty L and no occupied
            if seat == 'L' and elements.count('#') == 0:
                seats[row_idx][col_idx] = '#'
                num_changes += 1
            if seat == '#' and elements.count('#') >= 5:
                seats[row_idx][col_idx] = 'L'
                num_changes += 1
    return num_changes, seats


def find_adjacent_elements(seats, x, y, height, width):
    indices = []
    elements = []
    for xs in range(x - 1, x + 2):
        for ys in range(y - 1, y + 2):
            # Skip the central element
            if xs == x and ys == y:
                continue
            if 0 <= xs < height and 0 <= ys < width and seats[xs][ys] != '.':
                indices.append((xs, ys))
                elements.append(seats[xs][ys])
    return elements


def find_visible_elements(seats, row, col, height, width):
    elements = []
    # Up
    for r in range(row - 1, 0, -1):
        if seats[r][col] != '.':
            print("Up")
            elements.append(seats[r][col])
            break
    # Down
    for r in range(row + 1, height):
        if seats[r][col] != '.':
            print("Down {}@{} = {}".format(r, col, seats[r][col]))
            elements.append(seats[r][col])
            break
    # Left
    for c in range(col - 1, 0, -1):
        if seats[row][c] != '.':
            print("Left")
            elements.append(seats[row][c])
            break
    # Right
    for c in range(col + 1, width):
        if seats[row][c] != '.':
            print("Right")
            elements.append(seats[row][c])
            break
    # Up-Left
    for i in range(1, min(row, col)):
        if seats[row-i][col-i] != '.':
            print("Up-Left")
            elements.append(seats[row-i][col-i])
            break
    # Down-right
    for i in range(1, min(height-row, width-col)): # TODO +1?
        if seats[row+i][col+i] != '.':
            print("Down-Right")
            elements.append(seats[row+i][col+i])
            break
    # Up-Right
    for i in range(1, min(row, width-col)):
        if seats[row-i][col+i] != '.':
            print("Up-Right")
            elements.append(seats[row-i][col+i])
            break
    # Down-left
    for i in range(1, min(height-row, col)):
        if seats[row+i][col-i] != '.':
            print("Down-Left")
            elements.append(seats[row+i][col-i])
            break
    return elements


with open("input_11_test.txt", "r") as f:
    for line in f.readlines():
        seats.append(list(line.strip()))
    height = len(seats)
    width = len(seats[0])

    # num_changes, seats = apply_rules_policy_1(seats, height, width)
    # while num_changes > 0:
    #     num_changes, seats = apply_rules_policy_1(seats, height, width)
    # print("Occupied seats in policy #1 = {}".format(count_occupied(seats)))

    num_changes, seats = apply_rules_policy_2(seats, height, width)
    while num_changes > 0:
        num_changes, seats = apply_rules_policy_2(seats, height, width)
        print("num_changes={}".format(num_changes))
    print("Occupied seats in policy #2 = {}".format(count_occupied(seats)))

    # A
    # print(find_visible_elements(seats, 4, 3, height, width))
    # B
    # print(find_visible_elements(seats, 1, 1, height, width))
    # C
    # print(find_visible_elements(seats, 3, 3, height, width))
