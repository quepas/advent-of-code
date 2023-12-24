from operator import itemgetter


def parse_single_game(line: str) -> dict:
    """
    Parse single game into a dictionary with a game id and maximal number of colored cubes in the game (RGB).
    """
    chunks = line.split(":")
    game_id = int(chunks[0].split(" ")[1])
    d = {
        "id": game_id,
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for s in chunks[1].split(";"):
        for cubes in s.split(","):
            num, color = cubes.strip().split(" ")
            # Find maximal number of cubes of each color
            d[color] = max(d[color], int(num))
    return d


def is_possible_game(game: dict, avail_red=12, avail_green=13, avail_blue=14) -> bool:
    """
    Check if a game is possible to play given the available number of cubes (RGB)
    """
    return game["red"] <= avail_red and game["green"] <= avail_green and game["blue"] <= avail_blue


with open("input") as f:
    all_games = list(map(parse_single_game, f.readlines()))
    print("----- Part one -----")
    possible_games = list(filter(is_possible_game, all_games))
    sum_games_ids = sum(map(itemgetter("id"), possible_games))
    print(f"Sum of possible games: {sum_games_ids}")
    print("----- Part two -----")
    sum_power_set_of_cubes = sum(map(lambda game: game["red"] * game["blue"] * game["green"], all_games))
    print(f"Sum of the power of the minimum set of cubes: {sum_power_set_of_cubes}")
