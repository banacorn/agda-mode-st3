import sublime
from threading import Thread
from Agda.log import logger

class Panel(object):    
    """Outputs strings to the panel"""
    def __init__(self, id, edit):
        self.id = id
        self.window = sublime.active_window()
        self.view = self.window.create_output_panel('panel-' + str(id))
        self.edit = edit
        self.hidden = True 
        self.show()

        #
        self.piping = False


    def append(self, string):
        if string is not None:
            last = self.view.size()
            self.view.run_command('append_panel', {'string': string})

    def clear(self):
        region = self.view.visible_region()
        self.view.run_command('clear_panel')

    # piping data from queue to output panel
    def pipe(self, queue):
        self.piping = True
        self.queue = queue
        def worker():
            logger.debug('%d start piping: Agda ~~~> Panel' % self.id)
            while self.piping:
                data = queue.get()
                self.clear()
                self.append(data)
            logger.debug('%d stopped piping: Agda ~\~> Panel' % self.id)
        t = Thread(target=worker)
        t.start()

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

    def kill(self):
        if self.piping and self.queue:
            self.piping = False
            self.queue.put(None)
            self.hide()
            