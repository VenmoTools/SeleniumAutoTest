class BasePorter:

    def __init__(self):
        self.all_packages = set()

    def move(self):
        raise NotImplementedError()

    def move_all(self):
        raise NotImplementedError()

    def recv(self, data):
        raise NotImplementedError()

    def __len__(self):
        return len(self.all_packages)
