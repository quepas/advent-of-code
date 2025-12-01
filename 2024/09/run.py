from itertools import repeat

def find_space_bounds(elements) -> list:
    left_idx = 0
    bounds = []
    while left_idx < len(elements):
        while left_idx < len(elements) and  elements[left_idx] != -1:
            left_idx += 1
        if left_idx >= len(elements):
            break
        right_idx = left_idx + 1
        while right_idx < len(elements) and elements[right_idx] == -1:
            right_idx += 1
        if left_idx < right_idx:
            bounds.append((left_idx, right_idx))
        left_idx = right_idx
    return bounds

with open("input", "r") as f:
    line = f.read().strip()
    print(line)

    file_lengths = list(map(int, line[::2]))
    free_space = list(map(int, line[1::2])) + [0]  # Add nothing at the end
    memory = ""

    memory_blocks = {}

    # Prepare memory layout
    current_id = 0
    memory_ids = []
    memory_bounds = []  # end not inclusive
    space_bounds = []
    for length, space in zip(file_lengths, free_space):
        memory += "".join(repeat(str(length), length))
        start_idx = len(memory_ids)
        memory_ids.extend(repeat(current_id, length))
        end_idx = len(memory_ids)
        memory_bounds.append((start_idx, end_idx))
        if space > 0:
            memory += "".join(repeat(".", space))
            start_idx = len(memory_ids)
            memory_ids.extend(repeat(-1, space))
            end_idx = len(memory_ids)
            space_bounds.append((start_idx, end_idx))
        current_id += 1

    left_idx = 0
    print(memory)
    print(memory_ids)
    print(memory_bounds)
    print("Orig space_bounds: ", space_bounds)
    print("Found space bounds: ", find_space_bounds(memory_ids))
    right_idx = len(memory_ids) - 1
    # print(memory)
    compacted_memory = list(memory_ids)
    # block-based compaction
    while left_idx < right_idx:
        if compacted_memory[left_idx] == -1 and compacted_memory[right_idx] != -1:
            compacted_memory[left_idx] = compacted_memory[right_idx]
            compacted_memory[right_idx] = -1
        while compacted_memory[left_idx] != -1:
            left_idx += 1
        while compacted_memory[right_idx] == -1:
            right_idx -= 1
        # print(left_idx, right_idx)
        # print("".join(compacted_memory))
        # left_idx += 1
        # right_idx -= 1

    # file-based compaction
    print(memory_ids)
    for file_id, file in enumerate(reversed(memory_bounds)):
        print(f"Working on file_id: {file_id}")
        file_size = file[1] - file[0]
        space_bounds = find_space_bounds(memory_ids)
        for space in space_bounds:
            # Free space can't be after the file
            if space[1] > file[0]:
                break
            space_size = space[1] - space[0]
            if space_size >= file_size:
                # print("Have space!", space, memory_ids[space[0]:space[1]], file,memory_ids[file[0]:file[1]])
                memory_ids[space[0]:space[0]+file_size] = memory_ids[file[0]:file[1]]
                memory_ids[file[0]:file[1]] = [-1]*file_size
                # Update space bounds
                break
        # print(memory_ids)


    print(memory_ids)

    # print("".join(compacted_memory))
    # left = "".join(repeat(" ", left_idx)) + "^"
    # print(left)
    checksum = 0
    for idx, num in enumerate(memory_ids):
        if num == -1:
            continue
        checksum += idx * int(num)
        print("checksum", checksum, "idx", idx, "num", num)
    # 90366588601 - too low
    print(checksum)
