from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin
from report.Runner import Run
from report.reports import Report

"""

"""

if __name__ == '__main__':
    e = ExcelReader()
    r = Run()
    r.add_executor(NormalExecutor())
    r.add_plugin(AssertPlugin("assertion"))
    r.add_reader(e)
    r.generator_file("case")
    report = Report()
    report.start()
