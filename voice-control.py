#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Copyright 2012 Denis Stogl

Based on Sphinxkeys software Copyright 2011 Eric Worden. Licenced under GNU Licence.
(see: http://code.google.com/p/sphinxkeys/)

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

import pygtk
pygtk.require('2.0')
import gtk
from optparse import OptionParser
import os, sys
from vc.core.logic import Logic
from vc.gui.window import Window
from vc.core.helpers import Helpers
from vc.core.configuration_reader_writer import ConfigurationReaderWriter
#TODO use logging
#import logging

class VoiceControl(object):

    def __init__(self):
        # TODO maybe remove parser in new file
        parser = OptionParser()
        parser.add_option("-q", "--quiet", dest="quiet", action='store_true', default=False, help="Don't print anything")
        parser.add_option("-g", "--generate", dest="generate", action='store_true', default=False, help="Force generating sentences and dictionaries")
        parser.add_option("-s", "--no_sound", dest="espeak_output", action='store_false', default=True, help="No espeak audio messages")
        parser.add_option("-c", "--create_conf_files", dest="create_conf_files", action='store_true', default=False, help="Create inital configuration files")
        (self.options, args) = parser.parse_args()
        
        vc_dir = os.path.dirname(sys.argv[0])
        if vc_dir == '':
            vc_dir = '.'
        
        # Check system core files
        try:
            default_macros_dir = Helpers.check_path(vc_dir, 'macros')
            if not os.path.exists(default_macros_dir + 'system'):
                raise Exception("Unable to continue: System macro file don't exist in %s!" % (default_macros_dir))
            if not os.path.exists(default_macros_dir + 'passwords'):
                raise Exception("Unable to continue: Passwords macro file don't exist in %s!" % (default_macros_dir))
            if not os.path.exists(default_macros_dir + 'usernames'):
                raise Exception("Unable to continue: User-names macro file don't exist in %s!" % (default_macros_dir))
        except Exception as message:
            print(message)
            sys.exit(1)
        
        vc_conf_dir = Helpers.check_path(os.environ['HOME'], '.voice-control', True)
        self.macros_dir = Helpers.check_path(vc_conf_dir, 'macros', True)
        self.sentences_dir = Helpers.check_path(vc_conf_dir, 'sentences', True)
        self.dictionaries_dir = Helpers.check_path(vc_conf_dir, 'dictionaries', True)
        self.models_dir = Helpers.check_path(vc_conf_dir, 'models', True)
        
        # Check if status file exist if not then is first run
        status_file = vc_conf_dir + 'mode'
        if not os.path.exists(status_file) or self.options.create_conf_files:
            print "Starting first time: Creating macro-files"
            Helpers.write_in_file(status_file, '')
            macros, passwords, usernames = ConfigurationReaderWriter.read_macros_directory(default_macros_dir)
            ConfigurationReaderWriter.write_macros_directory(self.macros_dir, macros, passwords, usernames)
        
        self.logic = Logic(self.options, status_file, self.macros_dir, self.sentences_dir, self.dictionaries_dir, self.models_dir)
        self.window = Window(self.logic)


app = VoiceControl()
gtk.main()
