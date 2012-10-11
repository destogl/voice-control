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

class TextFieldTextFieldButton(gtk.HBox):

    def __init__(self, data, key):
        self.key = key
        self.data = data
        
        super(TextFieldTextField, self).__init__()
        
        tf_key = gtk.Entry()
        entryBuff_key = gtk.EntryBuffer(self.key, -1)
        tf_key.set_buffer(entryBuff_key)
        tf_key.connect("changed", self.tf_key_changed)
        
        self.tf_value = gtk.Entry()
        entryBuff_value = gtk.EntryBuffer(self.data[self.key], -1)
        self.tf_value.set_buffer(entryBuff_value)
        self.tf_value.connect("changed", self.tf_value_changed)
        
        self.add(tf_key)
        self.add(self.tf_value)
        
    def tf_value_changed(self, tf):
        self.data[self.key] = tf.get_text()
    
    #TODO see internet
    def tf_key_changed(self, tf):
        if not self.key in self.data.keys():
            self.data[self.key] = self.tf_value.get_text()
        self.key = tf.get_text()
