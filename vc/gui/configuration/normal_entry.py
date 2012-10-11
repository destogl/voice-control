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
from vc.gui.configuration.action_entry import ActionEntry

class NormalEntry(gtk.VBox):

    def __init__(self, data, key):
        self.key = key
        self.data = data
        
        super(NormalEntry, self).__init__(False, 3)
        
        hbox = gtk.HBox()
        
        hbox.pack_start(gtk.Label("Command"))
        
        tf = gtk.Entry()
        entryBuff_key = gtk.EntryBuffer(self.key, -1)
        tf.set_buffer(entryBuff_key)
        tf.connect("changed", self.tf_key_changed)
        
        hbox.pack_start(tf)
        self.pack_start(hbox)
        
        hbox = gtk.HBox()
        
        hbox.pack_start(gtk.Label("Action"))
        
        self.vbox = gtk.VBox()
        for action in self.data[self.key][0]:
            self.vbox.pack_start(self.__create_action_entry(action))
        
        button = gtk.Button("Add action")
        button.connect('clicked', self.add_action_button_clicked)
        self.vbox.pack_end(button, False, False, 5)
        
        hbox.pack_start(self.vbox)
        self.pack_start(hbox)
        
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Next mode"))
        
        tf = gtk.Entry()
        entryBuff_key = gtk.EntryBuffer(self.data[self.key][1], -1)
        tf.set_buffer(entryBuff_key)
        tf.connect("changed", self.tf_mode_changed)
        
        hbox.pack_start(tf)
        self.pack_start(hbox)
        
        button = gtk.Button("Delete Entry")
        button.connect('clicked', self.delete_button_clicked)
        self.pack_start(button, False, False, 5)
        
    def tf_key_changed(self, tf):
        new_key = tf.get_text().strip()
        self.data[new_key] = self.data.pop(self.key)
        self.key = new_key
        
    def __create_action_entry(self, action):
        action = ActionEntry(action)
        action.connect("destroy", self.action_entry_destroy)
        return action
        
    def action_entry_destroy(self, entry_object):
        self.vbox.remove(entry_object)
        self.data[self.key][0].remove(entry_object.data)
        self.show_all()
    
    def add_action_button_clicked(self, button):
        self.data[self.key][0].append([self.data[self.key][0][0][0], self.data[self.key][0][0][1]])
        self.vbox.pack_start(self.__create_action_entry(self.data[self.key][0][len(self.data[self.key][0])-1]))
        self.show_all()
    
    def tf_mode_changed(self, tf):
        self.data[self.key][1] = tf.get_text().strip()
    
    def delete_button_clicked(self, button):
        del self.data[self.key]
        self.destroy()
