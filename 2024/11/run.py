with open("input", "r") as f:
    content = list(map(int, f.read().strip().split()))
    print(content)

    # Remember transformations, there are not many of them!
    transformations = {}

    def transform_number(number: int) -> list[int]:
        if number in transformations:
            return transformations[number]

        if number == 0:
            transformations[0] = [1]
            return [1]
        number_str = str(number)
        number_digits = len(number_str)
        if number_digits % 2 == 0:
            middle = int(number_digits / 2)
            transformations[number] = [
                int(number_str[:middle]),
                int(number_str[middle:]),
            ]
            return [int(number_str[:middle]), int(number_str[middle:])]
        transformations[number] = [number * 2024]
        return [number * 2024]

    iteration = 0
    stones = content

    def increase_hist(hist, stone, increment=1):
        if stone in hist:
            hist[stone] += increment
        else:
            hist[stone] = increment

    total_hist = {}
    iteration_hist = {}
    for stone in stones:
        increase_hist(iteration_hist, stone)
    total_hist.update(iteration_hist)

    total_sum = sum(iteration_hist.values())
    while iteration < 75:
        new_stones = []
        print(f"Iteration {iteration}")  #: {stones}")
        next_iteration_hist = {}
        for stone, freq in iteration_hist.items():
            very_new_stones = transform_number(stone)
            for new_stone in very_new_stones:
                increase_hist(next_iteration_hist, new_stone, increment=freq)
        print(iteration_hist)
        print(len(next_iteration_hist))
        iteration_hist = next_iteration_hist
        total_sum = sum(next_iteration_hist.values())
        # input()
        # for stone in stones:
        #     new_stones.extend(transform_number(stone))
        stones = new_stones
        iteration += 1
    # 198075 after 25 iterations
    print(f"Num of stones after {iteration} iterations: {len(stones)}")
    # print(sum(iteration_hist.values()), len(iteration_hist))
    print("sum=",total_sum)
    # print(transformations, len(transformations))
