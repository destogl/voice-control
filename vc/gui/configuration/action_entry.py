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
import vc.core.data as Data

class ActionEntry(gtk.HBox):

    def __init__(self, data):
        self.data = data
        
        super(ActionEntry, self).__init__()
        
        vbox = gtk.VBox()
        
        hbox = gtk.HBox()
        button = None
        for action_type in Data.action_types_ordered.keys():
            button = gtk.RadioButton(button, action_type)
            if Data.action_types[action_type] == self.data[0]:
                button.set_active(True)
            button.connect("toggled", self.action_type_changed, action_type)
            hbox.pack_start(button, True, True, 0)
        
        tf = gtk.Entry()
        entryBuff = gtk.EntryBuffer(self.data[1], -1)
        tf.set_buffer(entryBuff)
        tf.connect("changed", self.tf_changed)
        
        vbox.pack_start(hbox)
        vbox.pack_start(tf)
        
        button = gtk.Button("Del")
        button.connect('clicked', self.button_clicked)
        
        self.pack_start(vbox)
        self.pack_start(button, False, False, 5)
    
    def action_type_changed(self, button, action_type):
        if button.get_active():
            self.data[0] = Data.action_types[action_type]
    
    def tf_changed(self, tf):
        self.data[1] = tf.get_text().strip()
    
    def button_clicked(self, button):
        self.destroy()
