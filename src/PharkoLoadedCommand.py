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

class PharkoLoadedCommand:
    staticIsPluginLoaded = False

    @staticmethod
    def isThisPluginLoaded():
        if not PharkoLoadedCommand.staticIsPluginLoaded:
            PharkoLoadedCommand.staticIsPluginLoaded = True
            PharkoLoadedCommand.toggleThisConsole()
            PharkoLoadedCommand.createThisPackageFolder()
        return True

    @staticmethod
    def toggleThisConsole():
        window = sublime.active_window()
        window.run_command("show_panel", {"panel": "console", "toggle": True})

    @staticmethod
    def createThisPackageFolder():
        ## All packages path
        PACKAGES_PATH = sublime.packages_path() + '/Pharkos'
        if not os.path.isdir(PACKAGES_PATH):
            print('Creating the folder, ' + PACKAGES_PATH)
            try:
                os.makedirs(PACKAGES_PATH)
                print('Folder created, ' + PACKAGES_PATH)
            except OSError:
                if not os.path.isdir(PACKAGES_PATH):
                    print('Please create the folder, ' + PACKAGES_PATH)
                    raise
