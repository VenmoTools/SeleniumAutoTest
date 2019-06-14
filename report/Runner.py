import re

from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from genator.report import GenTest
from plugin.assertplugin import AssertPlugin


class Run:

    def __init__(self):
        self.template_package = "from {0} import {1}"
        self.template_add_reader = "man.select_reader({0}())"
        self.template_add_executor = "man.register_executor({0}())"
        self.template_add_plugin = "man.register_plugin({0}('{1}'))"
        self.execute = "execute = man.get_execute()"
        self.content = "execute.run_by_name('{0}')"
        self.template_main = "man = Manager()"
        self.collection = {
            "Reader": [],
            "Executor": [],
            "Plugin": [],
        }

    def add_reader(self, reader):
        self.collection["Reader"].append(self.__get_meta(reader))

    def add_executor(self, executor):
        self.collection["Executor"].append(self.__get_meta(executor))

    def add_plugin(self, plugin):
        res = self.__get_meta(plugin)
        res["name"] = plugin.__dict__["name"]
        self.collection["Plugin"].append(res)

    def __get_class(self, instance):
        res = re.findall("<class .+\.(.+?)'>$", "{}".format(instance.__class__))
        return res[0]

    def __get_meta(self, instance):
        return {"module": instance.__module__, "class": self.__get_class(instance)}

    def __to_packages(self, data):
        if isinstance(data, dict):
            return self.template_package.format(data["module"], data["class"])

    def __gen_reader(self, gen):
        for read in self.collection["Reader"]:
            gen.add_mod_var(self.template_add_reader.format(read["class"]))

    def __gen_executor(self, gen):
        for read in self.collection["Executor"]:
            gen.add_mod_var(self.template_add_executor.format(read["class"]))

    def __gen_plugin(self, gen):
        for read in self.collection["Plugin"]:
            gen.add_mod_var(self.template_add_plugin.format(read["class"], read["name"]))

    def generator_file(self, name):
        gen = GenTest(name)
        gen.add_package("from managers.manager import Manager")
        for k in self.collection:
            arr = self.collection[k]
            if isinstance(arr, list):
                for data in arr:
                    gen.add_package(self.__to_packages(data))
            elif isinstance(arr, dict):
                gen.add_package(self.__to_packages(arr))
        gen.add_mod_var(self.template_main)
        self.__gen_reader(gen)
        self.__gen_executor(gen)
        self.__gen_plugin(gen)
        gen.add_mod_var(self.execute)
        names = "Test"
        gen.add_test_case(content=self.content.format(names), name=names)
        gen.save_file(names + "_test.py")


if __name__ == '__main__':
    e = NormalExecutor()
    p = AssertPlugin("assertion")
    d = ExcelReader()
    r = Run()
    r.add_executor(e)
    r.add_plugin(p)
    r.add_reader(d)
    r.generator_file("Case")
