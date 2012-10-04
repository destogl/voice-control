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

from helpers import Helpers

class SentencesGenerator():

    @staticmethod
    def generate_sentences_files(sentences_dir, macros, passwords, usernames):
        
        sentences = SentencesGenerator.__create_system_sentences(macros, passwords, usernames)
        Helpers.write_in_file(sentences_dir + 'system', sentences.keys())
        
        for value in macros['shortcuts'].values():
            if value != 'system':
                if value in macros['special_states'].values():
                    sentences = SentencesGenerator.__create_special_states_sentences(macros['non_system'][value])
                else:
                    sentences = SentencesGenerator.__create_other_sentences(macros, macros['non_system'][value])
                Helpers.write_in_file(sentences_dir + value, sentences.keys())
                
        for value in macros['shortcuts'].values():
            if value != 'system':
                if 'Additional' in macros['non_system'][value]:
                    for append_file_name in macros['non_system'][value]['Additional'].split(','):
                        Helpers.append_in_file(sentences_dir + value, sentences_dir + append_file_name.strip())
        
    @staticmethod
    def __create_system_sentences(macros, passwords, usernames):
        
        sentences = {}
        
        sentences[macros['system']['NAME'] + "\n"] = 1
        if macros['system']['START_COMMAND'] != "":
            sentences[macros['system']['NAME'] + " " + macros['system']['START_COMMAND'] + "\n"] = 1
        sentences[macros['system']['NAME'] + " " + macros['system']['STOP_COMMAND'] + "\n"] = 1
        sentences[macros['system']['NAME'] + " " + macros['system']['CLOSE_COMMAND'] + "\n"] = 1
        sentences[macros['system']['NAME'] + " " + macros['system']['UPDATE_COMMAND'] + "\n"] = 1
            
        for key in macros['shortcuts'].keys():
            sentences[macros['system']['USE'] + " " + key + "\n"] = 1
            
        for key in macros['applications'].keys():
            sentences[macros['system']['START'] + " " + key + "\n"] = 1
            sentences[macros['system']['NAME'] + " " + macros['system']['CLOSE'] + " " + key + "\n"] = 1
            
        for key in macros['window_manager_desktop_names'].keys():
            sentences[macros['system']['FOCUS'] + " " + key + "\n"] = 1
            
        for key in macros['window_manager_shortcuts'].keys():
            sentences[key + "\n"] = 1
            
        for key in macros['system_wide'].keys():
            sentences[key + "\n"] = 1
            
        for key in passwords.keys():
            sentences[macros['system']['PASSWORD_COMMAND'] + " " + key + "\n"] = 1
            
        for key in usernames.keys():
            sentences[macros['system']['USERNAME_COMMAND'] + " " + key + "\n"] = 1

        return sentences
        
    @staticmethod
    def __create_other_sentences(macros, non_system_macros):
        
        sentences = {}
        
        sentences[macros['system']['NAME'] + "\n"] = 1
        sentences[macros['system']['NAME'] + " " + macros['system']['STOP_COMMAND'] + "\n"] = 1
        
        for key in macros['shortcuts'].keys():
            sentences[macros['system']['USE'] + " " + key + "\n"] = 1
            
        for key in macros['window_manager_desktop_names'].keys():
            sentences[macros['system']['FOCUS'] + " " + key + "\n"] = 1
            
        for key in macros['system_wide'].keys():
            sentences[key + "\n"] = 1
            
        for key in non_system_macros.keys():
            if key != 'Additional':
                sentences[key + "\n"] = 1
            
        return sentences
        
    @staticmethod
    def __create_special_states_sentences(non_system_macros):
        
        sentences = {}
        
        for key in non_system_macros.keys():
            if key != 'Additional':
                sentences[key + "\n"] = 1
            
        return sentences
