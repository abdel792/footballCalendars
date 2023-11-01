# globalPlugins/maxiFoot/maxiFootDisplay.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import threading
from urllib.request import urlopen
from datetime import datetime
from .maxiFootRegexps import *
from typing import List

curYear = datetime.now().year
prefix1 = "https://www.maxifoot.fr/calendrier-ligue-1-france-"
prefix2 = "https://www.maxifoot.fr/calendrier-ligue-2-france-"
seasons = [f"{x}-{x+1}.htm" for x in range(curYear - 13, curYear + 1)]
ligue1Seasons = [f"Saisons ligue-1 {season[:-4]}" for season in seasons]
ligue2Seasons = [f"Saisons ligue-2 {season[:-4]}" for season in seasons]
urlsLigue1 = [f"{prefix1}{season}" for season in seasons]
urlsLigue2 = [f"{prefix2}{season}" for season in seasons]
pgsLigue1 = [urlopen(x).read().decode("iso-8859-1") for x in urlsLigue1]
pgsLigue2 = [urlopen(x).read().decode("iso-8859-1") for x in urlsLigue2]


def page(url):
	return urlopen(url).read().decode("iso-8859-1")


class ArticlesThread(threading.Thread):

	def __init__(self, event: threading.Event, isHtml: bool, url: str):
		threading.Thread.__init__(self)
		self.event = event
		self.isHtml = isHtml
		self.url = url
		self._result: List[str] = []

	def run(self):
		print(str(self.isHtml))
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
