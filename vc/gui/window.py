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
from vc.gui.standard_view import StandardView
from vc.gui.configuration_view import ConfigurationView

class Window(gtk.Window):
    
    def __init__(self, logic):
        self.logic = logic
        self.standard_view = None
        self.configuration_view = None
        
        super(Window, self).__init__()
        self.set_title("Voice Control")
        self.connect("delete-event", self.app_quit)
        self.set_border_width(10)
        
        # get resolution
#        self.width = gtk.gdk.display_get_default().get_default_screen().get_width()
#        self.height = gtk.gdk.display_get_default().get_default_screen().get_height()
#        self.maximize()
#        self.width, self.height = self.get_size()
        self.width = 1000
        self.height = 700
        self.set_default_size(self.width, self.height)
        
        mb = gtk.MenuBar()
        
        # FILE
        item = gtk.MenuItem("File")
        menu = gtk.Menu()
        
        subitem = gtk.MenuItem("Quit")
        subitem.connect("activate", self.app_quit)
        menu.append(subitem)
        item.set_submenu(menu)
        mb.append(item)
        
        # CONFIGURATION
        item = gtk.MenuItem("View")
        menu = gtk.Menu()
        
        subitem = gtk.MenuItem("Standard")
        subitem.connect("activate", self.activate_standard_view)
        menu.append(subitem)
        
        subitem = gtk.MenuItem("Configuration")
        subitem.connect("activate", self.activate_configuration_view)
        menu.append(subitem)
        
        item.set_submenu(menu)
        mb.append(item)
        
#        # HELP
#        item = gtk.MenuItem("Help")
#        menu = gtk.Menu()
#        
#        subitem = gtk.MenuItem("Contents")
#        subitem.connect("activate", self.help_view)
#        menu.append(subitem)
#        
#        subitem = gtk.MenuItem("About")
#        subitem.connect("activate", self.about_view)
#        menu.append(subitem)
#        
#        item.setsubmenu(menu)
#        mb.append(item)
        
        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(mb, False, False, 0)
        
        print self.width
        print self.height
        self.standard_view = StandardView(self.logic, self.width, self.height)
        self.vbox.pack_start(self.standard_view, False, False, 0)
#        self.configuration_view = ConfigurationView(self.logic, self.width, self.height)
#        self.vbox.pack_start(self.configuration_view, False, False, 0)
        
        self.add(self.vbox)
        self.resize_children()
        self.show_all()

    def app_quit(self, widget=None, event=None, data=None):
        self.logic.app_quit()
        
    def activate_standard_view(self, data=None):
        if self.standard_view == None:
            self.standard_view = StandardView(self.logic, self.width, self.height)
    
        self.vbox.remove(self.configuration_view)
        self.vbox.pack_start(self.standard_view, False, False, 0)
        self.show_all()
        
    def activate_configuration_view(self, data=None):
        if self.configuration_view == None:
            self.configuration_view = ConfigurationView(self.logic, self.width, self.height)
        
        self.vbox.remove(self.standard_view)
        self.vbox.pack_start(self.configuration_view, False, False, 0)
        self.show_all()
