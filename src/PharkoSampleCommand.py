import sublime
import sublime_plugin
import sys #for finding python version
import subprocess #for running terminal commands
import os
import sys
import json
import tempfile
import traceback
import pprint
import datetime

pp = pprint.PrettyPrinter(indent=4)
PY3 = sys.version > '3'

if PY3:
    import urllib.request as urllib
    from .PharkoLoadedCommand import PharkoLoadedCommand
else:
    import urllib2 as urllib
    from PharkoLoadedCommand import PharkoLoadedCommand

## As you type characters, a word is calculated by encountering first space char
## This then replace the found word with its capitalized version
class PharkoSampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        PharkoLoadedCommand.isThisPluginLoaded()

        sel = self.view.sel()[0]
        counter = 1;
        indexLess = sel.a
        while indexLess > 0:
            substring = self.view.substr(sublime.Region(sel.begin() - counter, indexLess))
            if substring.isspace():
                break
            indexLess = indexLess -1
            counter = counter + 1

        region = sublime.Region(indexLess, sel.begin())
        keyword = self.view.substr(region)
        keyword = keyword.capitalize()
        # self.view.sel()[0].a === region.a
        # self.view.sel()[0].b === region.b
        # Replace the selection with transformed text
        self.view.erase(edit, region)
        self.view.insert(edit, region.a, keyword)

        print(keyword, region)
