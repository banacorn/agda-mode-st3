import sublime, sublime_plugin
import os, sys
from Agda.log import logger
import Agda.agda.manager as manager

MANAGER = manager.Manager()

class EventCommand(sublime_plugin.EventListener):

    def on_new(self, view):
        MANAGER.new_view(view)

    def on_open(self, view):
        MANAGER.open_view(view)

    def on_close(self, view):
        MANAGER.close_view(view)

    def on_close(self, view):
        MANAGER.close_view(view)

    def on_activated_async(self, view):
        MANAGER.activate_view(view)

    def on_deactivated_async(self, view):
        MANAGER.deactivate_view(view)

class LoadCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if filename and filename.endswith('.agda'):
            MANAGER.load_agda(self.view, edit)

class QuitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if filename and filename.endswith('.agda'):
            MANAGER.quit_agda(self.view, edit)

class KillAndRestartCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.file_name()
        if filename and filename.endswith('.agda'):
            MANAGER.restart_agda(self.view, edit)


### commands for output panel
class AppendPanelCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kargs):
        last = self.view.size()
        self.view.insert(edit, last, kargs['string'])

class ClearPanelCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        region = self.view.visible_region()
        self.view.erase(edit, region)
