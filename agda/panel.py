import sublime
import threading
class Panel(object):
    """Outputs strings to the panel"""
    def __init__(self, id, agda):
        self.id = id
        self.window = sublime.active_window()
        self.panel = self.window.create_output_panel('panel-' + str(id))

        self.stream(agda.read)

    def write(self, string):
        self.panel.run_command('append', {'characters': string})
        self.window.run_command('show_panel', {'panel': 'output.panel-' + str(self.id)})

    # streaming data from target function to the panel
    def stream(self, target):
        def worker():
            while True:
                output = target()
                self.write(output)
        threading.Thread(target=worker).start()