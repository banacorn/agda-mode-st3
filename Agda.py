import sublime, sublime_plugin

class OnLoadCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith(".agda"):
            sublime.status_message("Welcome to Agda mode")
            
            view.set_syntax_file("Packages/Agda/NoAgda.tmLanguage")

class LoadSourceCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        filename = self.view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith(".agda"):
            self.view.set_syntax_file("Packages/Agda/Agda.tmLanguage")
