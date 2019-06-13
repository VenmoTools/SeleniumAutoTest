from plugin.base import BasePlugin


class AssertPlugin(BasePlugin):

    def __init__(self, name):
        super().__init__(name)
        self.index = 1

    def start(self, driver, case):
        print(self.index)
        self.index += 1
