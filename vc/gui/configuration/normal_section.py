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
from vc.gui.configuration.normal_entry import NormalEntry
from vc.gui.configuration.label_text_field import LabelTextField

class NormalSection(gtk.Frame):

    def __init__(self, name, data):
        self.data = data
        
        super(NormalSection, self).__init__(name)
        
        big_vbox = gtk.VBox()
        
        self.vbox = gtk.VBox()
        for key in self.data.keys():
            if key == 'Additional':
                self.vbox.pack_start(LabelTextField(self.data, key))
            else:
                self.vbox.pack_start(self.__create_entry_object(self.data, key))
            
        big_vbox.pack_start(self.vbox)
        
        button = gtk.Button("Add new command " + name)
        button.connect('clicked', self.button_clicked)
        big_vbox.pack_start(button, False, False, 5)
        
        self.add(big_vbox)
        
    def button_clicked(self, button):
        key = "<new>"
        self.data[key] = [[['hotkey', '']], '']
        self.vbox.pack_start(self.__create_entry_object(self.data, key))
        self.show_all()
        
    def __create_entry_object(self, data, key):
        entry = NormalEntry(data, key)
        entry.connect("destroy", self.entry_object_destroy)
        frame = gtk.Frame()
        frame.add(entry)
        return frame
        
    def entry_object_destroy(self, entry_object):
        self.vbox.remove(entry_object)
        self.show_all()
