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
from vc.gui.configuration.generic_tab import GenericTab
from vc.gui.configuration.text_field_text_field_button import TextFieldTextFieldButton

class UsernamesTab(GenericTab):

    def __init__(self, data):
        self.data = data
        
        super(UsernamesTab, self).__init__()
        self.vbox = gtk.VBox()
        for key in self.data.keys():
            self.vbox.pack_start(self.__create_entry_object(self.data, key))
            
        self.add(self.vbox)
        
        button = gtk.Button("Add username")
        button.connect('clicked', self.button_clicked)
        self.add(button)
        
    def button_clicked(self, button):
        key = "<new>"
        self.data[key] = ''
        self.vbox.pack_start(self.__create_entry_object(self.data, key))
        self.show_all()
        
    def __create_entry_object(self, data, key):
        tf_butt = TextFieldTextFieldButton(data, key)
        tf_butt.connect("destroy", self.entry_object_destroy)
        return tf_butt
        
    def entry_object_destroy(self, entry_object):
        self.vbox.remove(entry_object)
        self.show_all()
