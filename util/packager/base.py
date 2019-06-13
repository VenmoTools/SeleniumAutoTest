from util.package.packages import Packages


class BasePackager:

    def __init__(self):
        self.reader = None
        self.packages = Packages()

    def packing(self):
        raise NotImplementedError()

    def send(self):
        raise NotImplementedError()

    def select_reader(self, reader):
        raise NotImplementedError()
