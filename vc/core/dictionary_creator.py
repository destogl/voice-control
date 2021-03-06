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

import mechanize

class DictionaryCreator():

    @staticmethod
    def create_dictionaries_and_models(macros, sentences_dir, dictionaries_dir, models_dir):
        
        if not ('system' in macros['shortcuts'].values()):
            macros['shortcuts']['system'] = 'system'
        
        browser = mechanize.Browser()
        
        for filename in macros['shortcuts'].values():
            browser.open("http://www.speech.cs.cmu.edu/tools/lmtool-new.html")
            browser.select_form(nr=0)
            browser.form.add_file(open(sentences_dir + filename), 'text/plain', sentences_dir + filename) 
            browser.submit()
            for link in browser.links():
                if link.url.endswith(".dic"):
                    mechanize.urlretrieve(link.base_url  + link.url, dictionaries_dir + filename + ".dic")
                if link.url.endswith(".lm"):
                    mechanize.urlretrieve(link.base_url + link.url, models_dir + filename + ".lm")
