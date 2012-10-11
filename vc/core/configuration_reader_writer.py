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

from vc.core.helpers import Helpers
from collections import OrderedDict

class ConfigurationReaderWriter():
    
    __COMMENT_MARKER = '#'
    __COMMAND_SPLITTER = '='
    __ACTION_SPLITTER = ';'
    __ACTION_TYPE_SPLITTER = ':'
    __MODE_SPLITTER = '$'
    
    @staticmethod
    def __read_non_system_files(macros_dir, filenames):
        macros = OrderedDict()
        for filename in filenames:
            if filename != 'system':
                macros[filename] = OrderedDict()
                macrorc = open(macros_dir + filename)
                for line in macrorc:
                    if not (line.startswith(ConfigurationReaderWriter.__COMMENT_MARKER) or line.startswith(' ')):
                        pieces = line.split(ConfigurationReaderWriter.__COMMAND_SPLITTER)
                        if len(pieces) == 2:
                            if pieces[0] == 'Additional':
                                macros[filename][pieces[0]] = pieces[1]
                            else:
                                macros[filename][pieces[0]] = ConfigurationReaderWriter.__create_macro_from_action(pieces[1])
                macrorc.close()
        return macros
    
    @staticmethod
    def read_macros_directory(macros_dir, system_only=False):
        passwords = OrderedDict()
        usernames = OrderedDict()
        macros = OrderedDict()
        
        macrorc = open(macros_dir + "passwords")
        for line in macrorc:
            if not (line.startswith(ConfigurationReaderWriter.__COMMENT_MARKER) or line.startswith(' ')):
                passwords[line.strip()] = 'password'
        macrorc.close()
        
        #passwords = OrderedDict(sorted(passwords.items(), key=lambda t: t[0]))
        
        macrorc = open(macros_dir + "usernames")
        for line in macrorc:
            if not (line.startswith(ConfigurationReaderWriter.__COMMENT_MARKER) or line.startswith(' ')):
                pieces = line.split(ConfigurationReaderWriter.__COMMAND_SPLITTER)
                usernames[pieces[0]] = pieces[1].strip()
        macrorc.close()
        
        macrorc = open(macros_dir + "system")
        for line in macrorc:
            if not (line.startswith(ConfigurationReaderWriter.__COMMENT_MARKER) or line.startswith(' ')):
                if line.startswith('section'):
                    pieces = line.split(' ')
                    section = pieces[1].strip()
                    macros[section] = OrderedDict()
                else:
                    pieces = line.split(ConfigurationReaderWriter.__COMMAND_SPLITTER)
                    if len(pieces) == 2:
                        if section.startswith('window_manager') or section == 'system_wide':
                            macros[section][pieces[0]] = ConfigurationReaderWriter.__create_macro_from_action(pieces[1])
                        else:
                            macros[section][pieces[0]] = pieces[1].strip()
                            
        macrorc.close()
        if not system_only:
            macros['non_system'] = ConfigurationReaderWriter.__read_non_system_files(macros_dir, macros['shortcuts'].values())
            
        return macros, passwords, usernames
        
    @staticmethod
    def __create_macro_from_action(string):
        action_mode_list = string.split(ConfigurationReaderWriter.__MODE_SPLITTER)
        if len(action_mode_list) == 1:
            action_mode_list.append('')
        
        action_list = action_mode_list[0].split(ConfigurationReaderWriter.__ACTION_SPLITTER)
        actions = []
        for action in action_list:
            action_parts = action.split(ConfigurationReaderWriter.__ACTION_TYPE_SPLITTER)
            actions.append([action_parts[0].strip(), action_parts[1].strip()])
        
        return [actions, action_mode_list[1].strip()]
        
    @staticmethod
    def write_macros_directory(macros_dir, macros, passwords = None, usernames = None):
        if passwords != None:
            Helpers.write_in_file(macros_dir + "passwords", passwords.keys())
        
        if usernames != None:
            Helpers.write_in_file(macros_dir + "usernames", ConfigurationReaderWriter.__create_list_of_system_actions(usernames))
        
        system_file = macros_dir + "system"
        Helpers.write_in_file(system_file, '')
        for key in macros.keys():
            if key == 'non_system':
                for non_system_key in macros['non_system'].keys():
                    Helpers.write_in_file(macros_dir + non_system_key, ConfigurationReaderWriter.__create_list_of_actions(macros['non_system'][non_system_key]))
            else:
                Helpers.append_in_file(system_file, "section " + key + "\n")
                if key.startswith('window_manager') or key == 'system_wide':
                    Helpers.append_in_file(system_file, ConfigurationReaderWriter.__create_list_of_actions(macros[key]))
                else:
                    Helpers.append_in_file(system_file, ConfigurationReaderWriter.__create_list_of_system_actions(macros[key]))
            
        
    @staticmethod
    def __create_list_of_system_actions(macros):
        actions = []
        for key in macros.keys():
            actions.append(key + ConfigurationReaderWriter.__COMMAND_SPLITTER + macros[key] + "\n")
        
        return actions
    
    @staticmethod
    def __create_list_of_actions(macros):
        actions = []
        for key in macros.keys():
            if key == 'Additional':
                string = key + ConfigurationReaderWriter.__COMMAND_SPLITTER + macros[key]
            else:
                actions_list, mode = macros[key]
                string = key + ConfigurationReaderWriter.__COMMAND_SPLITTER
                for idx, action in enumerate(actions_list):
                    if idx == 0:
                        string += action[0] + ConfigurationReaderWriter.__ACTION_TYPE_SPLITTER + action[1]
                    else:
                        string += ConfigurationReaderWriter.__ACTION_SPLITTER + action[0] + ConfigurationReaderWriter.__ACTION_TYPE_SPLITTER + action[1]
                if mode != '':
                    string += ConfigurationReaderWriter.__MODE_SPLITTER + mode
            actions.append(string + "\n")
        
        return actions
