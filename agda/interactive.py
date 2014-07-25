import sublime
from subprocess import PIPE, Popen

class Agda(object):

    # executable
    __agda_path = None                   

    """Talks to Agda"""
    def __init__(self, filename):
        # super(Agda, self).__init__()
        self.__filename = filename
        self.locate()
        self.__agda = Popen([self.__agda_path, '--interaction'], stdin=PIPE, stdout=PIPE)

    # locate the path of Agda excutable
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

    def write(self, string):
        self.__agda.stdin.write(bytearray(string + '\n', 'utf-8'))

    def read(self):
        return self.__agda.stdout.readline().decode('utf-8')

    def load(self):
        s = 'IOTCM "' + self.__filename + '" None Direct (Cmd_load "' + self.__filename + '" [])'
        self.write(s)