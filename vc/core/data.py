# -*- coding: latin-1 -*-
"""
Copyright 2012 Denis Štogl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import OrderedDict

action_types = {
                'HotKey': 'hotkey',
                'Command': 'cmd',
                'Mouse': 'mouse',
                'String': 'string',
                }
action_types_ordered = OrderedDict(sorted(action_types.items(), key=lambda t: t[1][1]))

action_types_3 = {
                0: 'HotKey',
                1: 'Command',
                2: 'Mouse',
                3: 'String',
                }

action_types_2 = {
                'hotkey': 'HotKey',
                'cmd': 'Command',
                'mouse': 'Mouse',
                'string': 'String',
                }
