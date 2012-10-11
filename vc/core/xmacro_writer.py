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

import subprocess

# http://download.sarine.nl/xmacro/Description.html
class XmacroWriter():
    
    # From /usr/include/X11/keysymdef.h
    __ALL_KEYS = {
                'Backspace': 'BackSpace',
                'BackSpace': 'BackSpace',
                'Tab': 'Tab',
                'Enter': 'Return',
                'Return': 'Return',
                'Pause': 'Pause',
                'ScrollLock': 'Scroll_Lock',
                'Escape': 'Escape',
                'Esc': 'Escape',
                'Del': 'Delete',
                'Delete': 'Delete',
                
                'Home': 'Home',
                'ArrowLeft': 'Left',
                'ArrowUp': 'Up',
                'ArrowRight': 'Right',
                'ArrowDown': 'Down',
                'Previous': 'Prior',
                'PageUp': 'Page_Up',
                'Next': 'Next',
                'PageDown': 'Page_Down',
                'End': 'End',
                'Begin': 'Begin',
                
                'Select': 'Select',
                'Mark:': 'Select',
                'PrintScr': 'Print',
                'Execute': 'Execute',
                'Run': 'Execute',
                'Do': 'Execute',
                'Ins': 'Insert',
                'Undo': 'Undo',
                'Redo': 'Redo',
                'Again': 'Redo',
                'Menu': 'Menu',
                'Find': 'Find',
                'Cancel': 'Cancel',
                'Help': 'Help',
                'Break': 'Break',
                'NumLock': 'Num_Lock',
                
                'Shift': 'Shift_L',
                'Shift_R': 'Shift_R',
                'Control': 'Control_L',
                'Ctrl': 'Control_L',
                'Control_R': 'Control_R',
                'Ctrl_R': 'Control_R',
                'Capslock': 'Caps_Lock',
                'CapsLock': 'Caps_Lock',
                'Shiftlock': 'Shift_lock',
                'ShiftLock': 'Shift_lock',
                'Alt': 'Alt_L',
                'Alt_R': 'Alt_R',
                'Super': 'Super_L',
                'Super_r': 'Super_R',
                
                'Space': 'space',
                '"': 'exclam',
                '?': 'quotedbl',
                '#': 'numbersign',
                '$': 'dollar',
                '%': 'percent',
                '&': 'ampersand',
                "'": 'apostrophe',
                '(': 'parenleft',
                ')': 'parenright',
                '*': 'asterisk',
                '+': 'plus',
                ',': 'comma',
                '-': 'minus',
                '.': 'period',
                '/': 'slash',
                
                ':': 'hotkey:hotkey:hotkey:colon',
                ';': 'semicolon',
                '<': 'less',
                '=': 'equal',
                '>': 'greater',
                '?': 'question',
                '@': 'at',
                
                '[': 'bracketleft',
                "\\": 'backslash',
                ']': 'bracketright',
                '^': 'asciicircum',
                '_': 'underscore',
                '`': 'grave',
                
                '{': 'braceleft',
                '|': 'bar',
                '}': 'braceright',
                '~': 'asciitilde',
                

                '°': 'degree',
                '^1': 'onesuperior',
                '^2': 'twosuperior',
                '^3': 'threesuperior',
                '1/4': 'onequarter',
                '1/2': 'onehalf',
                '3/4': 'threequarters',
                
                '0': '0',
                '1': '1',
                '2': '2',
                '3': '3',
                '4': '4',
                '5': '5',
                '6': '6',
                '7': '7',
                '8': '8',
                '9': '9',
                
                'A': 'A',
                'B': 'B',
                'C': 'C',
                'D': 'D',
                'E': 'E',
                'F': 'F',
                'G': 'G',
                'H': 'H',
                'I': 'I',
                'J': 'J',
                'K': 'K',
                'L': 'L',
                'M': 'M',
                'N': 'N',
                'O': 'O',
                'P': 'P',
                'Q': 'Q',
                'R': 'R',
                'S': 'S',
                'T': 'T',
                'U': 'U',
                'V': 'V',
                'W': 'W',
                'X': 'X',
                'Y': 'Y',
                'Z': 'Z',
                
                'a': 'a',
                'b': 'b',
                'c': 'c',
                'd': 'd',
                'e': 'e',
                'f': 'f',
                'g': 'g',
                'h': 'h',
                'i': 'i',
                'j': 'j',
                'k': 'k',
                'l': 'l',
                'm': 'm',
                'n': 'n',
                'o': 'o',
                'p': 'p',
                'q': 'q',
                'r': 'r',
                's': 's',
                't': 't',
                'u': 'u',
                'v': 'v',
                'w': 'w',
                'x': 'x',
                'y': 'y',
                'z': 'z',
                
                'F1':'F1',
                'F2':'F2',
                'F3':'F3',
                'F4':'F4',
                'F5':'F5',
                'F6':'F6',
                'F7':'F7',
                'F8':'F8',
                'F9':'F9',
                'F10':'F10',
                'F11':'F11',
                'F11':'F12',
                }
                
    __xmacro_pipe = None
                
    def __init__(self):
        devnull = open('/dev/null', 'w')
        xmacro = subprocess.Popen(["xmacroplay", ":0",],stdin=subprocess.PIPE,stdout=devnull,bufsize=1,close_fds=True)
        self.__xmacro_pipe = xmacro.stdin
        
    def keyboard_action(self, hotkey):
        for shortcut in hotkey.split("|"):
            self.__write(self.__parse_shortcut(shortcut.strip()))
    
    def write_string(self, string):
        self.__write("String " + string + "\n")
        
    def mouse_action(self, keys):
        action = ""
        keys_list = keys.split("|")
        keys_list[0] = keys_list[0].strip()
        if len(keys_list[0]) == 1:
            action = "ButtonPress " + keys_list[0] + "\n"
        if len(keys_list) == 2:
            action += "ButtonRelease " + keys_list[1].strip() + "\n"
        #print action
        self.__write(action)
        
    def __write(self, command):
        self.__xmacro_pipe.write(command)
        
    def __parse_shortcut(self, shortcut):
        if shortcut.startswith("+"):
            parts_list[0] = shortcut[1]
            if len(shortcut) > 1:
                parts_list[1] = shortcut[2:len(shortcut)]
        else:
            parts_list = shortcut.split("+", 1)
            
        parts_list[0] = parts_list[0].strip()
        
        if len(parts_list) == 2:
            key = ("KeyStrPress " + self.__ALL_KEYS[parts_list[0]] + "\n"
                + self.__parse_shortcut(parts_list[1].strip())
                + "KeyStrRelease " + self.__ALL_KEYS[parts_list[0]] + "\n"
                )
        else:
            key = "KeyStr " + self.__ALL_KEYS[parts_list[0]] + "\n"
            
        return key
