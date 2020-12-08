with open("input_1.txt", "r") as f:
    numbers = list(map(lambda elem: int(elem), f.read().split("\n")))
    f.close()

    # First part
    for k in range(len(numbers) - 1):
        for l in range(k+1, len(numbers)):
            a = numbers[k]
            b = numbers[l]
            if a + b == 2020:
                print('Found numbers: {} and {}'.format(a, b))
                print('Result is {} x {} = {}'.format(a, b, a * b))
                break

    # Second part
    for k in range(len(numbers) - 2):
        for l in range(k+1, len(numbers) - 1):
            for m in range(l+1, len(numbers)):
                a = numbers[k]
                b = numbers[l]
                c = numbers[m]
                if a + b + c == 2020:
                    print('Found numbers: {}, {}, and {}'.format(a, b, c))
                    print('Result is {} x {} x {} = {}'.format(a, b, c, a * b * c))
                    break
