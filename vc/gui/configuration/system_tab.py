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

from vc.gui.configuration.generic_tab import GenericTab
from vc.gui.configuration.properties_system_section import PropertiesSystemSection
from vc.gui.configuration.special_states_shortcuts_applications_section import SpecialStatesShortcutsApplicationSection

class SystemTab(GenericTab):

    def __init__(self, macros):
        self.macros = macros
        
        super(SystemTab, self).__init__()
        
        self.add(PropertiesSystemSection("Properties", self.macros['properties']))
        self.add(PropertiesSystemSection("System commands", self.macros['system']))
        self.add(SpecialStatesShortcutsApplicationSection("Special states", self.macros['special_states']))
        self.add(SpecialStatesShortcutsApplicationSection("Shortcut-sets", self.macros['shortcuts']))
        self.add(SpecialStatesShortcutsApplicationSection("Applications", self.macros['applications']))
