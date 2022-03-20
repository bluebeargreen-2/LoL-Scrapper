import requests, json, re
from bs4 import BeautifulSoup
from enum import Enum
from cassiopeia.core.match import Position
    
class region(Enum):
    na = "1"
    euw = "2"
    kr = "3"
    euna = "4"
    br = "5"
    las = "6"
    lan = "7"
    oce = "8"
    ru = "9"
    tr = "10"
    jp = "11"
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
    diamond_two_plus = "12"
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
    perks = "0"
    summoner_spells = "1"
    start_items = "2"
    mythic_and_core = "3"
    abilities = "4"
    other_items = "5"
    shards = "8"
    
class shards(Enum):
    Health = ["5001", "Health"]
    Armor = ["5002", "Armor"]
    MR = ["5003", "Magic Resistance"]
    AS = ["5005", "Attack Speed"]
    AH = ["5007", "Ability Haste"]
    AF = ["5008", "Adpative Force"]
    
    
class stats():
    def __init__(self):
        self
        
    def stats(self, name):
        statsVersion = '1.1'
        overviewVersion = '1.5.0'
        baseOverviewUrl = 'https://stats2.u.gg/lol'
        gameMode = "ranked_solo_5x5"
        lolVersion = requests.get("https://raw.communitydragon.org/latest/content-metadata.json").json()["version"].split(".")
        ddragon_version = requests.get("https://static.u.gg/assets/lol/riot_patch_update/prod/versions.json").json()[0]
        championName = name.lower().title().strip()
        champName = re.sub(r'\W+', '', championName)
        championId = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/champion.json").json()["data"][f"{champName}"]["key"]
        uggLoLVersion = lolVersion[0] + '_' + lolVersion[1]
    
        URL = f"{baseOverviewUrl}/{statsVersion}/overview/{uggLoLVersion}/{gameMode}/{championId}/{overviewVersion}.json"

        page = requests.get(URL)
        j = page.text
        r = json.loads(j)
        return r

class UGG():
    

    def __init__(self):
        self
        
    #Data is gotten in the order 'Win rate, Rank, Pick rate, ban rate, matches' when using find all
    def Win_rate(self, name, role=''):
        champ = re.sub(r'\W+', '', name.lower())
        lane = '?role=' + role
        URL = f"https://u.gg/lol/champions/{champ}/build{lane}"
        page = requests.get(URL)
        ugg = BeautifulSoup(page.content, 'html.parser')
        wr = ugg.find_all('div', class_='value')
        return wr[0].text
    
    def Total_matches(self, name, role=''):
        champ = re.sub(r'\W+', '', name.lower())
        lane = "?role=" + role
        URL = f"https://u.gg/lol/champions/{champ}/build{lane}"
        page = requests.get(URL)
        ugg = BeautifulSoup(page.content, 'html.parser')
        pr = ugg.find_all('div', class_='value')
        return pr[1].text   
    
    def Pick_rate(self, name, role=''):
        champ = re.sub(r'\W+', '', name.lower())
        lane = "?role=" + role
        URL = f"https://u.gg/lol/champions/{champ}/build{lane}"
        page = requests.get(URL)
        ugg = BeautifulSoup(page.content, 'html.parser')
        pr = ugg.find_all('div', class_='value')
        return pr[2].text
    
    def Ban_rate(self, name, role=''):
        champ = re.sub(r'\W+', '', name.lower())
        lane = "?role=" + role
        URL = f"https://u.gg/lol/champions/{champ}/build{lane}"
        page = requests.get(URL)
        ugg = BeautifulSoup(page.content, 'html.parser')
        br = ugg.find_all('div', class_='value')
        return br[3].text
    
    def Runes(self, name, role):
            rune_ids = stats.stats(self, name=name)[region.world.value][tiers.platinum_plus.value][positions[role.lower()].value][0][0][4]
            trees = stats.stats(self, name=name)[region.world.value][tiers.platinum_plus.value][positions[role.lower()].value][0][0]
            ddragon_version = requests.get("https://static.u.gg/assets/lol/riot_patch_update/prod/versions.json").json()[0]
            dd_runes = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/runesReforged.json")
            runes_json = json.loads(dd_runes.text)
            runes_1 = []
            runes_2 = []     
            for y in range(6):
                for tree in runes_json:
                    for slots_pos, slots in enumerate(tree["slots"]):
                        for rune_data in slots["runes"]:
                            if rune_ids[y] == rune_data["id"]:
                                if tree["id"] == trees[2]:
                                    runes_1.insert(slots_pos, rune_data['name'])
                                elif tree['id'] == trees[3]:
                                    runes_2.insert(slots_pos - 1, rune_data['name'])
            runes = runes_1 + runes_2
            return runes
    
    def Items(self, name, role):
        ddragon_version = requests.get("https://static.u.gg/assets/lol/riot_patch_update/prod/versions.json").json()[0]
        dd_items = json.loads(requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ddragon_version}/data/en_US/item.json").text)
        items = stats.stats(self, name=name)[region.world.value][tiers.platinum_plus.value][positions[role.lower()].value][0]
        start = []
        core = []
        last = []
        
        for z in dd_items['data']:
            for y in range(2, 4):
                for i in items[y][2]:
                    if str(i) == z:
                        if y == 2:
                            start.append(dd_items['data'][z]['name'])
                        else:
                            core.append(dd_items['data'][z]['name'])
            else:
                for x in range(3):
                    for y in range(3):
                        try:
                            if str(items[5][x][y][0]) == z:
                                if dd_items['data'][z]['name'] not in last:
                                    last.append(dd_items['data'][z]['name'])
                                else: 
                                    pass
                        except:
                            pass      
                
        Items = [start, core, last]
        
        return Items
        
    def Shards(self, name, role):
        stat_shard_id = stats.stats(self, name=name)[region.world.value][tiers.platinum_plus.value][positions[role.lower()].value][0][8][2]
        stat_shard = []
        for s in range(3):
            if stat_shard_id[s] == shards.Health.value[0]:
                stat_shard.append(shards.Health.value[1])
            elif stat_shard_id[s] == shards.Armor.value[0]:
                stat_shard.append(shards.Armor.value[1])
            elif stat_shard_id[s] == shards.MR.value[0]:
                stat_shard.append(shards.MR.value[1])
            elif stat_shard_id[s] == shards.AS.value[0]:
                stat_shard.append(shards.AS.value[1])
            elif stat_shard_id[s] == shards.AH.value[0]:
                stat_shard.append(shards.AH.value[1])
            elif stat_shard_id[s] == shards.AF.value[0]:
                stat_shard.append(shards.AF.value[1])
            else:
                break
        return stat_shard
    
    def Abilities(self, name, role):
        abilities = stats.stats(self, name=name)[region.world.value][tiers.platinum_plus.value][positions[role.lower()].value][0][4][2]
        return abilities
