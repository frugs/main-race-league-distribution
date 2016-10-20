import pprint


distribution = {
    'bronze 1': 110,
    'bronze 2': 94,
    'bronze 3': 163,
    'diamond 1': 1319,
    'diamond 2': 807,
    'diamond 3': 497,
    'gold 1': 439,
    'gold 2': 464,
    'gold 3': 476,
    'grandmaster': 0,
    'master 1': 402,
    'master 2': 204,
    'master 3': 381,
    'platinum 1': 554,
    'platinum 2': 479,
    'platinum 3': 432,
    'silver 1': 357,
    'silver 2': 383,
    'silver 3': 515}

simplified_league_names = {
    "bronze",
    "silver",
    "gold",
    "platinum",
    "diamond",
    "master",
    "grandmaster"
}

total_pop = sum(distribution.values())

proportions = dict(zip(distribution.keys(), ["{:1.2f}%".format(x * 100 / total_pop) for x in distribution.values()]))

simplified_distribution = dict(zip(simplified_league_names,
                                   map(lambda name: sum([pop for tier, pop in distribution.items() if tier.startswith(name)]),
                                       simplified_league_names)))

simplified_proportions = dict(zip(simplified_distribution.keys(), ["{:1.2f}%".format(x * 100 / total_pop) for x in simplified_distribution.values()]))

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(simplified_proportions)