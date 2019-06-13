from case.cases.base import BaseCase


class NormalCase(BaseCase):

    def __init__(self):
        super().__init__()

    def inject(self, data):
        if isinstance(data, dict):
            self.id = data["id"]
            self.desc = data["desc"]
            self.element_name = data["element_name"]
            self.element_type = data["element_type"]
            self.method = data["method"]
            self.value = data["value"]
            self.action = data["action"]
            self.input = data["input"]
            self.wait_method = data["wait_method"]
            self.wait_time = data["wait_time"]
            self.execute_action = data["execute_action"]
            self.plugins = data["plugins"]
            self.assertion = data["assertion"]
            return self
        else:
            raise ValueError("{} is not dict".format(data.__class__))

    def __str__(self):
        return "编号：{0},描述：{1},元素名称：{2},元素类型：{3},定位方式：{4},定位值：{5},执行动作：{6},输入值：{7}等待方式：{8},等待时间：{9}". \
            format(self.id, self.desc, self.element_name, self.element_type, self.method, self.value, self.action,
                   self.input, self.wait_method, self.wait_time)


if __name__ == '__main__':
    c = NormalCase()
    print(isinstance(c, BaseCase))
