# globalPlugins/footballCalendars/__init__.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import addonHandler
import globalPluginHandler
import threading
from typing import Callable, Dict
import wx
import gui
from gui import NVDASettingsDialog
from .footballCalendars import FootballCalendarsDialog
from .footballSettings import ADDON_NAME, ADDON_SUMMARY, FootballSettingsPanel
from .contextHelp import showAddonHelp
addonHandler.initTranslation()

event = threading.Event()

# gettex translation function.
_: Callable[[str], str]

if hasattr(gui, 'contextHelp'):
	saveShowHelp = gui.contextHelp.showHelp


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory: str = ADDON_SUMMARY
	contextHelp: bool = False

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		NVDASettingsDialog.categoryClasses.append(FootballSettingsPanel)
		self.createMenu()

	def createMenu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		self.footballItem = self.toolsMenu.Append(wx.ID_ANY,
		# Translators: Item in the tools menu for displaying Football calendars.
		_("&Football calendars..."),
		# Translators: The tooltyp text for the football item.
		_("Allows you to display the football season calendars of the French championship for leagues 1 and 2 as well as the rankings history"))

		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onFootballDialog, self.footballItem)

	def terminate(self):
		try:
			NVDASettingsDialog.categoryClasses.remove(FootballSettingsPanel)
		except Exception:
			pass
		try:
			if wx.version().startswith("4"):
				self.toolsMenu.Remove(self.footballItem)
			else:
				self.toolsMenu.RemoveItem(self.footballItem)
		except Exception:
			pass

	def event_gainFocus(self, obj, nextHandler):
		if hasattr(gui, 'contextHelp'):
			if obj.parent and obj.parent.parent and any(
				x == ADDON_SUMMARY for x in (obj.name, obj.parent.parent.name)
			) or self.contextHelp:
				gui.contextHelp.showHelp = showAddonHelp
			else:
				gui.contextHelp.showHelp = saveShowHelp
		nextHandler()

	def script_displayFootballCalendars(self, gesture):
		self.onFootballDialog()

	# Translators: Message presented in input help mode.
	script_displayFootballCalendars.__doc__ = _(
		"Allows you to display the season calendars, as well as the history of the rankings of the French football championship for leagues 1 and 2"
	)

	def onFootballCalendarsDialog(self, evt):
		gui.mainFrame.prePopup()
		d = FootballCalendarsDialog(gui.mainFrame)
		d.Show()
		gui.mainFrame.postPopup()

	def script_activateAddonSettingsDialog(self, gesture):
		if hasattr(gui.settingsDialogs, "NVDASettingsDialog"):
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				gui.settingsDialogs.NVDASettingsDialog, FootballSettingsPanel
			)
		else:
			wx.CallAfter(self.onAddonSettingsDialog, gui.mainFrame)

	# Translators: Message presented in input help mode.
	script_activateAddonSettingsDialog.__doc__ = _(
		"Allows you to display the {0} add-on settings panel."
	).format(ADDON_NAME)

	def onFootballDialog(self, evt=None):
		wx.CallAfter(self.onFootballCalendarsDialog, gui.mainFrame)

	def onAddonSettingsDialog(self, evt):
		gui.mainFrame._popupSettingsDialog(NVDASettingsDialog, FootballSettingsPanel)

	__gestures: Dict = {
		"kb:control+shift+f8": "displayFootballCalendars",
	}
