import os
import platform
import re

from selenium.webdriver import Firefox

import config
from case.cases.base import BaseCase
from execute import WebDriver
from execute.object import PageObject
from util.package.base import BasePackage
from util.package.package import GenPo


class Executor:

    def __init__(self):
        self.current_object = None
        self.object = None
        self.url = config.url["page_object_file_path"]
        self.driver = None
        self.plugins = []
        self.before = []
        self.after = []
        self.exception = []

    def reset(self):
        self.plugins = []
        self.before = []
        self.after = []
        self.driver = None
        self.object = None
        self.current_object = None
        return self

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def add_after(self, plugin):
        self.after.append(plugin)

    def add_before(self, plugin):
        self.before.append(plugin)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def init(self, package):
        if isinstance(package, BasePackage):
            self.gen_object_file(package)
            # 解包
            process = package.unpack()
            # 根据case生成Page Object
            self.object = PageObject(self.current_object)
            # 指定当前使用的流程
            self.object.select_section(process.name)
            # 初始化Driver
            self.driver = WebDriver.Driver(os=self.get_os())
            # 启动Driver
            self.driver.start(config.selenium["browser"], config.selenium["driver_path"])
            # 执行命令
            self.execute(process)
        else:
            raise ValueError("{0} must be Package".format(package.__class__))

    def get_os(self):
        os = config.selenium["os"]
        if os == "":
            os = platform.system()
        return os

    def gen_object_file(self, package):
        """
        用于生成PageObject
        :param package: 流程名
        :return:
        """
        filename = package.name + ".ini"
        self.current_object = os.path.join(os.path.join(self.url, "temp"), filename)
        with GenPo(filename) as f:
            f.execute(package)

    def execute(self, process):
        raise NotImplementedError()

    def execute_element(self, name):
        self.driver.execute_element(self.object.get_with_action(name))

    def get_use_plugin(self, case):
        """
        使用插件表达式： assertion:B 表示该插件在测试用例之前执行
        使用插件表达式： assertion:A 表示该插件在测试用例之后执行
        :param case:
        :return:
        """
        if isinstance(case, BaseCase):
            if case == "":
                return
            pl = case.plugins.split(",")
            for i in pl:
                self.kind_of_plugin(i)
        else:
            raise ValueError("{}必须是Case".format(case.__class__))

    def plugin_exist(self, name):
        for pl in self.plugins:
            if name in pl.keys():
                return pl[name]
        return None

    def kind_of_plugin(self, p):
        if p == "":
            return
        res = re.findall("(.+):([ABE])", p)
        if res != 1:
            raise SyntaxError("'{0}':  命名格式错误 插件名:标识".format(p))
        plugin_name, when = res[0]
        # 在已注册的插件中去寻找
        plugin = self.plugin_exist(plugin_name)

        if plugin is None:
            raise ValueError("{} 插件没有注册".format(plugin_name))
        if when.upper() == "B":
            self.before.append(plugin)
        elif when.upper() == "A":
            self.after.append(plugin)
        elif when.upper() == "E":
            self.exception.append(plugin)
        else:
            raise SyntaxError("'{0}':  命名格式错误 插件名:标识".format(p))

    def use_before_plugin(self, case):
        if case.plugins == "" or case.plugins == "null":
            return
        self.get_use_plugin(case)
        for b in self.before:
            b.start(self.driver, case)
        self.before = []

    def use_error_plugin(self, case):
        if case.plugins == "" or case.plugins == "null":
            return
        self.get_use_plugin(case)
        for b in self.exception:
            b.start(self.driver, case)
        self.exception = []

    def use_after_plugin(self, case):
        if case.plugins == "" or case.plugins == "null":
            return
        self.get_use_plugin(case)
        for b in self.after:
            b.start(self.driver, case)
        self.before = []

    def browser_action(self, case, current):
        """
        处理浏览器动作
        :param case: 当前执行的用例
        :param current: 当前的时刻
        :return:
        """
        if case.execute_action == "" or case.execute_action == "null":
            return
        if isinstance(case, BaseCase):
            res = re.findall("(.+?):(\w)", case.execute_action)
            if len(res) != 1:
                raise SyntaxError("Syntax Error {}".format(res))
            cmd, when = res[0]
            if when.lower() == current.lower():
                self.execute_browser_action(cmd)

    def windows_control(self, cmd):
        if cmd == "win_max":
            self.driver.web_driver.maximize_window()
        elif cmd == "win_min":
            self.driver.web_driver.minimize_window()
        elif cmd == "win_full":
            self.driver.web_driver.fullscreen_window()
        else:
            raise SyntaxError("Syntax Error:{} not supported".format(cmd))

    def switch_windows(self, cmd):
        handles = self.driver.web_driver.window_handles
        if cmd == "switch_last":
            self.driver.web_driver.switch_to.window(handles[len(handles) - 1])
        elif cmd == "switch_first":
            self.driver.web_driver.switch_to.window(handles[0])
        else:
            res = re.findall("switch_index\((\d)\)", cmd)
            if len(res) != 1:
                raise SyntaxError("Syntax Error:{}".format(cmd))
            try:
                self.driver.web_driver.switch_to.window(handles[int(res[0])])
            except IndexError:
                raise SyntaxError("Syntax Error:{} index out of max windows number".format(cmd))

    def handle_alter(self, cmd):
        if cmd == "alter_accept":
            self.driver.web_driver.switch_to.alert.accept()
        elif cmd == "alter_dismiss":
            self.driver.web_driver.switch_to.alert.dismiss()
        else:
            res = re.findall("alter_send\((\d)\)", cmd)
            if len(res) != 1:
                raise SyntaxError("Syntax Error:{}".format(cmd))
            self.driver.web_driver.switch_to.alert.send_keys(res[0])

    def page_control(self, cmd):
        if cmd == "page_forward":
            self.driver.web_driver.forward()
        elif cmd == "page_back":
            self.driver.web_driver.back()
        else:
            raise SyntaxError("Syntax Error:{} not supported".format(cmd))

    def execute_browser_action(self, cmd):
        if "win" in cmd:
            self.windows_control(cmd)
        elif "switch" in cmd:
            self.switch_windows(cmd)
        elif "alter" in cmd:
            self.handle_alter(cmd)
        elif "page" in cmd:
            self.page_control(cmd)
        else:
            raise SyntaxError("Syntax Error:{} not supported".format(cmd))


if __name__ == '__main__':
    f = Firefox()
