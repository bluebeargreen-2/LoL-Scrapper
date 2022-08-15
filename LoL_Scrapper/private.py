import re, aiohttp, ujson as json
from async_lru import alru_cache
from bs4 import BeautifulSoup

@alru_cache(maxsize=1)
async def ddragondata():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://static.u.gg/assets/lol/riot_patch_update/prod/versions.json") as lolVersion:
            ddragon_version = json.loads(await lolVersion.text())[0]
    return ddragon_version

@alru_cache(maxsize=1)
async def champnamecleaner(name: str, title: bool = True):
    if title == True:
        champname = re.sub(r'\W+', '', name.lower().title().strip())
    else:
        champname = re.sub(r'\W+', '', name.lower().strip())
    return champname

@alru_cache(maxsize=1)
async def beautifulsoup(url: str) -> BeautifulSoup:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as website:
            html = await website.text()
            soup = BeautifulSoup(html, "lxml")
    return soup
