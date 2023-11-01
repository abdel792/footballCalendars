# addon/globalPlugins/maxiFoot/maxiFootCalendars.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import addonHandler
from typing import Callable
import tempfile
from .maxiFootDisplay import prefix1, prefix2, ligue1Seasons, ligue2Seasons, ArticlesThread
from .maxiFootSettings import ADDON_NAME
import os
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


class MaxiFootCalendarsDialog(SettingsDialog):

	# Translators: This is the label for the maxifoot calendars choices.
	title = _("List of calendars")

	def makeSettings(self, settingsSizer):
		self._liguesCalendars = (
			# Translators: Item for the league-1 calendar.
			_("Ligue-1 calendar"),
			# Translators: Item for the league-2 calendar.
			_("Ligue-2 calendar"),
		)
		# Translators: This is the label for a combo box in the maxifoot calendars dialog.
		self._calendarsTitle = _("Calendars...")

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
		super(MaxiFootCalendarsDialog, self).onOk(evt)
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
		self._ligueSeasons = tuple([x for x in (ligue1Seasons if self.ligue == 1 else ligue2Seasons)])

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
		super(SeasonsDialog, self).onOk(evt)
		season = self._seasonsChoice.GetString(self._seasonsChoice.GetSelection()).split(" ")[-1]
		if self.ligue == 1:
			url = f"{prefix1}{season}.htm"
		else:
			url = f"{prefix2}{season}.htm"
		isHtml = config.conf["maxiFoot"]["displayMaxiFootMode"] in ("HTMLMessage", "defaultBrowser")
		title = _("Season {0}").format(season)
		thread = ArticlesThread(event, isHtml=isHtml, url=url)
		thread.start()
		event.wait()
		event.clear()
		articles = thread._result
		message = "\r\n".join(articles)
		if config.conf["maxiFoot"]["displayMaxiFootMode"] in ("simpleMessage", "HTMLMessage"):
			ui.browseableMessage(title=title, message=message, isHtml=isHtml)
		else:
			displayInDefaultBrowser(fileName="maxiFootCalendars", title=title, body=message)
