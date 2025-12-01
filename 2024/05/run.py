with open("input", "r") as f:
    lines = f.readlines()
    page_ordering = []
    before_ordering = {}
    after_ordering = {}
    page_updates = []
    for line in lines:
        if "|" in line:
            nums = list(map(int, line.strip().split("|")))
            before, after = nums
            if before not in before_ordering:
                before_ordering[before] = [after]
            else:
                before_ordering[before].append(after)
            if after not in after_ordering:
                after_ordering[after] = [before]
            else:
                after_ordering[after].append(before)
            page_ordering.append(nums)
        if "," in line:
            page_updates.append(list(map(int, line.strip().split(","))))

    print("before", before_ordering)
    print("after", after_ordering)
    right_order_sum = 0
    wrong_order_sum = 0
    for update in page_updates:
        print("testing", update)
        right_order = True
        # Testing before
        for idx, page in enumerate(update):
            if page in before_ordering:
                for before in before_ordering[page]:
                    if before in update and update.index(before) < idx:
                        # print("found before!")
                        right_order = False
                        break
            if page in after_ordering:
                for after in after_ordering[page]:
                    if after in update and update.index(after) > idx:
                        # print("found after!")
                        right_order = False
                        break
        if right_order:
            median_elem = update[int(len(update)/2)]
            print("Right order! Median:", median_elem)
            right_order_sum += median_elem
        else:
            # Try fixing the order
            reconstructed = []
            for page in update:
                if page in before_ordering:
                    all_ok = True
                    for before in before_ordering[page]:
                        if before in reconstructed:
                            all_ok = False
                    if all_ok:
                        reconstructed.append(page)
                    else:
                        # Find first correct place
                        placement = -1
                        for placed in reversed(reconstructed):
                            if placed in after_
                        reconstructed.insert(-1, page)
                print(page)
            print("reconstructed", reconstructed)
            median_elem = reconstructed[int(len(reconstructed)/2)]
            print("Wrong order! Median:", median_elem)
            wrong_order_sum += median_elem
    print("Right Sum:", right_order_sum)
    # Too high: 6412
    print("Wrong Sum:", wrong_order_sum)
