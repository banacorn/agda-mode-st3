import sublime, sublime_plugin
import os, sys
import Agda.agda.interactive as interactive
import Agda.agda.manager as manager

AGDA = interactive.Agda()
MANAGER = manager.Maneger()

class EventCommand(sublime_plugin.EventListener):

    def on_close(self, view):
        MANAGER.close_view(view)

    def on_activated_async(self, view):
        MANAGER.activate_view(view)

class LoadCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if filename and filename.endswith('.agda'):
            MANAGER.load_agda(self.view)

            # activate_syntax(self.view)
            # path = self.locate_agda()
            # sublime.status_message('File loaded.')
            # AGDA.initialize(path)
            # AGDA.load(filename)

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
        if filename and filename.endswith('.agda'):
            MANAGER.quit_agda(self.view)

class KillAndRestartCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if filename and filename.endswith('.agda'):
            MANAGER.restart_agda(self.view)
