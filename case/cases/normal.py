from case.cases.base import BaseCase


class NormalCase(BaseCase):

    def __init__(self):
        super().__init__()

    def inject(self, data):
        pass

    # def inject(self, data):
    #     if isinstance(data, dict):
    #         self.id = data["id"]
    #         self.desc = data["desc"]
    #         self.element_name = data["element_name"]
    #         self.element_type = data["element_type"]
    #         self.method = data["method"]
    #         self.value = data["value"]
    #         self.action = data["action"]
    #         self.input = data["input"]
    #         self.wait_method = data["wait_method"]
    #         self.wait_time = data["wait_time"]
    #         self.execute_action = data["execute_action"]
    #         self.plugins = data["plugins"]
    #         self.assertion = data["assertion"]
    #         return self
    #     else:
    #         raise ValueError("{} is not dict".format(data.__class__))


if __name__ == '__main__':
    c = NormalCase()
    print(isinstance(c, BaseCase))
