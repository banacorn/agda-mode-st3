import sublime
import threading
from Agda.log import logger

class Panel(object):    
    """Outputs strings to the panel"""
    def __init__(self, id, edit, agda):
        self.id = id
        self.window = sublime.active_window()
        self.view = self.window.create_output_panel('panel-' + str(id))
        self.edit = edit
        self.hidden = True 
        self.streaming = False

        self.stream(agda.read)

        self.show()



      
    def appendLine(self, string):
        last = self.view.size()
        self.view.insert(self.edit, last, string + '\n')

    def clear(self):
        region = self.view.visible_region()
        self.view.erase(self.edit, region)






    # streaming data from target function to the panel
    def stream(self, target):
        def worker():
            while self.streaming:
                output = target()
                # self.write(output)
        self.streaming = True
        threading.Thread(target=worker).start()

    # shows output panel
    def show(self):
        logger.debug('%d show' % self.id)
        self.hidden = False
        self.window.run_command('show_panel', {'panel': 'output.panel-' + str(self.id)})

    # hides output panel
    def hide(self):
        logger.debug('%d hide' % self.id)
        self.hidden = True
        self.window.run_command('hide_panel', {'panel': 'output.panel-' + str(self.id)})

    # hides output panel & kills the stream (if any)
    def kill(self):
        self.hide()
        self.streaming = False

        logger.debug('%d killing the stream (if any)' % self.id)

