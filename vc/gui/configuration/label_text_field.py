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

class LabelTextField(gtk.HBox):

    def __init__(self, data, key):
        self.key = key
        self.data = data
        
        super(LabelTextField, self).__init__()
        
        self.pack_start(gtk.Label(self.key))
        
        tf = gtk.Entry()
        entryBuff = gtk.EntryBuffer(self.data[self.key], -1)
        tf.set_buffer(entryBuff)
        tf.connect("changed", self.tf_changed)
        
        self.pack_start(tf)
        
    def tf_changed(self, tf):
        self.data[self.key] = tf.get_text()
        print self.data
