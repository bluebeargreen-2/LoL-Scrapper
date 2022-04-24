import requests, re, asyncio, aiohttp, time, ujson as json
from async_lru import alru_cache
from bs4 import BeautifulSoup
from enum import Enum
from aiohttp import web
        
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

class stats():
    def __init__(self):
        self
        
    @alru_cache(maxsize=1)
    async def ddragon_data():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://static.u.gg/assets/lol/riot_patch_update/prod/versions.json") as lolVersion:
                ddragon_version = json.loads(await lolVersion.text())[0]

        return ddragon_version
    
    @alru_cache(maxsize=1)
    async def stats(name):
        statsVersion = '1.1'
        overviewVersion = '1.5.0'
        baseOverviewUrl = 'https://stats2.u.gg/lol'
        gameMode = "ranked_solo_5x5"
        ddragon_version = (await stats.ddragon_data())
        lolVersion = ddragon_version.split(".")
        champName = re.sub(r'\W+', '', name.lower().title().strip())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/champion.json") as champJson:
                championId = json.loads(await champJson.text())["data"][f"{champName}"]["key"]
        uggLoLVersion = lolVersion[0] + '_' + lolVersion[1]
    
        async with aiohttp.ClientSession() as session2:
            async with session2.get(f"{baseOverviewUrl}/{statsVersion}/overview/{uggLoLVersion}/{gameMode}/{championId}/{overviewVersion}.json") as URL:
                page = json.loads(await URL.text())
                
        return page
    
    @alru_cache(maxsize=5)
    async def uugsite(name, role='', rank='platinum_plus', region='world'):
        champ = re.sub(r'\W+', '', name.lower())
        lane = "?rank=" + rank.lower() + "&region=" + region.lower() + '&role=' + role.lower()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://u.gg/lol/champions/{champ}/build{lane}") as site:
                ugg_html = await site.text()
                ugg = BeautifulSoup(ugg_html, 'lxml')
                site_array = ugg.find_all('div', class_='value')
                return site_array
    
class UGG():
    def __init__(self):
        self
    #Data is gotten in the order 'Win rate, Rank, Pick rate, ban rate, matches' when using find all
    #We use scraping because this data does not exist in U.GGs JSON files
    #The underlying array is cached, so well the initial scrape takes a bit, the following uses are quite quick
    async def Win_rate(name, role='', rank='platinum_plus', region='world'):
        wr  = await stats.uugsite(name, role)
        return wr[0].text
    
    async def Total_matches(name, role='', rank='platinum_plus', region='world'):
        pr = await stats.uugsite(name, role)
        return pr[1].text   
    
    async def Pick_rate(name, role='', rank='platinum_plus', region='world'):
        pr = await stats.uugsite(name, role)
        return pr[2].text
    
    async def Ban_rate(name, role='', rank='platinum_plus', region='world'): 
        br = await stats.uugsite(name, role)
        return br[3].text
    
    @alru_cache(maxsize=1)
    async def Runes(name, role, ranks='platinum_plus', regions='world'):
        ddragon_version = (await stats.ddragon_data())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/runesReforged.json") as dd_runes:
                runes_json = json.loads(await dd_runes.text())
  
        trees = (await stats.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.perks.value]
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
    async def Items(name, role, ranks='platinum_plus', regions='world'):
        ddragon_version = (await stats.ddragon_data())
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/item.json") as dd_items:
                items_json = json.loads(await dd_items.text())
        
        items = (await stats.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0]
        start = []
        core = []
        last_set = set()
        
        
        for z in items_json['data']:
            [start.append(items_json['data'][z]['name']) for i in items[2][2] if str(i) == z]
            [core.append(items_json['data'][z]['name']) for i in items[3][2] if str(i) == z]
            for x in range(3):
                for y in range(3):
                    try:
                        if str(items[data.other_items.value][x][y][0]) == z:
                            last_set.add(items_json['data'][z]['name'])
                    except: pass

        last = list(last_set)
        Items = [start, core, last]
        
        return Items
        
    @alru_cache(maxsize=1)
    async def Shards(name, role, ranks='platinum_plus', regions='world'):
        stat_shard_id = (await stats.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.shards.value][2]
        stat_shard = []
        for s in stat_shard_id:
            match s:
                case "5001" : stat_shard.append("Health")
                case "5008" : stat_shard.append("Adaptive Force")
                case "5007" : stat_shard.append("Ability Haste")
                case "5002" : stat_shard.append("Armor")
                case "5005" : stat_shard.append("Attack Speed")
                case "5003" : stat_shard.append("Magic Resist")
        return stat_shard
    
    @alru_cache(maxsize=5)
    async def Abilities(name, role, ranks='platinum_plus', regions='world'):
        abilities = (await stats.stats(name=name))[region[regions.lower()].value][tiers[ranks.lower()].value][positions[role.lower()].value][0][data.abilities.value][2]
        return abilities