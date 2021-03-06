import sublime, sublime_plugin
import os
from Agda.agda.interactive import Agda
from Agda.agda.panel import Panel
from Agda.log import logger

import inspect
from pprint import pprint
class Manager(object):
    """docstring for Manager"""
    loaded_views = {}

    def __init__(self):
        super(Manager, self).__init__()

    def new_view(self, view):
        logger.debug('%d new' % view.id())

    def load_view(self, view):
        logger.debug('%d load' % view.id())

    def close_view(self, view):
        logger.debug('%d close' % view.id())

    def deactivate_view(self, view):
        id = view.id()
        logger.debug('%d deactivate' % id)
        isLoaded = id in self.loaded_views

        # hide agda output panel
        if isLoaded: 
            self.loaded_views[id]['panel'].hide()

    def activate_view(self, view):

        id = view.id()
        filename = view.file_name()

        logger.debug('%d activate' % id)

        isAgda = filename and filename.endswith('.agda')
        isLoaded = id in self.loaded_views

        if isAgda:
            show_menu()
            if isLoaded:
                activate_syntax(view)
                self.loaded_views[id]['panel'].show()
            else:
                deactivate_syntax(view)
        else:
            hide_menu()


    def load_agda(self, view, edit):


        id = view.id()
        filename = view.file_name()
        if id in self.loaded_views:
            self.restart_agda(view, edit)
        else:
            logger.debug('%d load agda' % id)

            # initializing this newly loaded view
            agda = Agda(id, filename)
            panel = Panel(id, edit)
            panel.pipe(agda.output)

            activate_syntax(view)
            self.loaded_views[id] = {
                'view': view,
                'agda': agda, 
                'panel': panel
            }

            # EAT IT, AGDA
            agda.load()

    def quit_agda(self, view, edit):
        id = view.id()
        isLoaded = id in self.loaded_views

        if not isLoaded:
            logger.debug('%d agda never loaded' % id)

            return
        else:
            logger.debug('%d quit agda' % view.id())

            deactivate_syntax(view)
            self.loaded_views[id]['panel'].kill()
            self.loaded_views.pop(id, None)


    def restart_agda(self, view, edit):
        logger.debug('%d restart agda' % view.id())

        self.quit_agda(view, edit)
        self.load_agda(view, edit)

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
