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
from vc.gui.configuration.label_text_field import LabelTextField

class PropertiesSystemSection(gtk.Frame):

    def __init__(self, name, data):
        self.data = data
        
        super(PropertiesSystemSection, self).__init__(name)
        
        vbox = gtk.VBox()
        for key in self.data.keys():
            vbox.pack_start(LabelTextField(data, key))
            
        self.add(vbox)
