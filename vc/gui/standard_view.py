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
from vc.gui.generic_view import GenericView

class StandardView(GenericView):

    def __init__(self, logic, width, height):
        self.logic = logic
        
        super(StandardView, self).__init__(width, height)
        
        self.set_homogeneous(False)
        
        hbox = gtk.HBox(False)
        hbox.pack_start(gtk.Label("Mode: "))
        tf = gtk.Entry()
        entryBuff = gtk.EntryBuffer(logic.mode, -1)
        tf.set_buffer(entryBuff)
        tf.set_editable(False)
        #tf.connect("changed", self.tf_changed)
        self.logic.add_mode_status_output(tf)
        hbox.pack_start(tf)
        
        self.pack_start(hbox)
        
        # Text View
        hbox = gtk.HBox(False)
        hbox.pack_start(gtk.Label("Heard:"))
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        
        textbuf = gtk.TextBuffer()
        self.logic.add_output_on_gui(textbuf)
        
        text = gtk.TextView(textbuf)
        text.set_wrap_mode(gtk.WRAP_WORD)
        text.set_editable(False)
        text.set_cursor_visible(False)
        
        # Auto scroll ScrolledWindow
        text.connect('size-allocate', self.text_changed)
        
        self.scrolled_window.add(text)
        self.scrolled_window.get_vadjustment().set_upper(text.get_vadjustment().get_upper())
        hbox.pack_start(self.scrolled_window)
        self.pack_start(hbox)
        
        # Buttons box
        hbox = gtk.HBox()
        
        self.lis_button = gtk.ToggleButton("Start Listening")
        self.lis_button.connect('clicked', self.buttListen_clicked)
        hbox.pack_start(self.lis_button)
        
        button = gtk.Button("Update")
        button.connect('clicked', self.buttUpdate_clicked)
        hbox.pack_start(button)
        
        button = gtk.Button("Quit")
        button.connect('clicked', self.buttQuit_clicked)
        hbox.pack_start(button)
        
        self.pack_start(hbox)
    
    def tf_changed(self, entry):
        print entry.get_text()
        if entry.get_text() != 'system':
            self.lis_button.set_active(True)
            self.lis_button.set_label("Stop listening")
        else:
            self.lis_button.set_active(False)
            self.lis_button.set_label("Start Listening")
        
    # TODO make click event when is listening trough voice command activated
    def buttListen_clicked(self, button):
        """Handle button presses."""
        if button.get_active():
            button.set_label("Stop listening")
            self.logic.change_to_listening()
        else:
            button.set_label("Listening")
            self.logic.change_to_system()
    
    def buttUpdate_clicked(self, button):
        self.logic.update_dictionaries()
        
    def buttQuit_clicked(self, button):
        self.logic.app_quit()
        
    def text_changed(self, widget, event, data=None):
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value( adj.upper - adj.page_size )
