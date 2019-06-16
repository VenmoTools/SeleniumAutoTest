import pickle

from util.package.packages import Packages
from util.porter.BasePorter import BasePorter


class Porter(BasePorter):

    def move_all(self):
        return self.all_packages

    def move(self):
        return self.all_packages.pop()

    def recv(self, data):
        if isinstance(data, Packages):
            self.all_packages.add(data)
            return
        elif isinstance(data, bytes):
            packages = pickle.loads(data)
            if isinstance(packages, Packages):
                self.all_packages.add(packages)
                return
        raise TypeError("{0} is not packages", data.__class__)


