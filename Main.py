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
            AGDA.locate()            
            MANAGER.load_agda(self.view)

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