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
        self.input = []                 
        self.command = []  

        self.startPiping()


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

    def startPiping(self):
        def worker():
            logger.debug('%d start piping: Agda ~~~> Interactive' % self.id)
            while True:
                data = self.agda.stdout.readline().decode('utf-8')
                self.input.append(data)
            # logger.debug('%d stopped piping: Agda ~\~> Interactive' % self.id)
        t = Thread(target=worker)
        t.start()

    def load(self):
        s = 'IOTCM "' + self.filename + '" None Direct (Cmd_load "' + self.filename + '" [])'
        self.command.append('load')
        self.write(s)

    def parse(self):

        # load
        if self.command and self.command[0] is 'load' and len(self.stack) >= 8:
            # remove comand 'load' & stacked data from Agda
            self.command.pop()
            self.stack, data = self.stack[8:], self.stack[0:8]
            

    # properly terminate the child process (Agda)
    def terminate(self):
        self.agda.terminate()