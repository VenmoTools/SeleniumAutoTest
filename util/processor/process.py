class Processor:

    def __init__(self, name):
        self.name = name
        self.sources = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.sources):
            data = self.sources[self.index]
            self.index += 1
            return data
        else:
            self.index = 0
            raise StopIteration()

    def reset_index(self):
        self.index = 0

    def add_case(self, case):
        raise NotImplementedError()

    def __len__(self):
        return len(self.sources)

    def ordered(self):
        self.sources.sort(key=lambda case: int(case.id), reverse=False)
        return self
