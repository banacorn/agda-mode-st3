import sublime
from subprocess import PIPE, Popen
# import threading

class Agda:
    """Talks to Agda"""
    def __init__(self):
        super(Agda, self).__init__()

    def initialize(self, path, edit):
        self.__fd = Popen([path, '--interaction'], stdin=PIPE, stdout=PIPE)
        self.panel = Panel(edit)
    def __write(self, string):
        self.__fd.stdin.write(bytearray(string + '\n', 'utf-8'))

    def __read(self):
        return self.__fd.stdout.readline().decode('utf-8')

    def load(self, file):
        s = 'IOTCM "' + file + '" None Direct (Cmd_load "' + file + '" [])'
        self.__write(s)
        self.panel.write(self.__read());


class Panel(object):
    """Outputs strings to the panel"""
    def __init__(self, edit):
        super(Panel, self).__init__()
        self.window = sublime.active_window()
        self.panel = self.window.create_output_panel('panel')
        self.edit = edit

    def write(self, string):
        print('* PANEL: ' + string)
        self.panel.insert(self.edit, 0, string)
        self.window.run_command('show_panel', {'panel': 'output.panel'})


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