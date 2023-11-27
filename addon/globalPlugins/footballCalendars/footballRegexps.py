# globalPlugins/footballCalendars/footballRegexps.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-l+backspace

import re

# Patterns.
pattern1 = r"id='tj\d+' class=ch3>(.*?)</table>"
pattern2 = r"<[^>]*?>"
pattern3 = "</td><td>"
pattern4 = "</td><th><a title[^>]*?>"
pattern5 = r"<table.*?</table>"
pattern6 = r"^[ ]+"

# Compiled regexps.
finditer = re.compile(pattern1, re.S)
clean = re.compile(pattern2, re.S)
clean2 = re.compile(pattern3, re.M)
clean3 = re.compile(pattern4, re.M)
tbl = re.compile(pattern5, re.I | re.S)
first = re.compile(pattern6, re.M)
