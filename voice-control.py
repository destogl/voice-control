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
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst
import getpass, os
import subprocess, sys
from optparse import OptionParser
from vc.helpers import Helpers
from vc.sentences_generator import SentencesGenerator
from vc.dictionary_creator import DictionaryCreator
from vc.xmacro_writer import XmacroWriter
#TODO use logging
#import logging

class VoiceControl(object):

    __SYSTEM = 'system'
    __LISTENING = 'listening'
    __OFF = 'off'
    
    def __init__(self):
        #TODO maybe remove parser in new file
        parser = OptionParser()
        parser.add_option("-q", "--quiet", dest="quiet", action='store_true', default=False, help="Don't print anything")
        parser.add_option("-g", "--generate", dest="generate", action='store_true', default=False, help="Force generating sentences and dictionaries")
        parser.add_option("-s", "--no_sound", dest="espeak_output", action='store_false', default=True, help="No espeak audio messages")
        (self.options, args) = parser.parse_args()
        
        vc_dir = os.path.dirname(sys.argv[0])
        if vc_dir == '':
            vc_dir = '.'
        
        try:
            self.macros_dir = Helpers.check_path(vc_dir, 'macros')
            if not os.path.exists(self.macros_dir + 'system'):
                raise Exception("Unable to continue: System macro file don't exist in %s!" % (self.macros_dir))
            if not os.path.exists(self.macros_dir + 'passwords'):
                raise Exception("Unable to continue: Passwords macro file don't exist in %s!" % (self.macros_dir))
            if not os.path.exists(self.macros_dir + 'usernames'):
                raise Exception("Unable to continue: User-names macro file don't exist in %s!" % (self.macros_dir))
        except Exception as message:
            print(message)
            sys.exit(1) 
        
        #TODO read this form configuration file
        self.mode = self.__SYSTEM
        self.default_macro_file = 'system'
        self.status_file = os.environ['HOME'] + '/.voice-control/mode'
        Helpers.write_in_file(self.status_file, self.mode)
        self.previous_hyp = ""
        
        self.init_macros()
        
        self.sentences_dir = Helpers.check_path(vc_dir, 'sentences', True)
        self.dictionaries_dir = Helpers.check_path(vc_dir, 'dictionaries', True)
        self.models_dir = Helpers.check_path(vc_dir, 'models', True)
       
        if self.options.generate or not os.listdir(self.sentences_dir) or not os.listdir(self.dictionaries_dir) or not os.listdir(self.models_dir):
            print("Santences and dictionaries will be created")
            SentencesGenerator.generate_sentences_files(self.sentences_dir, self.macros, self.passwords, self.usernames)
            DictionaryCreator.create_dictionaries_and_models(self.macros, self.sentences_dir, self.dictionaries_dir, self.models_dir)
                
        self.xmacro_writer = XmacroWriter()
        #TODO espeak as subprocess
#        espeak = subprocess.Popen("espeak -v " + self.macros['properties']['LANG'] , stdin=subprocess.PIPE, stdout=devnull, bufsize=1, close_fds=True)
#        self.espeak_pipe = espeak.stdin
        
        self.init_gst(self.default_macro_file) # or self.mode --- the names are the same
        
        self.say("I am ready for taking commands")

    def init_macros(self):
        """Read macro configurations from macro folders"""
        self.macros = {}
        self.passwords = {}
        self.usernames = {}
        self.macros, self.passwords, self.usernames = Helpers.read_macros_directory(self.macros_dir)
