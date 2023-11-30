# globalPlugins/footballCalendars/footballDisplay.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import threading
from urllib.request import Request, urlopen
from .footballRegexps import *
from typing import List, Optional
from datetime import datetime
import queue


curYear: int = datetime.today().year if datetime.today().month > 6 else datetime.today().year - 1
prefix1: str = "https://www.maxifoot.fr/calendrier-ligue-1-france-"
prefix2: str = "https://www.maxifoot.fr/calendrier-ligue-2-france-"
prefLequipe1: str = "https://www.lequipe.fr/Football/ligue-1/"
prefLequipe2: str = "https://www.lequipe.fr/Football/ligue-2/"
seasons: List[str] = [f"{x}-{x+1}.htm" for x in range(curYear - 13, curYear + 1)]
ligue1Seasons: List[str] = [f"Calendrier ligue-1 {season[:-4]}" for season in seasons]
ligue2Seasons: List[str] = [f"Calendrier ligue-2 {season[:-4]}" for season in seasons]
lequipeLigue1Rankings: List[str] = [f"Derniers classements ligue-1 {season[:-4]}" for season in seasons]
lequipeLigue2Rankings: List[str] = [f"Derniers classements ligue-2 {season[:-4]}" for season in seasons]
allLigue1: List[str] = []
allLigue2: List[str] = []
urlsLequipeLigue1: List[str] = [
	f"{prefLequipe1}saison-{season[:-4]}/page-classement-equipes/general"
	for season in seasons
]
urlsLequipeLigue2: List[str] = [
	f"{prefLequipe2}saison-{season[:-4]}/page-classement-equipes/general"
	for season in seasons
]
pgsLequipe1: List[str] = []
pgsLequipe2: List[str] = []


def readUrl(url: str, coding: str, q: Optional[queue.Queue] = None) -> Optional[str]:
	headers = {"User-Agent": "Mozilla/5.0"}
	req = Request(url=url, headers=headers)
	data = urlopen(req).read().decode(coding)
	if not q:
		return data
	q.put(data)
	return None


def fetchLequipe(ligue: int) -> None:
	result: queue.SimpleQueue = queue.SimpleQueue()
	res: List[str] = []
	if ligue == 1:
		pgsLequipe1.clear()
	else:
		pgsLequipe2.clear()
	threads = [threading.Thread(
		target=readUrl,
		args=(url, "utf-8", result,)) for url in (
		urlsLequipeLigue1 if ligue == 1
		else urlsLequipeLigue2)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	for i in range(result.qsize()):
		res.append(result.get_nowait())
	if ligue == 1:
		pgsLequipe1.extend(res)
	else:
		pgsLequipe2.extend(res)


fetchLequipe(1)
fetchLequipe(2)
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
		pg = readUrl(self.url, "iso8859-1")
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
