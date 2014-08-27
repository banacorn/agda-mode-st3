import sublime
from subprocess import PIPE, Popen, os
from threading import Thread
from queue import Queue
from Agda.log import logger

class Agda(object):

    # executable
    agda_path = None

    """Talks to Agda"""
    def __init__(self, id, filename):
        # super(Agda, self).__init__()
        self.id = id
        self.filename = filename
        self.locate()
        self.agda = Popen([self.agda_path, '--interaction'], stdin=PIPE, stdout=PIPE)

        self.output = Queue()
        self.input = Queue()           

        self.start_piping()
        self.start_parser()

    # locate the path of Agda excutable
    def locate(self):

        if self.agda_path:
            return self.agda_path
        else:
            settings = sublime.load_settings("Agda.sublime-settings")
            agda_path = settings.get('agda_path')

            if not agda_path or not os.path.isfile(agda_path): # empty or not found
                sublime.status_message('Agda executable not found : ' + agda_path)

                # query the user
                def on_done(new_path):
                    settings.set('agda_path', new_path)
                    sublime.status_message('path set as: ' + new_path)
                    self.locate_agda()

                self.window = sublime.active_window()
                self.window.show_input_panel('path of Agda executable', '', on_done, None, None)

            else:
                sublime.save_settings("Agda.sublime-settings")
                self.agda_path = agda_path

    def write(self, string):
        self.agda.stdin.write(bytearray(string + '\n', 'utf-8'))

    def start_piping(self):
        def worker():
            logger.debug('%d start piping: Agda ~~~> Interactive' % self.id)
            while True:
                data = self.agda.stdout.readline().decode('utf-8')
                self.input.put(data)
            # logger.debug('%d stopped piping: Agda ~\~> Interactive' % self.id)
        t = Thread(target=worker)
        t.start()

    def load(self):
        s = 'IOTCM "' + self.filename + '" None Direct (Cmd_load "' + self.filename + '" [])'
        self.write(s)

    def start_parser(self):
        def worker():
            logger.debug('%d start parsing' % self.id)
            while True:
                data = self.input.get()
                print(data)
                self.output.put(data)
        t = Thread(target=worker)
        t.start()
                    

    # properly terminate the child process (Agda)
    def terminate(self):
        self.agda.terminate()