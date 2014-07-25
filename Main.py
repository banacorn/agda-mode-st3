import sublime, sublime_plugin
import os, sys
import Agda.agda.interactive as ai

AGDA = ai.Agda()

class EventCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            activate_menu()
            deactivate_syntax(view)


    def on_close(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            deactivate_menu()

class LoadCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            activate_syntax(self.view)
            path = self.locate_agda()
            sublime.status_message('File loaded.')
            AGDA.initialize(path)
            AGDA.load(filename)

    # find Agda with settings
    # ask if not found
    def locate_agda(self):
        settings = sublime.load_settings("Agda.sublime-settings")
        agda_path = settings.get('agda_path')


        if not agda_path or not os.path.isfile(agda_path): # empty or not found
            sublime.status_message('Agda executable not found : ' + agda_path)
            self.ask_and_set_agda_path() # query the user
        else:
            sublime.save_settings("Agda.sublime-settings")

        return agda_path

    def ask_and_set_agda_path(self):

        def on_done(new_path):
            settings = sublime.load_settings("Agda.sublime-settings")
            settings.set('agda_path', new_path)
            sublime.status_message('path set as: ' + new_path)
            self.locate_agda()

        self.window = sublime.active_window()
        self.window.show_input_panel('path of Agda executable', '', on_done, None, None)

class QuitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith('.agda'):
            deactivate_syntax(self.view)

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

def activate_menu():
    old = path('Menus/NoMain.sublime-menu')
    new = path('Menus/Main.sublime-menu')
    os.rename(old, new)

def deactivate_menu():
    old = path('Menus/Main.sublime-menu')
    new = path('Menus/NoMain.sublime-menu')
    os.rename(old, new)

def activate_syntax(view):
    view.set_syntax_file('Packages/Agda/Syntax/Agda.tmLanguage')

def deactivate_syntax(view):
    view.set_syntax_file('Packages/Agda/Syntax/NoAgda.tmLanguage')



