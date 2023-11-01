# globalPlugins/maxiFoot/maxiFootSettings.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import wx
from typing import Callable, Dict, Tuple
import gui
import gui.guiHelper
import config

# We initialize translation support
import addonHandler
addonHandler.initTranslation()
if hasattr(gui.settingsDialogs, "SettingsPanel"):
	from gui.settingsDialogs import SettingsPanel
else:
	from gui import SettingsPanel

# Constants
ADDON_SUMMARY: str = addonHandler.getCodeAddon().manifest["summary"]
ADDON_NAME: str = addonHandler.getCodeAddon().manifest["name"]

# gettex translation function.
_: Callable[[str], str]

confSpec: Dict = {
	"displayMaxiFootMode": "string(default = HTMLMessage)",
}
config.conf.spec["maxiFoot"] = confSpec


class MaxiFootSettingsPanel(SettingsPanel):

	# Translators: The title of the add-on configuration dialog box.
	title: str = ADDON_SUMMARY
	helpId: str = "maxiFootSettings"
	DISPLAY_MODES: Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]] = (
		("HTMLMessage",
		 # Translators: Display the result in an NVDA message of type HTML.
		 _("Display in HTML message")),
		("simpleMessage",
		 # Translators: Displays the result in a simple NVDA browseable message.
		 _("Display in a simple NVDA browseable message")),
		("defaultBrowser",
		 # Translators: Display the result in default browser.
		 _("Display in default browser"))
	)

	def makeSettings(self, settingsSizer):
		# Translators: The label for an item to select the display mode for maxiFootCalendars pages.
		self.displayMaxiFootModeText = _("{0} pages display mode").format(ADDON_NAME)
		self.showSettingsDialog(settingsSizer)

	def showSettingsDialog(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		displayMaxiFootModeChoices = [name for mode, name in self.DISPLAY_MODES]
		self.displayMaxiFootModesList = settingsSizerHelper.addLabeledControl(
			self.displayMaxiFootModeText,
			wx.Choice,
			choices=displayMaxiFootModeChoices
		)
		curMaxiFootMode = config.conf["maxiFoot"]["displayMaxiFootMode"]
		for index, (mode, name) in enumerate(self.DISPLAY_MODES):
			if mode == curMaxiFootMode:
				self.displayMaxiFootModesList.SetSelection(index)
				break

	def onSave(self):
		displayMaxiFootMode = self.DISPLAY_MODES[self.displayMaxiFootModesList.GetSelection()][0]
		config.conf["maxiFoot"]["displayMaxiFootMode"] = displayMaxiFootMode
