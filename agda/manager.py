import sublime, sublime_plugin
import os
from pprint import pprint

from Agda.agda.interactive import Agda
from Agda.agda.panel import Panel

class Maneger(object):
    """docstring for Maneger"""
    def __init__(self):
        super(Maneger, self).__init__()
    
    previously_shown_panel = None
    loaded_views = {}

    def new_view(self, view):
        print('new', view.id())

    def load_view(self, view):
        print('load', view.id())

    def close_view(self, view):
        print('close', view.id())

    def activate_view(self, view):
        id = view.id()
        print('activate', id)
        filename = view.file_name()
        if filename and filename.endswith('.agda'): # agda
            show_menu()
            if id in self.loaded_views:  
                panel = self.loaded_views[id]['panel']
                panel.show()
                self.previously_shown_panel = panel
            else:                                   # deactivate syntax when agda not loaded
                deactivate_syntax(view)

                # hide panel
                if self.previously_shown_panel:
                    self.previously_shown_panel.hide()
                    self.previously_shown_panel = None
        else:                                       # no agda
            hide_menu()

            # hide panel
            if self.previously_shown_panel:
                self.previously_shown_panel.hide()
                self.previously_shown_panel = None

    def load_agda(self, view):
        id = view.id()
        filename = view.file_name()
        if id in self.loaded_views:
            print('agda already loaded', id)
            return
        else:
            print('load agda', id)

            # initializing this newly loaded view
            agda = Agda(filename)
            panel = Panel(id, agda)
            activate_syntax(view)
            self.loaded_views[id] = {
                'view': view,
                'agda': agda, 
                'panel': panel,
            }

            # EAT IT, AGDA
            agda.load()

    def quit_agda(self, view):
        id = view.id()
        if id not in self.loaded_views:
            print('agda never loaded', id)
            return
        else:
            print('quit agda', view.id())
            deactivate_syntax(view)
            self.loaded_views[id]['panel'].kill()
            self.loaded_views[id]['agda'].terminate()
            self.loaded_views.pop(id, None)

    def restart_agda(self, view):
        print('restart agda', view.id())

def path(suffix):
    return sublime.packages_path() + '/Agda/' + suffix

def show_menu():
    old = path('Menus/NoMain.sublime-menu')
    new = path('Menus/Main.sublime-menu')
    if os.path.isfile(old):
        os.rename(old, new)

def hide_menu():
    old = path('Menus/Main.sublime-menu')
    new = path('Menus/NoMain.sublime-menu')    
    if os.path.isfile(old):
        os.rename(old, new)

def activate_syntax(view):
    view.set_syntax_file('Packages/Agda/Syntax/Agda.tmLanguage')

def deactivate_syntax(view):
    view.set_syntax_file('Packages/Agda/Syntax/NoAgda.tmLanguage')