# globalPlugins/maxiFoot/__init__.py.

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
from .maxiFootCalendars import MaxiFootCalendarsDialog
from .maxiFootSettings import ADDON_NAME, ADDON_SUMMARY, MaxiFootSettingsPanel
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
		NVDASettingsDialog.categoryClasses.append(MaxiFootSettingsPanel)
		self.createMenu()

	def createMenu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		self.maxiFootItem = self.toolsMenu.Append(wx.ID_ANY,
		# Translators: Item in the tools menu for displaying maxiFoot calendars.
		_("Maxi&Foot calendars..."),
		# Translators: The tooltyp text for the maxiFoot item.
		_("Allows you to view the football season calendars for league-1 and 2 using maxifoot.fr website"))

		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMaxiFootDialog, self.maxiFootItem)

	def terminate(self):
		try:
			NVDASettingsDialog.categoryClasses.remove(MaxiFootSettingsPanel)
		except Exception:
			pass
		try:
			if wx.version().startswith("4"):
				self.toolsMenu.Remove(self.maxiFootItem)
			else:
				self.toolsMenu.RemoveItem(self.maxiFootItem)
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

	def script_displayMaxiFootCalendars(self, gesture):
		self.onMaxiFootDialog()

	# Translators: Message presented in input help mode.
	script_displayMaxiFootCalendars.__doc__ = _(
		"Allows you to display the football calendars for leagues 1 and 2 from the maxifoot.fr website"
	)

	def onMaxiFootCalendarsDialog(self, evt):
		gui.mainFrame.prePopup()
		d = MaxiFootCalendarsDialog(gui.mainFrame)
		d.Show()
		gui.mainFrame.postPopup()

	def script_activateAddonSettingsDialog(self, gesture):
		if hasattr(gui.settingsDialogs, "NVDASettingsDialog"):
			wx.CallAfter(
				(gui.mainFrame.popupSettingsDialog if hasattr(gui.mainFrame, "popupSettingsDialog")
				 else gui.mainFrame._popupSettingsDialog),
				gui.settingsDialogs.NVDASettingsDialog, MaxiFootSettingsPanel
			)
		else:
			wx.CallAfter(self.onAddonSettingsDialog, gui.mainFrame)

	# Translators: Message presented in input help mode.
	script_activateAddonSettingsDialog.__doc__ = _(
		"Allows you to display the {0} add-on settings panel."
	).format(ADDON_NAME)

	def onMaxiFootDialog(self, evt=None):
		wx.CallAfter(self.onMaxiFootCalendarsDialog, gui.mainFrame)

	def onAddonSettingsDialog(self, evt):
		gui.mainFrame._popupSettingsDialog(NVDASettingsDialog, MaxiFootSettingsPanel)

	__gestures: Dict = {
		"kb:control+shift+f8": "displayMaxiFootCalendars",
	}