#        print self.macros
#        print self.passwords
        if len(self.passwords) > 0:
            self.password_input()

    def password_input(self):
        """User inputs passwords."""
        for password_key in self.passwords:
            match = False
            while match == False:
                prompt = "\nEnter password for %s: " % password_key
                password1 = getpass.getpass(prompt)
                prompt = "\nConfirm password for %s: " % password_key
                password2 = getpass.getpass(prompt)
                if password1 == password2:
                    match = True
                    self.passwords[password_key] = password1
                    self.macros["PASSWORD " + password_key] = "String %s\n" % password1
                else:
                    print "\nPasswords don't match. Try again."

    def init_gst(self, file_name):
        """Initialize the speech components"""
        self.pipeline = gst.parse_launch('alsasrc ! audioconvert ! audioresample '
                                         + '! vader name=vad auto-threshold=true '
                                         + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')
        asr.set_property('lm', self.models_dir + file_name + '.lm')
        asr.set_property('dict', self.dictionaries_dir + file_name + '.dic')
        asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)
        asr.set_property('configured', True)
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.application_message)
        self.pipeline.set_state(gst.STATE_PLAYING)

    def asr_partial_result(self, asr, text, uttid):
        """Forward partial result signals on the bus to the main thread."""
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def asr_result(self, asr, text, uttid):
        """Forward result signals on the bus to the main thread."""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def application_message(self, bus, msg):
        """Receive application messages from the bus."""
        #TODO Check partial resoult - but why?
        msgtype = msg.structure.get_name()
        if msgtype == 'result':
            self.final_result(msg.structure['hyp'], msg.structure['uttid'])
            

    def final_result(self, hyp, uttid):
        """Decide what to do with the heard words."""
        if not self.options.quiet:
            print 'Heard: "%s"' % hyp
            self.send_notification('Heard: "%s"' % hyp)
        word_list = hyp.split(' ', 1)
        word_count = len(word_list)
        if word_count > 0 and not (word_list[0] == ""):
        
            # Main control with NAME
            if word_list[0] == self.macros['system']['NAME']:
                if self.mode == self.__SYSTEM and self.macros['system']['START_COMMAND'] == "" and word_count == 1:
                            self.change_mode(self.__LISTENING)
                            self.say_and_send_notification("I listen")
                if word_count > 1:
                    word_list = word_list[1].split()
                    if self.mode == self.__SYSTEM:
                        if word_list[0] == self.macros['system']['START_COMMAND']:
                            self.change_mode(self.__LISTENING)
                            self.say_and_send_notification("I listen")
                        elif word_list[0] == self.macros['system']['CLOSE']:
                            self.execute_command("killall -3 " + self.macros['applications'][word_list[1]])
                            self.say_and_send_notification("Closing application for " + word_list[1] + " " + self.macros['applications'][word_list[1]])
                        elif word_list[0] == self.macros['system']['CLOSE_COMMAND']:
                            self.say_and_send_notification("Goodbye " + self.macros['properties']['USER'])
                            sys.exit()
                        elif self.macros['system']['START_COMMAND'] == "":
                            self.change_mode(self.__LISTENING)
                            self.say_and_send_notification("I am listening")
                    elif word_list[0] == self.macros['system']['STOP_COMMAND']:
                        self.change_mode(self.__SYSTEM, True)
                        self.say_and_send_notification("I am stopping listening")
                
            if self.mode != self.__SYSTEM and word_list[0] != self.macros['system']['NAME']:
                if word_list[0] == self.macros['system']['START'] and self.mode == self.__LISTENING:
                    self.execute_command(self.macros['applications'][word_list[1]])
                    self.say_and_send_notification("Opening application for " + word_list[1] + " " + self.macros['applications'][word_list[1]])
                # TODO write function for search in special dictionaries
                # Standard usage
                elif word_list[0] == self.macros['system']['FOCUS']:
                    action, function, mode = self.macros['window_manager_desktop_names'][word_list[1]]
                    self.functions[function](self, action)
                    if mode != '':
                        self.change_mode(self.macros['shortcuts'][mode], True)
                        self.say_and_send_notification("Now using " + self.macros['shortcuts'][mode] + " shortcuts set")
                    
                elif word_list[0] == self.macros['system']['USE']:
                    self.change_mode(self.macros['shortcuts'][word_list[1]], True)
                    self.say_and_send_notification("Now using " + self.macros['shortcuts'][word_list[1]] + " shortcuts set")
                    if self.macros['shortcuts'][word_list[1]] == 'system':
                        self.change_mode(self.__LISTENING)
                
                # System wide shortcuts
                elif hyp in self.macros['system_wide'].keys():
                    action, function, mode = self.macros['system_wide'][hyp]
                    self.functions[function](self, action)
                    if mode != '':
                        self.change_mode(self.macros['shortcuts'][mode], True)
                        self.send_notification("Now using " + self.macros['shortcuts'][mode] + " shortcuts set")
                    
                #Password and user-name writer
                elif self.mode == self.__LISTENING:
                    if word_list[0] == self.macros['system']['PASSWORD_COMMAND']:
                        self.xmacro_writer.write_string(self.passwords[word_list[1]])
                    if word_list[0] == self.macros['system']['USERNAME_COMMAND']:
                        self.xmacro_writer.write_string(self.usernames[word_list[1]])
                        self.hotkey('Tab')
                
                # WM shortcuts
                elif self.mode == self.__LISTENING or self.mode == self.__SYSTEM:
                    action, function, mode = self.macros['window_manager_shortcuts'][hyp]
                    self.functions[function](self, action)
                    
                elif self.mode != self.__LISTENING and self.mode != self.__SYSTEM:
                    action, function, mode = self.macros['non_system'][self.mode][hyp]
                    self.functions[function](self, action)
                    if mode != '':
                        self.change_mode(self.macros['shortcuts'][mode], True)
                        self.say_and_send_notification("Now using " + self.macros['shortcuts'][mode] + " shortcuts set")

#    def 

    def change_mode(self, mode, load_file = False):
        self.mode = mode
        Helpers.write_in_file(self.status_file, self.mode)
        if load_file:
            self.pipeline.set_state(gst.STATE_NULL)
#            if self.mode == self.__LISTENING:
#                self.init_gst(self.__SYSTEM)
#            else:
            self.init_gst(self.mode)
    
    def say_and_send_notification(self, message):
        self.send_notification(message)
        self.say(message)
    
    def say(self, message):
        if self.options.espeak_output:
#            self.espeak_pipe.write(" '" + message + "'")
            command = "espeak -v " + self.macros['properties']['LANG'] + " '" + message + "'"
            self.execute_command(command)
    
    def send_notification(self, message):
        self.execute_command("notify-send VOICE-CONTROL '" + message + "'")
    
    def hotkey(self, shortcut_set):
        self.xmacro_writer.keyboard_action(shortcut_set)
        
    def execute_command(self, command):
        if not command.endswith("&"):
            command += " &"
        subprocess.call(command, shell=True)
        
    def mouse(self, key):
        self.xmacro_writer.mouse_action(key)
    
    def print_string(self, string):
        self.xmacro_writer.write_string(string)
    
    functions = {
                'hotkey': hotkey,
                'cmd': execute_command,
                'mouse': mouse,
                'string': print_string,
                }

app = VoiceControl()
gtk.main()
