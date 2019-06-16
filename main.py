from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin
from report.Runner import Run
from report.report import Report

"""

"""

if __name__ == '__main__':
    r = Run()
    r.add_executor(NormalExecutor())
    r.add_plugin(AssertPlugin("assertion"))
    r.add_reader(ExcelReader())
    r.generator_file("case")
    report = Report()
    report.start()
