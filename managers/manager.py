from managers.casemanager import CaseManager
from managers.center import ExecuteCenter
from plugin.assertplugin import AssertPlugin
from util.packager.packager import ProcessPackager


class Manager:
    """
    总管理器，负责搬运工(porter)调度
    """

    def __init__(self):
        self.case_manager = CaseManager()
        self.reader = None
        self.packager = ProcessPackager()
        self.center = ExecuteCenter()

    def select_reader(self, reader):
        self.reader = reader

    def select_center(self, case):
        if isinstance(case, ExecuteCenter):
            self.center = case
        else:
            raise ValueError("{0} is not ExecuteCenter", case.__class__)

    def select_manager(self, case):
        if isinstance(case, CaseManager):
            self.case_manager = case
        else:
            raise ValueError("{0} is not CaseManager", case.__class__)

    def register_plugin(self, plugin):
        self.center.add_plugin(plugin)

    def register_executor(self, executor):
        self.center.register_execute(executor)

    def porking(self):
        """
        搬运工将包裹送给任务中心
        :return:
        """
        # 注册
        self.case_manager.register_reader(self.reader)
        self.case_manager.register_packager(self.packager)
        # 启动
        self.case_manager.start()
        # 将获得包裹的搬运工交给执行中心
        self.center.recv_porter(self.case_manager.get_porter())
        # 搬运工卸货
        self.center.distribute()
        self.register_plugin(AssertPlugin("assertion"))

    def get_execute(self):
        self.porking()
        return self.center
