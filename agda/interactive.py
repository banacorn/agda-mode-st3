from subprocess import PIPE, Popen

class Agda:
    def __init__(self, path):
        self.__fd = Popen([path, '--interaction'], stdin=PIPE, stdout=PIPE)

    def __write(self, string):
        self.__fd.stdin.write(bytearray(string + '\n', 'utf-8'))

    def __read(self):
        return self.__fd.stdout.readline()

    def load(self, file):
        s = 'IOTCM "' + file + '" None Direct (Cmd_load "' + file + '" [])'
        print(s)
        self.__write(s)
        return self.__read()