# LoL-Scrapper
Tools for getting data from LoL sites like u.gg

## Setup:
Install from github using `pip install git+https://github.com/AlsoSylv/LoL-Scrapper.git`
This is designed to work without the usage of LoL API

## Usage:
Examples can be found in ./examples/{site-name}, but should be mostly the same between sites.

Example for [u.gg](https://u.gg/):
```python
print(asyncio.run(ugg.UGG.WinRate(self, "Annie", "Mid")))
#Returns the current winrate for Annie in the mid lane
```
## Currently Supports:
- [X] [U.gg](https://u.gg/)
- [x] [Mobalytics.gg](https://mobalytics.gg/)
- [ ] [OP.gg](https://na.op.gg/)
- [ ] [Champion.gg](https://champion.gg/)
- [ ] [LoLalytics.com](https://lolalytics.com/)
- [X] [LeagueOfGraphcs.com](https://www.leagueofgraphs.com/)
- [ ] [ProBuilds](https://www.probuilds.net/)
- [ ] [MobaFire.com](https://www.mobafire.com/)
- [ ] [Blitz.gg](https://blitz.gg/)
- [ ] [METAsrc](https://www.metasrc.com/5v5)
