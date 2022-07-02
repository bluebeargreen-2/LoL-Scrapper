import aiohttp
from bs4 import BeautifulSoup

class __internal__:
    def __init__(self) -> None:
        self

    async def soup(link, champ: str):
        champname = champ.lower()
        url = f"https://www.leagueofgraphs.com/champions/{link}/{champname}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as website:
                text = await website.text()
                soup = BeautifulSoup(text, 'html.parser')
        return soup

    async def ratescache(champ: str, id: str):
        link = "stats"
        soup = await __internal__.soup(link, champ=champ)
        text = soup.find(id=id)
        return text

class leagueofgraphs:
    def __init__(self):
        self

    async def runes(champ):
        link = "runes"
        soup = await __internal__.soup(link, champ)
        main = soup.find_all('img', {"style" : "opacity: 1; "})
        secondary = soup.find_all('img', {"style" : "opacity: 0.6; opacity:1"})
        primarytree = [main[y]['alt'] for y  in range(4)]
        secondarytree = [secondary[y]['alt'] for y in range(2)]
        return primarytree + secondarytree

    async def items(champ):
        link = "items"
        soup = await __internal__.soup(link, champ)
        boots = ["Berserker's Greaves", "Boots of Swiftness", "Ionian Boots of Lucidity", "Mercury's Treads", "Sorcerer's Shoes", "Plated Steelcaps", "Mobility Boots"]
        itemimages = soup.find_all('img', {"height" : "36", "width" : "36", "src" : "//lolg-cdn.porofessor.gg/img/s/fond_sprite.png?v=5", "tooltip-class" : "itemTooltip"})
        names = [itemimages[y]["alt"] for y in range (len(itemimages))]
        boot = [i for i in names for y in range(len(boots)) if i == boots[y]]
        smallerrow = 0
        for l in names:
            if l == "Corrupting Potion":
                smallerrow += 1
        if names[1] != "Corrupting Potion":
            start = [names[:3]]
        else:
            start = [names[:2]]
        core = [names[30 - smallerrow:33 - smallerrow]]
        other = [names[60 - smallerrow:63 - smallerrow]]
        return start + core + other + [boot[0]]

    async def pickrate(champ: str):
        id = "graphDD1"
        pr = await __internal__.ratescache(champ=champ, id=id)
        return pr.text.strip()

    async def winrate(champ: str):
        id = "graphDD2"
        wr = await __internal__.ratescache(champ=champ, id=id)
        return wr.text.strip()

    async def banrate(champ: str):
        id = "graphDD3"
        br = await __internal__.ratescache(champ=champ, id=id)
        return br.text.strip()

    async def abilities(champ):
        link = "skills-orders"
        soup = await __internal__.soup(link=link, champ=champ)
        abilitieshtml = soup.find_all("td")
        q = [abilitieshtml[y].text.strip() for y in range(1, 19)]
        w = [abilitieshtml[y].text.strip() for y in range(22, 40)]
        e = [abilitieshtml[y].text.strip() for y in range(41, 59)]
        r = [abilitieshtml[y].text.strip() for y in range(60, 78)]
        qwer = [q, w, e, r]
        abilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for y in range(4):
            for abilitypos, abilityname in enumerate(qwer[y]):
                if abilityname != '':
                    abilities[abilitypos] = abilityname
        return abilities