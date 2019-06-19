import configparser


class PageObject:

    def __init__(self, filename, encoding="utf-8"):
        self.config = configparser.ConfigParser()
        self.config.read(filename, encoding=encoding)
        self.current_section = None

    def select_section(self, section):
        self.current_section = self.config[section]

    def get(self, name):
        if self.current_section is None:
            raise InitError("请选择当前的section")
        method = name + ".method"
        value = name + ".value"
        return self.current_section[method], self.current_section[value]

    # todo:元素拖动
    def get_with_action(self, name):
        """
        根据当前的name获取元素操作属性
        :param name:
        :return:
        """
        if self.current_section is None:
            raise InitError("请选择当前的section")

        # input_button.method = id
        # input_button.value = kw
        # input_button.action = click
        # input_button.inputs = ""

        method = name + ".method"
        value = name + ".value"
        action = name + ".action"
        inputs = name + ".input_value"
        action_method = self.current_section[action]

        r = Element()
        # 获取元素定位方式
        r.method = self.current_section[method]
        # 获取元素定位值
        r.value = self.current_section[value]
        # 获取元素执行动作
        r.action = self.current_section[action]

        if action_method != "click":
            r.inputs = self.current_section[inputs]

        return r


class Element:

    # , method, value, action, inputs="", select=""
    def __init__(self):
        self.__method = ""
        self.__value = ""
        self.__action = ""
        self.__inputs = ""

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action

    @property
    def inputs(self):
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs):
        self.__inputs = inputs

    def __str__(self):
        return "method: [{0}],value: [{1}],action: [{2}],input: [{3}]".format(self.method, self.value, self.action,
                                                                              self.inputs)


class InitError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
