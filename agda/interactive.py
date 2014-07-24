from subprocess import PIPE, Popen

class Agda:
    def __init__(self, path):
        self.fd = Popen([path, '--interactive'], stdin=PIPE, stdout=PIPE)

    def load(self, file):
        s = b'IOTCM "' + file + '" None Direct (Cmd_load "' + file + '" [])'
        self.fd.write(s)
        return self.fd.readline()