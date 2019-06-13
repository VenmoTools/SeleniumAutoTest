"""
所有case类的接口
"""
from abc import ABCMeta


class BaseCase(metaclass=ABCMeta):
    """
    一个case就是一个执行步骤
    """

    def __init__(self):
        # 编号	描述	生成的元素名称	元素类别	定位方式	定位值	动作	输入值	等待方式	等待时间 执行动作
        self.id = "1"
        self.desc = ""
        self.element_name = ""
        self.element_type = ""
        self.method = ""
        self.value = ""
        self.action = ""
        self.input = ""
        self.wait_method = ""
        self.wait_time = 0
        self.execute_action = ""
        self.plugins = ""
        self.assertion = ""

    def inject(self, data):
        raise NotImplementedError()
