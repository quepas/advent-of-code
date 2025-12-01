secret_num = 1


def mix(num: int, secret_num: int) -> int:
    return num ^ secret_num


def prune(secret_num: int) -> int:
    return secret_num % 16777216


def next_number(secret_num: int) -> int:
    num = secret_num * 64
    secret_num = prune(mix(num, secret_num))
    num = int(secret_num / 32)
    secret_num = prune(mix(num, secret_num))
    num = secret_num * 2048
    secret_num = prune(mix(num, secret_num))
    return secret_num


def get_nth_numbers(secret_num: int, n: int) -> list[int]:
    results = []
    for i in range(n):
        secret_num = next_number(secret_num)
        results.append(secret_num)
    return results


def compute_changes(secret_num: int, buyer_nums: list[int]):
    prev = secret_num % 10
    banans = []
    diffs = []
    for num in buyer_nums:
        current = num % 10
        diffs.append(current - prev)
        banans.append(current)
        prev = current
    return diffs, banans

def find_banans_sales_points(changes, banans) -> dict:
    sales_points = {}
    for i in range(len(changes) - 4):
        seq = tuple(changes[i:(i+4)])
        banan = banans[i+3]
        if seq in sales_points:
            # TODO: or += ?
            sales_points[seq] += banan
        else:
            sales_points[seq] = banan
    return sales_points


with open("input", "r") as f:
    secret_nums = list(map(int, f.readlines()))
    sum_2000th_secret_nums = 0
    collection_sales_points = []
    unique_seq = set()
    banans_sums = {}
    for secret_num in secret_nums:
        buyer_nums = get_nth_numbers(secret_num, 2000)
        sum_2000th_secret_nums += buyer_nums[-1]
        changes, banans  = compute_changes(secret_num, buyer_nums)
        sales_points = find_banans_sales_points(changes, banans)
        collection_sales_points.append(sales_points)
        unique_seq.update(sales_points.keys())

    for seq in unique_seq:
        sum_banans = 0
        for sales_points in collection_sales_points:
            sum_banans += sales_points.get(seq, 0)
            banans_sums[seq] = sum_banans
    print("Sum of 2000th secret numbers: ", sum_2000th_secret_nums)
    print(max(banans_sums.values()))
    # 2084 - too low
    # 2077 - too low
    # 2277 - too high
