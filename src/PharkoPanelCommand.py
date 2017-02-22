import sublime
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
    from .PharkoLoadedCommand import PharkoLoadedCommand
else:
    import urllib2 as urllib
    from PharkoLoadedCommand import PharkoLoadedCommand

class PharkoPanelCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        title = ''
        docs = ''
        code = ''
        for a in kwargs:
            if a == 'title':
                title = html.escape(kwargs[a], quote=False)
            if a == 'docs':
                docs = html.escape(kwargs[a], quote=False)
            if a == 'code':
                code = kwargs[a]

        docs = "<br />".join(docs.split("\n"))
        code = "&nbsp;".join(html.escape(code, quote=False).split(" "))
        code = "<br />".join(code.split("\n"))

        view = self.window.active_view()
        if not view:
            sublime.error_message('Syntax performance tests can only be run when a buffer is open')
            return

        if not title and not docs and not code:
            return

        if not hasattr(self, 'output_view'):
            # Try not to call get_output_panel until the regexes are assigned
            self.output_view = self.window.create_output_panel('pharko')

        settings = self.output_view.settings()
        settings.set('line_numbers', False)
        settings.set('gutter', False)
        settings.set('scroll_past_end', False)

        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel('pharko')

        # Shows the output panel
        self.window.run_command('show_panel', {'panel': 'output.pharko'})

        # this works
        self.output_view.run_command('append', {'characters': '   Syntax Help ...' + '\n', 'force': True, 'scroll_to_end': True})

        stylesheet = '''
            <style>
                body.container {
                    padding:0 20px 20px;
                }
                div.header {
                    position:relative;
                }
                .title {
                    margin:0;
                }
                div.header a.close-button {
                    text-decoration: inherit;
                    font-weight: bold;
                    display: block;
                    padding:10px;
                }
                html.dark div.header a.close-button {
                    background-color: #00000018;
                }
                html.light div.header a.close-button {
                    background-color: #ffffff18;
                }
                code {
                    padding:5px 20px 20px 20px;
                    display:block;
                    width:100%;
                    background-color: #00000018;
                    color:#89DDFF;
                }
            </style>
        '''

        self.output_view.add_phantom("phantom.pharko", self.output_view.sel()[0],
            ('<body class="container">' + stylesheet +
            '<div class="header">' +
            '<h2 class="title">' +
            '<a class="close-button" href="#">' + chr(0x00D7) + '&nbsp;' +
            html.escape(title, quote=False) + '</a>' +
            '</h2></div>' +
            '<div class="content">' +
            '<p>' + docs + '</p>' +
            '<code>' + code + '</code>' +
            '</div></body>'),
            sublime.LAYOUT_BLOCK,
            on_navigate=self.on_navigate)

    def on_navigate(self, href):
        self.output_view.erase_phantoms("phantom.pharko")
        self.window.run_command('hide_panel', {'panel': 'output.pharko'})
