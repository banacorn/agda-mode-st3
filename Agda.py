import sublime, sublime_plugin, sys, os

import json
from pprint import pprint

# from subprocess import Popen, PIPE, check_output, call

class EventCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):

            print('loaded')

            self.activateMenu()
            self.deactivateSyntax(view)


    def on_close(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            self.deactivateMenu()

            
    def activateMenu(self):
        oldPath = sublime.packages_path() + '/Agda/Menus/NoMain.sublime-menu'
        newPath = sublime.packages_path() + '/Agda/Menus/Main.sublime-menu'
        os.rename(oldPath, newPath)


    def deactivateMenu(self):
        oldPath = sublime.packages_path() + '/Agda/Menus/Main.sublime-menu'
        newPath = sublime.packages_path() + '/Agda/Menus/NoMain.sublime-menu'
        os.rename(oldPath, newPath)

    def deactivateSyntax(self, view):
        view.set_syntax_file('Packages/Agda/NoAgda.tmLanguage')


    # def initialize(self):
    #     configPath = sublime.packages_path() + '/Agda/configuration.json'
    #     config = json.load(open(configPath))
    #     pprint(config)

    #     if config['initialized'] == 'False' :
    #         self.window.show_input_panel("Goto Line:", "", self.on_done, None, None)


class LoadSourceCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            self.view.set_syntax_file('Packages/Agda/Agda.tmLanguage')

