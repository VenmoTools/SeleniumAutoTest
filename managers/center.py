from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from genator.report import GenTest
from managers.casemanager import CaseManager
from managers.executemanager import ExecuteManager
from plugin.assertplugin import AssertPlugin
from util.packager.packager import ProcessPackager
from util.porter.BasePorter import BasePorter
from util.porter.porter import Porter


class ExecuteCenter:
    """
    任务中心，用于分配任务
    """

    def __init__(self):
        """
        current_port: 当前传入的搬运工
        manager： 管理执行器
        names： 以注册的文件或流程
        """
        self.current_port = None
        self.manager = ExecuteManager()
        self.names = []

    def recv_porter(self, porter):
        """
        获得搬运工
        :param porter:
        :return:
        """
        if isinstance(porter, BasePorter):
            self.current_port = porter

    def add_plugin(self, plugin):
        """
        添加插件
        :param plugin: 插件
        :return:
        """
        self.manager.plugin_center.add_plugin(plugin)

    def register_execute(self, execute):
        """
        添加执行器
        :param execute: execute
        :return:
        """
        self.manager.register_executor(execute)

    def distribute(self):
        """
        卸货：
            port -> Packages
        """
        packages = self.current_port.move()
        # 解包
        self.names.extend(packages.revers.keys())
        self.manager.add_package(packages)

    def run_by_name(self, name):
        """
        运行传入的文件名
        :param name:
        :return:
        """
        self.manager.execute_one_by_name(name)

    def run_one(self):
        """
        执行一个文件
        :return:
        """
        self.manager.execute_one_process()


if __name__ == '__main__':
    r = ExcelReader()
    man = CaseManager()
    man.register_reader(r)
    man.register_packager(ProcessPackager())
    man.register_porter(Porter())
    man.start()

    exec = ExecuteCenter()
    exec.recv_porter(man.get_porter())
    exec.distribute()
    exec.register_execute(NormalExecutor())
    exec.add_plugin(AssertPlugin(""))
    exec.run_one()
