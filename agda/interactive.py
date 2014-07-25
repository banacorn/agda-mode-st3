import sublime
import os
from subprocess import PIPE, Popen
import threading

class Agda:

    __initialized = False

    # executable
    __agda_path = None                   

    """Talks to Agda"""
    def __init__(self):
        super(Agda, self).__init__()

    # wire on Agda
    def initialize(self, path):
        self.__fd = Popen([path, '--interaction'], stdin=PIPE, stdout=PIPE)
        self.__initialized = True

    def locate(self):

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
            self.__agda_path = agda_path

    def __write(self, string):
        self.__fd.stdin.write(bytearray(string + '\n', 'utf-8'))

    def __read(self):
        return self.__fd.stdout.readline().decode('utf-8')

    def load(self, file):
        if self.__initialized:

            s = 'IOTCM "' + file + '" None Direct (Cmd_load "' + file + '" [])'
            self.__write(s)

            # panel = Panel()
            # panel.stream(self.__read);

class Panel(object):
    """Outputs strings to the panel"""
    def __init__(self):
        self.window = sublime.active_window()
        print(self.window.views())
        self.panel = self.window.create_output_panel('panel')

    def write(self, string):
        self.panel.run_command("append", {"characters": string})
        self.window.run_command('show_panel', {'panel': 'output.panel'})


    __killStream = False

    # streaming data from target function to the panel
    def stream(self, target):
        def worker():
            #
            while not self.__killStream:
                output = target()
                self.write(output)
        t = threading.Thread(target=worker)
        t.start()

# class Writer(threading.Thread):
#     def __init__(self, edit):
#         threading.Thread.__init__(self)

#         print('== writer init!!! ==')
#         self.window = sublime.active_window()
#         self.panel = self.window.create_output_panel('output_panel')
#         self.edit = edit

#     def run(self):
#         print('== writer insert!!! ==')
#         self.panel.insert(self.edit, 0, 'aaaa\n')
#         self.window.run_command('show_panel', {'panel': 'output.output_panel'})