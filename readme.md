# Football calendars #

* Authors : Abdel.
* Download [stable version][1]
* Download [development version][2]

This add-on allows you to view football season of France championship schedules for leagues 1 and 2 using the website «https://www.maxifoot.fr».

In its latest version, it integrates the ranking of the teams, according to each season, and according to leagues 1 or 2 based on the history of the rankings appearing on «https://www.lequipe.fr».

It adds a menu to the NVDA Tools menu named «Football calendars».

If you validate this item, a list composed of 2 elements should be displayed:

* League-1 calendars and rankings, which allows you to display the list of league-1 seasons, as well as the history of rankings.
* League-2 calendars and rankings, which allows you to display the list of league-2 seasons, as well as the history of rankings.

The list of seasons and rankings starts from the "2010-2011" season, up to the current ranking, which should be selected by default.

You will then only have to validate on the title of the season to display the planned matches, or on that of the ranking, to see the ranking of the season in question.

If you choose the current season, you will be able to view the matches played, as well as those that have not yet been played.

The standings for the current season are up to date until the last day played.

It is therefore necessary to consult it regularly to view the progress of each team.

For completed seasons, it is of course the final ranking which should be displayed.

## Add-on settings ## {: #footballCalendarsSettings }

In the add-on's settings panel, you should find the following:

* FootballCalendars display mode, which allows you to define the display mode for your calendars and rankings;
* You should then find 3 display modes:
    * Display in an HTML message, which allows you to display the result in a browseable HTML message  (this is the default choice);
    * Display in a simple message, which allows you to display the result in a simple browseable message, without HTML formatting;
    * Display in default browser, to display the result in your default browser.
* An «OK» button to save your configuration;
* A «Cancel» button to cancel and close the dialog box.
* An «Apply» button to apply your configuration;

## Notes ##

* By default, the «control + shift + f8» gesture is assigned to the script which allows you to display season calendars, as well as ranking history;
* A script without an assigned gesture allows you to open the add-on's settings panel;
* You can assign new gestures to run these scripts in the «Input Gestures» menu and more precisely, in the «Football calendars» category;
* If you are using nvda-2021.1 and later, you will be able to access the paragraph describing the add-on settings panel by simply pressing F1 as soon as the focus is on this control.

## Compatibility ##

* This add-on is compatible with NVDA 2019.3 and beyond.


## Changes for version 23.11.27 ##

* Added ranking history to complete the season calendar;
* Renamed the add-on from «maxiFootCalendars» to «footballCalendars».

## Changes for version 23.11.01 ##

* Initial version.

[1]: https://github.com/abdel792/footballCalendars/releases/download/v23.11.27/footballCalendars-23.11.27.nvda-addon

[2]: http://cyber25.free.fr/nvda-addons/footballCalendars-23.11.27-dev.nvda-addon