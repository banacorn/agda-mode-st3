import sublime
import threading

class Panel(object):    
    """Outputs strings to the panel"""
    def __init__(self, id, agda):
        self.id = id
        self.window = sublime.active_window()
        self.panel = self.window.create_output_panel('panel-' + str(id))
        self.hidden = True 
        self.streaming = False

        self.stream(agda.read)


    # write to output panel
    def write(self, string):
        self.panel.run_command('append', {'characters': string})
        self.show()

    # streaming data from target function to the panel
    def stream(self, target):
        def worker():
            while self.streaming:
                output = target()
                self.write(output)
        self.streaming = True
        threading.Thread(target=worker).start()

    # shows output panel
    def show(self):
        print('showing panel', self.id)
        self.hidden = False
        self.window.run_command('show_panel', {'panel': 'output.panel-' + str(self.id)})

    # hides output panel
    def hide(self):
        print('hiding panel', self.id)
        self.hidden = True
        self.window.run_command('hide_panel', {'panel': 'output.panel-' + str(self.id)})

    # hides output panel & kills the stream (if any)
    def kill(self):
        self.hide()
        self.streaming = False
        print('killing the stream (if any)', self.id)

