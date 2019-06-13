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
        self.plugins = {}

    def add_plugin(self, plugin):
        self.plugins = plugin

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

    def execute_element(self, name):
        self.driver.execute_element(self.object.get_with_action(name))

    def get_use_plugin(self, case):
        if isinstance(case, BaseCase):
            if case == "":
                return []
            return case.plugins.split(",")
        raise ValueError("{}必须是Case".format(case.__class__))
