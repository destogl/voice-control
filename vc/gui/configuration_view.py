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

import gtk
import os
from vc.core.configuration_reader_writer import ConfigurationReaderWriter
from vc.gui.generic_view import GenericView
from vc.gui.configuration.system_tab import SystemTab
from vc.gui.configuration.window_manager_tab import WMTab
from vc.gui.configuration.shortcut_set_tab import ShortcutSetTab
from vc.gui.configuration.usernames_tab import UsernamesTab
from vc.gui.configuration.passwords_tab import PasswordsTab

class ConfigurationView(GenericView):

    def __init__(self, logic, width, height):
        self.logic = logic
        
        super(ConfigurationView, self).__init__(width, height)
        
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.set_scrollable(True)
        
        notebook.append_page(SystemTab(self.logic.macros), gtk.Label("System"))
        notebook.append_page(WMTab(self.logic.macros), gtk.Label("Window Manger"))
        notebook.append_page(ShortcutSetTab('', self.logic.macros['system_wide']), gtk.Label("System-wide"))
        
        for shortcut_set in self.logic.macros['shortcuts'].values():
            if shortcut_set != 'system':
                notebook.append_page(ShortcutSetTab('', self.logic.macros['non_system'][shortcut_set]), gtk.Label(shortcut_set.capitalize()))
        
#        notebook.append_page(UsernamesTab(self.logic.usernames), gtk.Label("Usernames"))
#        notebook.append_page(PasswordsTab(self.logic.usernames), gtk.Label("Passwords"))
        
        self.add(notebook)
        
        button = gtk.Button("Save Configurtion")
        button.connect('clicked', self.button_clicked)
        self.pack_start(button, False, False, 5)
        
    def button_clicked(self, button):
        ConfigurationReaderWriter.write_macros_directory(os.environ['HOME'] + '/.voice-control/macros/', self.logic.macros, self.logic.passwords, self.logic.usernames)
