import aiohttp, ujson as json
from async_lru import alru_cache
from enum import Enum
from LoL_Scrapper import private

class region(Enum):
    na1 = "1"
    euw1 = "2"
    kr = "3"
    eun1 = "4"
    br1 = "5"
    las = "6"
    la2 = "7"
    oc1 = "8"
    ru = "9"
    tr1 = "10"
    jp1 = "11"
    world = "12"

class tiers(Enum):
    challenger = "1"
    master = "2"
    diamond = "3"
    platinum = "4"
    gold = "5"
    silver = "6"
    bronze = "7"
    overall = "8"
    platinum_plus = "10"
    diamond_plus = "11"
    diamond_2_plus = "12"
    grandmaster = "13"
    master_plus = "14"
    iron = "15"

class positions(Enum):
    jungle = "1"
    support = "2"
    adc = "3"
    top = "4"
    mid = "5"
    none = "6"

class data(Enum):
    perks = 0
    summoner_spells = 1
    start_items = 2
    mythic_and_core = 3
    abilities = 4
    other_items = 5
    shards = 8

class stats(Enum):
    wins = 0
    matches = 1
    rank = 2
    total_rank = 3
    bans = 10
    total_matches = 11
    real_matches = 13

class __stats__():
    def __init__(self):
        self

    @alru_cache(maxsize=1)
    async def championid(name):
        champName = await private.champnamecleaner(name=name)
        ddragon_version = (await private.ddragondata())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/champion.json") as champJson:
                championId = json.loads(await champJson.text())["data"][f"{champName}"]["key"]
        return championId

    @alru_cache(maxsize=1)
    async def stats(name):
        statsVersion = '1.1'
        overviewVersion = '1.5.0'
        baseOverviewUrl = 'https://stats2.u.gg/lol'
        gameMode = "ranked_solo_5x5"
        ddragon_version = (await private.ddragondata())
        lolVersion = ddragon_version.split(".")
        championId = await __stats__.championid(name=name)
        uggLoLVersion = lolVersion[0] + '_' + lolVersion[1]
        async with aiohttp.ClientSession() as session2:
            async with session2.get(f"{baseOverviewUrl}/{statsVersion}/overview/{uggLoLVersion}/{gameMode}/{championId}/{overviewVersion}.json") as URL:
                print(f"{baseOverviewUrl}/{statsVersion}/overview/{uggLoLVersion}/{gameMode}/{championId}/{overviewVersion}.json")
                page = json.loads(await URL.text())
        return page

    @alru_cache(maxsize=1)
    async def rankings(name):
        statsVersion = '1.5'
        overviewVersion = '1.5.0'
        baseOverviewUrl = 'https://stats2.u.gg/lol'
        gameMode = "ranked_solo_5x5"
        ddragon_version = (await private.ddragondata())
        championId = await __stats__.championid(name=name)
        lolVersion = ddragon_version.split(".")
        uggLoLVersion = lolVersion[0] + '_' + lolVersion[1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{baseOverviewUrl}/{statsVersion}/rankings/{uggLoLVersion}/{gameMode}/{championId}/{overviewVersion}.json") as URL:
                page = json.loads(await URL.text())
        return page

class ugg():
    def __init__(self):
        self

    #Take the number of picks, bans, etc, divied by the number of matches, rounded to the 3nd place, multipled by 100
    async def winrate(name, role: str, ranks='platinum_plus', regions='world'):
        json = (await __stats__.rankings(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value]
        wr: float = json[stats.wins.value] / json[stats.matches.value]
        return f"{str(round(wr * 100, 1))}%"

    async def rank(name, role: str, ranks='platinum_plus', regions='world'):
        json = (await __stats__.rankings(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value]
        rank  = json[stats.rank.value]
        return rank[2].text

    async def totalmatches(name, role: str, ranks='platinum_plus', regions='world'):
        pr = (await __stats__.rankings(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value]
        return int(round(pr[stats.total_matches.value], 0))

    async def pickrate(name, role: str, ranks='platinum_plus', regions='world'):
        json = (await __stats__.rankings(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value]
        pr = json[stats.matches.value] / json[stats.total_matches.value]
        return f"{str(round(pr * 100, 1))}%"

    async def banrate(name, role: str, ranks='platinum_plus', regions='world'): 
        json = (await __stats__.rankings(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value]
        br = json[stats.bans.value] / json[stats.total_matches.value]
        return f"{str(round(br * 100, 1))}%"

    @alru_cache(maxsize=1)
    async def runes(name, role: str, ranks='platinum_plus', regions='world'):
        ddragon_version = (await private.ddragondata())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/runesReforged.json") as dd_runes:
                runes_json = json.loads(await dd_runes.text())

        trees = (await __stats__.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.perks.value]
        rune_ids = trees[4]
        runes_1 = []
        runes_2 = []

        for tree in runes_json: 
            if tree['id'] == trees[2]:
                [runes_1.insert(slots_pos, rune_data['name']) for slots_pos, slots in enumerate(tree["slots"]) for rune_data in slots['runes'] for y in range(6) if rune_ids[y] == rune_data['id']]
            elif tree['id'] == trees[3]:
                [runes_2.insert(slots_pos - 1, rune_data['name']) for slots_pos, slots in enumerate(tree["slots"]) for rune_data in slots['runes'] for y in range(6) if rune_ids[y] == rune_data['id']]

        runes = runes_1 + runes_2
        return runes

    @alru_cache(maxsize=1)
    async def items(name, role: str, ranks='platinum_plus', regions='world'):
        ddragon_version = (await private.ddragondata())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/item.json") as dd_items:
                items_json = json.loads(await dd_items.text())

        items = (await __stats__.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0]
        start = []
        core = []
        last_set = set()

        print(items[2])
        for z in items_json['data']:\
            #These can be empty. This is the fault of U.GG, not me.
            [start.append(items_json['data'][z]['name']) for i in items[data.start_items.value][2] if str(i) == z]
            [core.append(items_json['data'][z]['name']) for i in items[data.mythic_and_core.value][2] if str(i) == z]
            {last_set.add(items_json['data'][z]['name']) for x in range(3) for y in range(len(items[data.other_items.value][x])) if str(items[data.other_items.value][x][y][0]) == z}

        Items = [start, core, list(last_set)]
        return Items

    @alru_cache(maxsize=1)
    async def shards(name, role: str, ranks='platinum_plus', regions='world'):
        stat_shard_id = (await __stats__.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.shards.value][2]
        stat_shard = []
        for s in stat_shard_id:
            match s:
                case "5001": stat_shard.append("Health")
                case "5008": stat_shard.append("Adaptive Force")
                case "5007": stat_shard.append("Ability Haste")
                case "5002": stat_shard.append("Armor")
                case "5005": stat_shard.append("Attack Speed")
                case "5003": stat_shard.append("Magic Resist")
        return stat_shard

    @alru_cache(maxsize=5)
    async def abilities(name, role: str, ranks='platinum_plus', regions='world'):
        abilities = (await __stats__.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.abilities.value][2]
        return abilities