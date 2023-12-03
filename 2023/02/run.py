def parse_game(line: str) -> dict:
    chunks = line.split(":")
    game = int(chunks[0].split(" ")[1])
    d = {
        "id": game,
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for s in chunks[1].split(";"):
        for cubes in s.split(","):
            num, color = cubes.strip().split(" ")
            d[color] = max(d[color], int(num))
    return d

max_red = 12
max_green = 13
max_blue = 14

id_sum = 0
id_prod_sum = 0
with open("input", "r") as f:
    for line in f.readlines():
        game = parse_game(line)
        if game["red"] <= max_red and game["green"] <= max_green and game["blue"] <= max_blue:
            id_sum += game["id"]
        game_prod = game['red']*game['blue']*game['green']
        print(f"Game power {game['id']}: {game_prod}")
        id_prod_sum += game_prod
print(f"ID sum: {id_sum}")
print(f"ID prod sum: {id_prod_sum}")

