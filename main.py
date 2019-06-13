from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from managers.manager import Manager
from plugin.assertplugin import AssertPlugin

"""

"""

if __name__ == '__main__':
    r = ExcelReader("/home/amdins/桌面/teach/seleniums/selenium/case.xlsx")
    man = Manager()
    man.select_reader(r)
    man.register_executor(NormalExecutor())
    man.register_plugin(AssertPlugin("assertion"))
    man.porking()
    man.get_execute().run_by_name("case")
