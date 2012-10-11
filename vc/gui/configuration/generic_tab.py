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

class GenericTab(gtk.VBox):

    def __init__(self):
        super(GenericTab, self).__init__()
        
        self.vbox = gtk.VBox()
        
        self.sw = gtk.ScrolledWindow()
        self.sw.set_border_width(10)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        
        self.sw.add_with_viewport(self.vbox)
        self.pack_start(self.sw)
        
    def add(self, child):
        self.vbox.pack_start(child)
