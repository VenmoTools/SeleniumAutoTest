from case.cases.normal import NormalCase
from case.reader.base import BaseReader
from case.reader.excel import ExcelReader
from exception.exception import EmptyPackagesError, NoSuchReaderError
from util.package.package import ProcessPackage
from util.packager.base import BasePackager
from util.processor.CaseProcess import CaseProcessor


class ProcessPackager(BasePackager):
    """
    ProcessPackager根据读取的数据打包测试流程
    """

    def send(self):
        if len(self.packages.all_packages()) == 0:
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
            data = self.reader.read()
            # 获取读取的json数据
            cases = data["cases"]
            for i in cases:
                for name, steps in i.items():
                    # 生成包裹
                    package = ProcessPackage(data["name"])
                    # 生成page object 文件名根据 package的编号生成
                    # 根据流程名生成测试步骤
                    process = CaseProcessor(name)
                    # 遍历所有执行步骤
                    for step in steps:
                        # 创建单个case
                        ca = NormalCase()
                        ca.inject(step)
                        # 添加case
                        self.__add_case(process, ca)
                    # 将生成的测试步骤按照id排序
                    process.ordered()

                    # 解析该流程的Page Object
                    # r.execute(process)

                    # 重置索引
                    process.reset_index()
                    # 将读取好的数据打包
                    package.pack(process)
                    # 添加包裹
                    self.packages.add_package(package)

        else:
            raise ValueError("Reader is None!")


if __name__ == '__main__':
    r = ExcelReader("/home/amdins/桌面/teach/seleniums/selenium/case.xlsx")
    # r.set_name("case")
    # p = ProcessPackager()
    # p.select_reader(r)
    # p.packing()
