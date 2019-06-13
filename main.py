from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from managers.manager import Manager

"""

"""

if __name__ == '__main__':
    r = ExcelReader("/home/amdins/桌面/SeleniumAutoTest/case.xlsx")
    man = Manager()
    man.select_reader(r)
    man.register_executor(NormalExecutor())
    man.get_execute().run_by_name("case")
