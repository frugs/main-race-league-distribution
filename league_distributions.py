import os
import json
import urllib.request
import pprint

access_token = os.environ["BATTLE_NET_ACCESS_TOKEN"]
api_key = os.environ["BATTLE_NET_API_KEY"]

queue_id_1v1 = "201"

team_type_arranged = "0"

league_names = [
    "bronze",
    "silver",
    "gold",
    "platinum",
    "diamond",
    "master",
    "grandmaster"
]

leagues = enumerate(league_names)

tier_names = [
    "bronze 3",
    "bronze 2",
    "bronze 1",
    "silver 3",
    "silver 2",
    "silver 1",
    "gold 3",
    "gold 2",
    "gold 1",
    "platinum 3",
    "platinum 2",
    "platinum 1",
    "diamond 3",
    "diamond 2",
    "diamond 1",
    "master 3",
    "master 2",
    "master 1",
    "grandmaster",
]

races = [
    "PROTOSS",
    "TERRAN",
    "ZERG",
    "RANDOM"
]

game_data_resource = "https://us.api.battle.net/data/sc2"


def get_game_data(path: str) -> dict:
    response = urllib.request.urlopen(game_data_resource + path + "?access_token=" + access_token)
    response_str = response.read().decode('utf8')
    return json.loads(response_str)


def get_league_data(season: int, league_id: int) -> dict:
    path = "/league/{}/{}/{}/{}".format(season, queue_id_1v1, team_type_arranged, league_id)
    return get_game_data(path)


def get_current_season_data() -> dict:
    return get_game_data("/season/current")


def get_ladder_data(ladder_id: int) -> dict:
    path = "https://us.api.battle.net/sc2/ladder/{}?apikey={}".format(ladder_id, api_key)
    response = urllib.request.urlopen(path)
    response_str = response.read().decode('utf8')
    return json.loads(response_str)


players = {}

current_season_id = get_current_season_data()["id"]

for league_id, league_name in leagues:
    try:
        league_data = get_league_data(current_season_id, league_id)
    except:
        print("error retrieving league data for league: " + league_id)
        break

    for tier_data in league_data["tier"]:
        tier_index = tier_data["id"]
        tier_id = league_id * 3 + tier_index

        if "division" in tier_data:
            for division_data in tier_data["division"]:
                division_ladder_id = division_data["ladder_id"]

                try:
                    ladder_data = get_ladder_data(division_ladder_id)
                except:
                    print("error retrieving ladder data for ladder: " + division_ladder_id)
                    break

                for member_data in ladder_data["ladderMembers"]:
                    player_key = member_data["character"]["profilePath"]

                    if "favoriteRaceP1" in member_data:
                        preferred_race = member_data["favoriteRaceP1"]
                        race_index = races.index(preferred_race)

                        if player_key not in players:
                            players[player_key] = [0, 0, 0, 0]

                        players[player_key][race_index] = tier_id

league_distribution = dict(zip(tier_names, [0] * len(tier_names)))

for player_key, tiers in players.items():
    tier_name = tier_names[max(tiers)]
    league_distribution[tier_name] += 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(league_distribution)