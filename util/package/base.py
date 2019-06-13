from abc import ABCMeta


class BasePackage(metaclass=ABCMeta):

    def __init__(self, name):
        self.__name = name
        self.__id = ""
        self.names = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, nid):
        self.__id = nid

    def gen_id(self):
        raise NotImplementedError()

    @property
    def name(self):
        return self.__name

    def pack(self, data):
        raise NotImplementedError()

    def unpack(self):
        raise NotImplementedError()
