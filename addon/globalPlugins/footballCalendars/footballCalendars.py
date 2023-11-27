# globalPlugins/footballCallendars/footballCalendars.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import addonHandler
from typing import Callable
import tempfile
from .footballDisplay import prefix1, prefix2, pgsLequipe1, pgsLequipe2, ArticlesThread, allLigue1, allLigue2
from .footballRegexps import *
from .footballSettings import ADDON_NAME
import os
import re
import ui
import threading
import gui
import config
from gui import SettingsDialog
import wx
addonHandler.initTranslation()

event = threading.Event()

# gettex translation function.
_: Callable[[str], str]


def cleanMessageForText(htmlMessage):
	text = clean.sub("", htmlMessage)
	lines = [x.strip() for x in text.split("\n")]
	while lines.count(""):
		lines.remove("")
	return "\n".join(lines)


def displayInDefaultBrowser(fileName: str, title: str, body: str) -> None:
	addonTempDir = os.path.join(tempfile.gettempdir(), ADDON_NAME)
	if not os.path.exists(addonTempDir):
		os.mkdir(addonTempDir)
	file = os.path.join(addonTempDir, f"{fileName}.html")
	htmlText = f"""<!DOCTYPE html>
	<html lang='fr'>
	<meta charset = 'utf-8' />
	<head>
	<title>{title}</title>
	</head>
	<body>
	{body}
	</body>
	</html>"""
	with open(file, mode="w", encoding="utf-8") as f:
		f.write(htmlText.replace("\t", ""))
	os.startfile(file)  # type: ignore[attr-defined]


class FootballCalendarsDialog(SettingsDialog):

	# Translators: This is the label for the football calendars choices.
	title = _("List of calendars and rankings")

	def makeSettings(self, settingsSizer):
		self._liguesCalendars = (
			# Translators: Item for the league-1 calendars and rankings.
			_("League-1 calendar"),
			# Translators: Item for the league-2 calendars and rankings.
			_("League-2 calendar"),
		)
		# Translators: This is the label for a combo box in the football calendars dialog.
		self._calendarsTitle = _("Calendars and rankings...")

		self.showCalendarsDialog(settingsSizer=settingsSizer)

	def postInit(self):
		self._calendarsChoice.SetFocus()

	def showCalendarsDialog(self, settingsSizer):
		calendarsSettingsGuiHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._calendarsChoice = calendarsSettingsGuiHelper.addLabeledControl(
			self._calendarsTitle, wx.Choice, choices=self._liguesCalendars
		)
		self._calendarsChoice.SetSelection(0)

	def onOk(self, evt):
		ligue = self._calendarsChoice.GetSelection() + 1
		gui.mainFrame.prePopup()
		d = SeasonsDialog(parent=gui.mainFrame, ligue=ligue)
		d.Show()
		gui.mainFrame.postPopup()


class SeasonsDialog(SettingsDialog):

	# Translators: This is the label for the season choices.
	title = _("List of seasons")

	def __init__(self, ligue, *args, **kwargs):
		self.ligue = ligue
		super(SeasonsDialog, self).__init__(*args, **kwargs)

	def makeSettings(self, settingsSizer):
		self._ligueSeasons = tuple([x for x in (allLigue1 if self.ligue == 1 else allLigue2)])

		# Translators: This is the label for a combo box in the seasons dialog.
		self._seasonsTitle = _("Seasons...")

		self.showSeasonsDialog(settingsSizer=settingsSizer)

	def postInit(self):
		self._seasonsChoice.SetFocus()

	def showSeasonsDialog(self, settingsSizer):
		seasonsSettingsGuiHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._seasonsChoice = seasonsSettingsGuiHelper.addLabeledControl(
			self._seasonsTitle, wx.Choice, choices=self._ligueSeasons
		)
		max = len(self._ligueSeasons) - 1
		self._seasonsChoice.SetSelection(max)

	def onOk(self, evt):
		curIndex = self._seasonsChoice.GetSelection()
		isHtml = config.conf["football"]["displayFootballMode"] in ("HTMLMessage", "defaultBrowser")
		display = self._seasonsChoice.GetString(curIndex)
		season = display.split(" ")[-1]
		if "classement" not in display:
			if self.ligue == 1:
				url = f"{prefix1}{season}.htm"
			else:
				url = f"{prefix2}{season}.htm"
			title = _("Season {0}").format(season)
			thread = ArticlesThread(event, isHtml=isHtml, url=url)
			thread.start()
			event.wait()
			event.clear()
			calendars = thread._result
			message = "\r\n".join(calendars)
		else:
			index = int(curIndex / 2)
			if self.ligue == 1:
				page = pgsLequipe1[index]
			else:
				page = pgsLequipe2[index]
			result = clean.sub("", tbl.search(page).group(0))
			content = result.split("\n")
			for item in content:
				if item.isspace():
					content.remove(item)
			result = first.sub("", result)
			lResult = result.split("\n")
			content = lResult[lResult.index("1"):]
			content = [item for item in content if item != ""]
			for i in range(len(content)):
				try:
					if content[i].isnumeric():
						content[i:i + 2] = [". ".join(content[i:i + 2])]
				except IndexError:
					pass
			addition = ["Nombre de points ",
			"Nombre de matchs joués ",
			"Nombre de victoires ",
			"Nombre de matchs nulls ",
			"Nombre de défaites ",
			"Nombre de buts marqués ",
			"Nombre de buts encaissés ",
			"Différences de buts "]
			lst = []
			for item in content:
				lst.append(f"<h1>{item}</h1>")
				if "  " in item:
					lst.remove(f"<h1>{item}</h1>")
					newLst = re.split(r"[\s]+", item)[: -1]
					if "1." in newLst:
						newLst.remove("1.")
					newLst.insert(0, "<ul>")
					newLst[1] = f"<li>{addition[0]}{newLst[1]}</li>"
					newLst[2] = f"<li>{addition[1]}{newLst[2]}</li>"
					newLst[3] = f"<li>{addition[2]}{newLst[3]}</li>"
					newLst[4] = f"<li>{addition[3]}{newLst[4]}</li>"
					newLst[5] = f"<li>{addition[4]}{newLst[5]}</li>"
					newLst[6] = f"<li>{addition[5]}{newLst[6]}</li>"
					newLst[7] = f"<li>{addition[6]}{newLst[7]}</li>"
					newLst[8] = f"<li>{addition[7]}{newLst[8]}</li>"
					newLst.insert(9, "</ul>")
					lst.extend(newLst)
			lst = [x for x in lst if x != ""]
			message = "\n".join(lst)
			message = message if isHtml else cleanMessageForText(message)
			print(message)
			title = display
		if config.conf["football"]["displayFootballMode"] in ("simpleMessage", "HTMLMessage"):
			ui.browseableMessage(title=title, message=message, isHtml=isHtml)
		else:
			displayInDefaultBrowser(fileName="footballCalendars", title=title, body=message)
