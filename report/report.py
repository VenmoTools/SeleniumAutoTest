import re
import unittest

from emailcenter.smtp import STMPSender, email_template
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
        sender = STMPSender()
        with open("result.html") as f:
            res = "".join(f.readlines()[:130])
            title = re.findall('<h1 style="font-family: Microsoft YaHei">(.+?)</h1>', res)
            print(res)
            man = re.findall("<p .*测试人员.*> ([\w\d]+?)</p>", res)
            time = re.findall("<p .*>开始时间.*> (.+?)</p>", res)
            cost = re.findall("<p .*>合计耗时.*> (.+?)</p>", res)
            result = re.findall("<p .*>测试结果.*> 共 (\d+?)，通过 (\d+?)，通过率= (.+?)%</p>", res)
            total, succeed, passed = result[0]
            res = email_template.format(title[0], "", total, succeed, passed, time[0], cost[0], man[0])
            sender.build_email(res)
            sender.send_with_tls()

        with open("result.html", 'wb') as f:
            HTMLTestRunner(title=self.__title, description=self.__description,
                           tester=self.__tester,
                           stream=f).run(self.cover)


if __name__ == '__main__':
    a = Report("/home/amdins/桌面/teach/seleniums/selenium/tests")
    a.start()
