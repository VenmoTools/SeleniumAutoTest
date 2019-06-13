import os
import platform

from case.cases.base import BaseCase
from execute import WebDriver
from execute.object import PageObject
from managers import config
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
            self.object.select_section(process.name)
            self.driver = WebDriver.Driver(os=self.get_os())
            self.driver.start(config.selenium["browser"], config.selenium["driver_path"])
            self.execute(process)
        else:
            raise ValueError("{0} must be Package".format(package.__class__))

    def get_os(self):
        os = config.selenium["os"]
        if os == "":
            os = platform.system()
        return os

    def gen_object_file(self, package):
        filename = package.name + ".ini"
        self.current_object = os.path.join(os.path.join(self.url, "temp"), filename)
        with GenPo(filename) as f:
            f.execute(package)

    def execute(self, process):
        raise NotImplementedError()

    def kind(self, case):
        if case.element_type == "输入框":
            return case.element_name + "_input"
        if case.element_type == "按钮":
            return case.element_name + "_button"
        if case.element_type == "下拉列表":
            return case.element_name + "_select"

    def execute_element(self, name):
        self.driver.execute_element(self.object.get_with_action(name))

    # todo：插件调用多了一次？？？
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
        arr = p.split(":")
        if len(arr) == 2:
            if arr[1] == "B":
                # 如果以B结尾
                plugin = self.plugin_exist(arr[0])
                if plugin is not None:
                    self.before.append(plugin)
            elif arr[1] == "A":
                plugin = self.plugin_exist(arr[0])
                if plugin is not None:
                    self.after.append(plugin)
        else:
            raise ValueError("'{0}':  命名格式错误 插件名:标识".format(p))

    def use_before_plugin(self, case):
        if case.plugins == "" or case.plugins == "null":
            return
        self.get_use_plugin(case)
        for b in self.before:
            b.start(self.driver, case)
        self.before = []

    def use_after_plugin(self, case):
        if case.plugins == "" or case.plugins == "null":
            return
        self.get_use_plugin(case)
        for b in self.after:
            b.start(self.driver, case)
        self.before = []
