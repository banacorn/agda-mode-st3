import sublime
from subprocess import PIPE, Popen
import threading

class Agda:
    def __init__(self, path, edit):
        self.__fd = Popen([path, '--interaction'], stdin=PIPE, stdout=PIPE)
        self.writer = Writer(edit)
        print('Agda inited')

    def __write(self, string):
        self.__fd.stdin.write(bytearray(string + '\n', 'utf-8'))

    def __read(self):
        return self.__fd.stdout.readline()

    def load(self, file):
        self.writer.start()
        # s = 'IOTCM "' + file + '" None Direct (Cmd_load "' + file + '" [])'
        # self.__write(s)



class Writer(threading.Thread):
    def __init__(self, edit):
        threading.Thread.__init__(self)

        print('== writer init!!! ==')
        self.window = sublime.active_window()
        self.panel = self.window.create_output_panel('output_panel')
        self.edit = edit

    def run(self):
        print('== writer insert!!! ==')
        self.panel.insert(self.edit, 0, 'aaasdfasdfasfasdfasfasfaaa\n')
        self.window.run_command('show_panel', {'panel': 'output.output_panel'})