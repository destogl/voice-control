# -*- coding: latin-1 -*-
"""
Copyright 2012 Denis Štogl

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

import os

class Helpers():
    """ Helpers Class"""
    
    @staticmethod
    def write_in_file(file_path, data):
        filewriter = open(file_path, 'w')
        for string in data:
            filewriter.write(string)
        filewriter.close()
        
    @staticmethod
    def append_in_file(file_path, append_file_path):
        filewriter = open(file_path, 'a')
        filereader = open(append_file_path, 'r')
        filewriter.write(filereader.read())
        filereader.close()
        filewriter.close()
    
    @staticmethod
    def check_path(vc_dir, directory, create=False):
    
        paths = [
            os.environ['HOME'] + '/.voice-control/'+ directory + '/',
            vc_dir + '/' + directory + '/'
            ]
        
        dir_path = None
        for path in paths:
            if not dir_path:
                if os.path.isdir(path):
                    dir_path = path
                    break
        if not dir_path:
            if create:
                os.mkdir(paths[1], 744)
                dir_path = paths[1]
            else:
                raise Exception("Unable to continue: '%s' directory not found in '%s' nor '%s'!" % (directory, paths[0], paths[1]))
        
        return dir_path
    
    @staticmethod
    def __read_non_system_files(macros_dir, filenames):
        macros = {}
        for filename in filenames:
            if filename != 'system':
                macros[filename] = {}
                macrorc = open(macros_dir + filename)
                for line in macrorc:
                    if not (line.startswith('#') or line.startswith(' ')):
                        pieces = line.split('=')
                        if len(pieces) == 2:
                            if pieces[0] == 'Additional':
                                macros[filename][pieces[0]] = pieces[1]
                            else:
                                macros[filename][pieces[0]] = Helpers.__create_macro_from_action(pieces[1])
                macrorc.close()
        return macros
    
    @staticmethod
    def read_macros_directory(macros_dir, system_only=False):
        passwords = {}
        usernames = {}
        macros = {}
        
        macrorc = open(macros_dir + "passwords")
        for line in macrorc:
            if not (line.startswith('#') or line.startswith(' ')):
                passwords[line.strip()] = 'password'
        macrorc.close()
        
        macrorc = open(macros_dir + "usernames")
        for line in macrorc:
            if not (line.startswith('#') or line.startswith(' ')):
                pieces = line.split('=')
                usernames[pieces[0]] = pieces[1].strip()
        macrorc.close()
        
        macrorc = open(macros_dir + "system")
        for line in macrorc:
            if not (line.startswith('#') or line.startswith(' ')):
                if line.startswith('section'):
                    pieces = line.split(' ')
                    section = pieces[1].strip()
                    macros[section] = {}
                else:
                    pieces = line.split('=')
                    if len(pieces) == 2:
                        if section.startswith('window_manager') or section == 'system_wide':
                            macros[section][pieces[0]] = Helpers.__create_macro_from_action(pieces[1])
                        else:
                            macros[section][pieces[0]] = pieces[1].strip()
                            
        macrorc.close()
        if not system_only:
            macros['non_system'] = Helpers.__read_non_system_files(macros_dir, macros['shortcuts'].values())
            
        #print macros[filename]
        return macros, passwords, usernames
        
    @staticmethod
    def __create_macro_from_action(action):
        action_list = action.split(":")
        print action_list
        if len(action_list) == 3:
            macro = [action_list[1].strip(), action_list[0].strip(), action_list[2].strip()]
        else:
            macro = [action_list[1].strip(), action_list[0].strip(), '']
        return macro
