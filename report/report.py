import unittest

from managers import config
from report.HTMLTestReportCN import HTMLTestRunner


class Report:

    def __init__(self, pattern="*_test.py"):
        self.cover = unittest.defaultTestLoader.discover(config.report["file_url"], pattern=pattern)
        self.__title = "测试标题"
        self.__description = "测试描述"
        self.__tester = "测试人员"

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, titles):
        self.__title = titles

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def tester(self):
        return self.__tester

    @tester.setter
    def tester(self, tester):
        self.__tester = tester

    def start(self):
        # close
        with open("result.html", 'wb') as f:
            HTMLTestRunner(title=self.__title, description=self.__description,
                           tester=self.__tester,
                           stream=f).run(self.cover)


if __name__ == '__main__':
    a = Report("/home/amdins/桌面/teach/seleniums/selenium/tests")
    a.start()
