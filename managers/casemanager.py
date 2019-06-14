import threading

from case.reader.base import BaseReader
from case.reader.excel import ExcelReader
from exception.exception import NoPorterError, EmptyPackagesError
from util.packager.base import BasePackager
from util.packager.packager import ProcessPackager
from util.porter.BasePorter import BasePorter
from util.porter.porter import Porter


class CaseManager:
    """
    CaseManager主要负责porter和packager的调度(目前单线程)
    """

    def __init__(self):
        self.__porter = []
        self.__packager = set()
        self.__reader = set()
        self.lock = threading.RLock()
        self.concurrency = False

    def register_porter(self, porter):
        if self.concurrency:
            self.__concurrency_register(porter)
            return
        if isinstance(porter, BasePorter):
            self.__porter.append(porter)
        else:
            self.exception(porter, "porter")

    def __concurrency_register(self, porter):
        """
        多线程注册
        :param porter:
        :return:
        """
        if isinstance(porter, BasePorter):
            self.lock.acquire(timeout=30)
            self.__porter.append(porter)
            self.lock.release()
        else:
            self.exception(porter, "porter")

    def exception(self, exc, msg):
        raise ValueError("{0} is not {1}".format(exc.__class__, msg))

    def register_reader(self, reader):
        """
        注册Reader
        :param reader: 指定的Reader
        :return:
        """
        if isinstance(reader, BaseReader):
            self.__reader.add(reader)
        else:
            self.exception(reader, "reader")

    def register_packager(self, packager):
        """
        注册Packager
        :param packager: packager
        :return:
        """
        if isinstance(packager, BasePackager):
            self.__packager.add(packager)
        else:
            self.exception(packager, "packager")

    def start(self):
        while True:
            try:
                if self.__porter is None:
                    raise NoPorterError("porter is none")
                # 从reader集合中获取一个reader
                reader = self.__reader.pop()
                # 从packager集合中获取一个packager
                packager = self.__packager.pop()
                # packager指定reader
                packager.select_reader(reader)
                # packager 打包
                packager.packing()
                # 生成一个porter
                porter = Porter()
                # 接受打包的数据
                porter.recv(packager.send())
                # 注册porter
                self.register_porter(porter)
            except KeyError as e:
                print(e)
                break

    def get_porter(self):
        if len(self.__porter) == 0:
            raise EmptyPackagesError("porter queue is empty")

        if self.__porter:
            # 从队列获取porter
            porter = self.__porter.pop(0)
            if len(porter.all_packages) == 0:
                raise EmptyPackagesError("porter`s packages is empty")
            return porter
        raise NoPorterError("porter is none")


if __name__ == '__main__':
    r = ExcelReader("/home/amdins/桌面/teach/seleniums/selenium/case.xlsx")
    man = CaseManager()
    man.register_reader(r)
    man.register_packager(ProcessPackager())
    man.register_porter(Porter())
    man.start()
    p = man.get_porter()
    print(len(p))
