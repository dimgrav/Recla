from optparse import OptionParser

__author__ = "Dimitris Gravanis"
__copyright__ = "2019"
__version__ = "0.0.1"
__description__ = "Recla option parsing classes"


class OptionError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg


class OptionExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status


class ReclaOptionParser(OptionParser):
    def error(self, msg):
        raise OptionError(msg)

    def exit(self, status=0, msg=None):
        raise OptionExit(status, msg)
