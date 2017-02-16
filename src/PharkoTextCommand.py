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
else:
    import urllib2 as urllib

class PharkoTextCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):

        # add this to insert at current cursor position
        # http://www.sublimetext.com/forum/viewtopic.php?f=6&t=11509

        self.view.insert(edit, self.view.sel()[0].begin(), args['text'])
