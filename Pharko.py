import sublime
import sublime_api
import sublime_plugin
import sys #for finding python version
import subprocess #for running terminal commands
import os
import sys
import json
import html
import collections
import tempfile
import traceback
import pprint
import shutil #for copying files/dirs

pp = pprint.PrettyPrinter(indent=4)
PY3 = sys.version > '3'

if PY3:
    import urllib.request as urllib
    from .src.PharkoLoadedCommand import PharkoLoadedCommand
    from .src.PharkoTextCommand import PharkoTextCommand
    from .src.PharkoPanelCommand import PharkoPanelCommand
    from .src.PharkoSampleCommand import PharkoSampleCommand
else:
    import urllib2 as urllib
    from src.PharkoLoadedCommand import PharkoLoadedCommand
    from src.PharkoTextCommand import PharkoTextCommand
    from src.PharkoPanelCommand import PharkoPanelCommand
    from src.PharkoSampleCommand import PharkoSampleCommand

## Current files path
PLUGIN_PATH = os.path.abspath(os.path.dirname(__file__))
## All packages path
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(PLUGIN_PATH)
PACKAGES_PATH = os.path.join(PACKAGES_PATH, 'Pharkos')

def plugin_loaded():
    PharkoLoadedCommand.isThisPluginLoaded()

## Runs the terminal command 'ls -la'
## Inserts the contents on the first line of the file
class PharkoListCommand(sublime_plugin.TextCommand):
    staticIsPluginLoaded = False
    def on_done(self, index):

        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return
        # if user picks from list, return the correct entry
        self.view.run_command("pharko_list", {"args":{'text': self.list[index]}})

    def run(self, edit, args={}):
        # pp.pprint(args)
        PharkoLoadedCommand.isThisPluginLoaded()

        # Copy sample php snippets if necessary
        samplePHPSnippets = PACKAGES_PATH + '/php'
        if not os.path.isdir(samplePHPSnippets):
            shutil.copytree(PLUGIN_PATH + '/php', samplePHPSnippets)

        location = ""
        if len(args):
            location = args['text']
        # command = ["ls", "-la", PLUGIN_PATH]
        command = ["php", PLUGIN_PATH + "/pharko.phar", "dir", "--base=" + PACKAGES_PATH, location]

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response, _ = process.communicate()
        returncode = process.returncode
        response = response.decode('utf-8')
        response = json.loads(response)

        if (response['type'] == 'list'):
            # this will populate the quick_panel
            self.list = response['data']

            # show_quick_panel(items, on_done, <flags>, <default_index>)
            # ref: http://www.sublimetext.com/forum/viewtopic.php?f=4&t=7139
            # take the list, and place it in a quick_panel, make 3rd item
            # default pick

            self.view.window().show_quick_panel(self.list, self.on_done, 1, 0)
        elif (response['type'] == 'snippet'):
            self.view.run_command("insert_snippet", { "name": "Packages/Pharkos/" + response['data']})
            self.view.window().run_command("pharko_panel", response) #works too
        elif (response['type'] == 'file'):
            self.view.run_command("insert_snippet", {'contents': response['data']})
