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

class TextFieldButton(gtk.HBox):

    def __init__(self, data, key):
        self.key = key
        self.data = data
        
        super(TextFieldButton, self).__init__()
        
        tf = gtk.Entry()
        entryBuff_key = gtk.EntryBuffer(self.key, -1)
        tf.set_buffer(entryBuff_key)
        tf.connect("changed", self.tf_changed)
        
        button = gtk.Button("Del")
        button.connect('clicked', self.button_clicked)
        
        self.pack_start(tf)
        self.pack_start(button, False, False, 5)
        
    def tf_changed(self, tf):
        self.data[tf.get_text().strip()] = self.data.pop(self.key)
    
    def button_clicked(self, button):
        del self.data[self.key]
        self.destroy()
