import os
import pickle

import config
from case.reader.base import BaseReader
from case.reader.excel import ExcelReader
from exception.exception import EmptyPackagesError, NoSuchReaderError
from util.package.package import ProcessPackage
from util.packager.base import BasePackager


class ProcessPackager(BasePackager):
    """
    ProcessPackager根据读取的数据打包测试流程
    """

    def dumps(self):
        return pickle.dumps(self.packages)

    def send(self):
        if self.use_dumps:
            return self.dumps()
        elif len(self.packages.all_packages()) == 0:
            raise EmptyPackagesError("the package is empty")
        return self.packages

    def __init__(self):
        super().__init__()

    def select_reader(self, reader):
        if isinstance(reader, BaseReader):
            self.reader = reader
        else:
            raise NoSuchReaderError(reader.__class__)

    def __add_case(self, process, case):
        res = process.add_case(case)
        if res == -1:
            print("添加{0}失败".format(case))

    def packing(self):
        if self.reader is not None:
            processes = self.reader.read()
            # 循环读取的流程
            for process in processes:
                # 根据流程进行打包
                package = ProcessPackage(process.name)
                # 打包流程
                package.pack(process)
                self.packages.add_package(package)
            if self.serialize:
                self.save_to_file()
        else:
            raise ValueError("Reader is None!")

    def save_to_file(self):
        self.packages.gen_id()
        p = os.path.join(config.case["serialize_path"], "serialized")
        if not os.path.exists(p):
            os.mkdir("serialized")
        path = os.path.join(p, "{}.pkl".format(self.packages.id))
        with open(path, "wb") as f:
            pickle.dump(self.packages, f)


if __name__ == '__main__':
    r = ExcelReader()
    p = ProcessPackager()
    p.select_reader(r)
    p.packing()
    p.use_dumps = True
    # print(isinstance(p.send(),bytes))
    data = pickle.loads(p.send())
    print(data)
