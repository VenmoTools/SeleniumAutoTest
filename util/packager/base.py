import config
from util.package.packages import Packages


class BasePackager:

    def __init__(self):
        self.reader = None
        self.packages = Packages()
        self.use_dumps = False
        self.serialize = config.case["serialize_packages"]

    def packing(self):
        raise NotImplementedError()

    def send(self):
        raise NotImplementedError()

    def select_reader(self, reader):
        raise NotImplementedError()

    def dumps(self):
        raise NotImplementedError()
