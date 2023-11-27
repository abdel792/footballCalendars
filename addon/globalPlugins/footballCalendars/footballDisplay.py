# globalPlugins/footballCalendars/footballDisplay.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import threading
from urllib.request import Request, urlopen
from .footballRegexps import *
from typing import List
from datetime import datetime
import queue
import os
import json
import addonHandler

curYear = datetime.today().year
addonPath = addonHandler.getCodeAddon().path
prefix1 = "https://www.maxifoot.fr/calendrier-ligue-1-france-"
prefix2 = "https://www.maxifoot.fr/calendrier-ligue-2-france-"
prefLequipe1 = "https://www.lequipe.fr/Football/ligue-1/"
prefLequipe2 = "https://www.lequipe.fr/Football/ligue-2/"
seasons = [f"{x}-{x+1}.htm" for x in range(curYear - 13, curYear + 1)]
firstYear = seasons[0].split("-")[0]
lastYear = seasons[-1].split("-")[1][:-4]
availableSeasons = f"{firstYear}-{lastYear}"
ligue1Seasons = [f"Calendrier ligue-1 {season[:-4]}" for season in seasons]
ligue2Seasons = [f"Calendrier ligue-2 {season[:-4]}" for season in seasons]
lequipeLigue1Rankings = [f"Derniers classements ligue-1 {season[:-4]}" for season in seasons]
lequipeLigue2Rankings = [f"Derniers classements ligue-2 {season[:-4]}" for season in seasons]
allLigue1 = []
allLigue2 = []
urlsLigue1 = [f"{prefix1}{season}" for season in seasons]
urlsLigue2 = [f"{prefix2}{season}" for season in seasons]
urlsLequipeLigue1 = [
	f"{prefLequipe1}saison-{season[:-4]}/page-classement-equipes/general"
	for season in seasons
]
urlsLequipeLigue2 = [
	f"{prefLequipe2}saison-{season[:-4]}/page-classement-equipes/general"
	for season in seasons
]
pgsLigue1 = [urlopen(x).read().decode("iso-8859-1") for x in urlsLigue1]
pgsLigue2 = [urlopen(x).read().decode("iso-8859-1") for x in urlsLigue2]
pgsLequipe1: List[str] = []
pgsLequipe2: List[str] = []


def page(url):
	return urlopen(url).read().decode("iso-8859-1")


def readUrl(url: str, q: queue.Queue):
	headers = {"User-Agent": "Mozilla/5.0"}
	req = Request(url=url, headers=headers)
	data = urlopen(req).read().decode("utf-8")
	q.put(data)


def fetchLequipe(ligue):
	import addonHandler
	print(addonHandler.getCodeAddon().path)
	result = queue.Queue()
	if ligue == 1:
		pgsLequipe1.clear()
	else:
		pgsLequipe2.clear()
	threads = [threading.Thread(
		target=readUrl,
		args=(url, result,)) for url in (
		urlsLequipeLigue1 if ligue == 1
		else urlsLequipeLigue2)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	res = list(result.queue)
	lequipeFile = open(os.path.join(addonPath, f"lequipe{ligue}-{availableSeasons}.json"), "w", encoding="utf-8")
	json.dump(res, lequipeFile)
	if ligue == 1:
		pgsLequipe1.extend(res)
	else:
		pgsLequipe2.extend(res)


if not os.path.exists(os.path.join(addonPath, f"lequipe1-{availableSeasons}.json")):
	fetchLequipe(1)
else:
	lequipe1File = open(os.path.join(addonPath, f"lequipe1-{availableSeasons}.json"), "r", encoding="utf-8")
	pgsLequipe1 = json.load(lequipe1File)
if not os.path.exists(os.path.join(addonPath, f"lequipe2-{availableSeasons}.json")):
	fetchLequipe(2)
else:
	lequipe2File = open(os.path.join(addonPath, f"lequipe2-{availableSeasons}.json"), "r", encoding="utf-8")
	pgsLequipe2 = json.load(lequipe2File)
pgsLequipe1.sort()
pgsLequipe2.sort()

for item in lequipeLigue1Rankings:
	allLigue1.append(ligue1Seasons[lequipeLigue1Rankings.index(item)])
	allLigue1.append(item)

for item in lequipeLigue2Rankings:
	allLigue2.append(ligue2Seasons[lequipeLigue2Rankings.index(item)])
	allLigue2.append(item)


class ArticlesThread(threading.Thread):

	def __init__(self, event: threading.Event, isHtml: bool, url: str):
		threading.Thread.__init__(self)
		self.event = event
		self.isHtml = isHtml
		self.url = url
		self._result: List[str] = []

	def run(self):
		pg = page(self.url)
		lst = [clean.sub("", clean2.sub("-", clean3.sub(" ", x.group(1)))) for x in finditer.finditer(pg)]
		if self.isHtml:
			self._result.clear()
			lstForHtml = []
			[lstForHtml.extend(x.split("\n")[:-1]) for x in lst]
			lstForHtml = [(f"<h1>{x[1:]}</h1>" if x.startswith("^top ") else f"<p>{x}</p>") for x in lstForHtml]
			self._result.extend(lstForHtml)
		else:
			self._result.clear()
			[self._result.extend(x.split("\n")[:-1]) for x in lst]
		self.event.set()

	@property
	def result(self):
		return self._result
