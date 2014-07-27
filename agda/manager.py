import sublime, sublime_plugin
import os
from Agda.agda.interactive import Agda
from Agda.agda.panel import Panel
from Agda.log import logger

class Manager(object):
    """docstring for Manager"""
    def __init__(self):
        super(Manager, self).__init__()
    
    previously_shown_panel = None
    loaded_views = {}

    def new_view(self, view):
        logger.debug('[View] %d new' % view.id())

    def load_view(self, view):
        logger.debug('[View] %d load' % view.id())

    def close_view(self, view):
        logger.debug('[View] %d close' % view.id())

    def activate_view(self, view):
        id = view.id()
        logger.debug('[View] %d activate' % id)
        filename = view.file_name()
        if filename and filename.endswith('.agda'): # agda
            show_menu()
            if id in self.loaded_views:             # loaded
                panel = self.loaded_views[id]['panel']
                panel.show()
                self.previously_shown_panel = panel

            else:                                   # unloaded
                deactivate_syntax(view)

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
            logger.debug('[View] %d agda already loaded' % id)
            return
        else:
            logger.debug('[View] %d load agda' % id)

            # initializing this newly loaded view
            agda = Agda(id, filename)
            panel = Panel(id, agda)
            activate_syntax(view)
            self.loaded_views[id] = {
                'view': view,
                'agda': agda, 
                'panel': panel,
            }

            self.previously_shown_panel = panel

            # EAT IT, AGDA
            agda.load()

    def quit_agda(self, view):
        id = view.id()
        if id not in self.loaded_views:
            logger.debug('[View] %d agda never loaded' % id)

            return
        else:
            logger.debug('[View] %d quit agda' % view.id())

            deactivate_syntax(view)
            self.loaded_views[id]['panel'].kill()
            self.loaded_views.pop(id, None)
            self.previously_shown_panel = None


    def restart_agda(self, view):
        logger.debug('[View] %d restart agda' % view.id())

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