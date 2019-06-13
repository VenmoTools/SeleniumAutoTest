from execute.execute import Executor
from plugin.plugincenter import PluginCenter
from util.package.packages import Packages


class ExecuteManager:

    def __init__(self):
        self.executors = set()
        self.packages = None
        self.plugin_center = PluginCenter()

    def register_executor(self, execute):
        if isinstance(execute, Executor):
            self.executors.add(execute)
        else:
            raise ValueError("{0} is not executor".format(execute.__class__))

    def add_package(self, package):
        """
        ALL Packages
        :param package:
        :return:
        """
        if isinstance(package, Packages):
            self.packages = package
        else:
            raise ValueError("{0} is not package".format(package.__class__))

    def execute_one_by_name(self, name):
        """
        根据文件名执行该文件的所有流程
        packages -> package
        :param name: 包名
        :return:
        """
        try:
            package = self.packages.get_package_by_name(name)
            exec = self.executors.pop()
            for pk in package:
                with exec as execute:
                    execute.add_plugin(self.plugin_center.plugins)
                    execute.init(pk)
        except ValueError as e:
            print(e)

    def execute_one_process(self):
        try:
            exec = self.executors.pop()
            for pk in self.packages:
                with exec as execute:
                    execute.add_plugin(self.plugin_center.plugins)
                    execute.init(pk)
        except ValueError as e:
            print(e)
