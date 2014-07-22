import sublime, sublime_plugin

class OnLoadCommand(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:  # buffer has never been saved
            return
        if filename.endswith(".agda"):
            sublime.status_message("Welcome to Agda mode")


