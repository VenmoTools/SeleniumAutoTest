import os
import pickle

import xlrd
from case.cases.base import BaseCase
from case.reader.base import BaseReader
import config
from util.processor.CaseProcess import CaseProcessor


class ExcelReader(BaseReader):
    """
    Version 1.1.1 :从excel文件读取数据，可以自定义，生成的数据必须是dict
    Version 1.1.2 : ExcelReader从excel读取文件,生成的数据为Process对象
    """

    def __init__(self):
        self.path = config.case["url"]
        self.work = xlrd.open_workbook(self.path)
        self.data = {}
        self.gen_file()

    def set_name(self, name):
        self.data["name"] = name

    def gen_file(self):
        file = config.case["case_info"]
        p = os.path.join(file, "temp.file")
        with open(p, mode="w", encoding="utf8") as f:
            f.writelines("|".join(self.work.sheet_names()))

    def get_file_name(self):
        if isinstance(self.path, str):
            arr = self.path.split("/")
            name = arr[len(arr) - 1]
            name = name[:name.index(".")]
            return name

    def read(self):
        # 运用存放流程
        processes = []
        self.set_name(self.get_file_name())
        for name in self.work.sheet_names():
            # 获取一个sheet
            sheet = self.work.sheet_by_name(name)
            # 添加一个流程
            processes.append(self.__read(sheet))
        return processes

    def __read(self, sheet):
        # 生成的流程
        process = CaseProcessor(sheet.name)
        for i in range(1, sheet.nrows):
            x = 0
            # 生成一个case
            case = BaseCase()
            attr = case.__dict__
            for k in attr:
                attr[k] = sheet.cell_value(rowx=i, colx=x)
                x += 1
            # 生成case并添加
            process.add_case(case)
        return process.ordered()


if __name__ == '__main__':
    res = ExcelReader().read()
    res = pickle.dumps(res)
    print(isinstance(res,bytes))
    c = pickle.loads(res)
    print(c)
