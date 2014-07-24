import sublime, sublime_plugin
import os

class EventCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            activateMenu()
            deactivateSyntax(view)


    def on_close(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            deactivateMenu()


class LoadCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            activateSyntax(self.view)

class QuitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            deactivateSyntax(self.view)

class KillAndRestartCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            sublime.run_command('quit');
            sublime.run_command('load');

def path(suffix):
    return sublime.packages_path() + '/Agda/' + suffix

def activateMenu():
    oldPath = path('Menus/NoMain.sublime-menu')
    newPath = path('Menus/Main.sublime-menu')
    os.rename(oldPath, newPath)

def deactivateMenu():
    oldPath = path('Menus/Main.sublime-menu')
    newPath = path('Menus/NoMain.sublime-menu')
    os.rename(oldPath, newPath)

def activateSyntax(view):
    syntaxPath = 'Packages/Agda/Syntax/Agda.tmLanguage'
    view.set_syntax_file(syntaxPath)

def deactivateSyntax(view):
    syntaxPath = 'Packages/Agda/Syntax/NoAgda.tmLanguage'
    view.set_syntax_file(syntaxPath)

