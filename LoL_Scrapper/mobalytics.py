from async_lru import alru_cache
import private

@alru_cache(maxsize=1)
async def soup_catch(champion: str, role: str = ''):
    champname = await private.champnamecleaner(name=champion)
    lane = role.lower()
    url = f"https://app.mobalytics.gg/lol/champions/{champname}/build/{lane}"
    soup = await private.beautifulsoup(url=url)
    matches = soup.find("div", class_="m-j0296l")
    if matches is not None:
        lane = ' '
        url = f"https://app.mobalytics.gg/lol/champions/{champname}/build/{lane}"
        soup = await private.beautifulsoup(url=url)
    return soup

@alru_cache(maxsize=1)
async def rates_cache(champion: str, role: str = ''):
    rates = (await soup_catch(champion, role)).find_all("td", class_="m-m7fsih")
    return rates

@alru_cache(maxsize=1)
async def items(champion: str, role: str = ''):
    item = (await soup_catch(champion, role)).find_all("img", class_="m-10vuljw")
    items = []
    [items.append(entry["alt"]) for entry in item if entry["alt"] not in items]
    return items

class mobalytics():
    def __init__(self):
        self
    
    @alru_cache(maxsize=1)
    async def runes(champion: str, role: str = ''):
        async def KeyStone():
            keystone = (await soup_catch(champion, role)).find("img", class_="m-u9bqoh")
            return keystone["alt"]
        async def Tree():
            runes = []
            tree = (await soup_catch(champion, role)).find_all("img", class_="m-oa6z1e")
            for rune in tree:
                runes.append(rune["alt"])
            return runes
        x = await KeyStone()
        y = await Tree()
        y.insert(0, x)
        return y
    
    @alru_cache(maxsize=1)
    async def items(champion: str, role: str = ''):
        mythic = (await soup_catch(champion, role)).find("img", class_="m-g620l3")["alt"]
        i = await items(champion, role)
        s = i.index("Stealth Ward") + 1
        b = i.index("Boots") + 1
        async def starting():
            start = [i[:s]]
            return start
        async def early():
            early = [i[s:b]]
            return early
        async def core():
            core = [i[b:b+2]]
            core.insert(0, mythic)
            return core
        async def final():
            final = [i[b+2:b+5]]
            return final
        x = [(await starting()), (await early()), (await core()), (await final())]
        return x
    
    async def tier(champion: str, role: str = ''):
        x = await rates_cache(champion, role)
        return x[0].text
    
    async def winrate(champion: str, role: str = ''):
        x = await rates_cache(champion, role)
        return x[1].text
    
    async def pickrate(champion: str, role: str = ''):
        x = await rates_cache(champion, role)
        return x[2].text
    
    async def banrate(champion: str, role: str = ''):
        x = await rates_cache(champion, role)
        return x[3].text
    
    #Only the position of the div is needed here, hence why yy remains unnamed and unused
    async def abilities(champion: str, role: str = ''):
        x = (await soup_catch(champion, role)).find_all("div", class_="m-af8mp8")
        abilities = [x[y].text for y, yy in enumerate(x)]
        return abilities
    
    async def shards(champion: str, role: str = ''):
        x = (await soup_catch(champion, role)).find_all("img", class_="m-j7ixa3")
        shards = [x[y]["alt"] for y, yy in enumerate(x)]
        return shards