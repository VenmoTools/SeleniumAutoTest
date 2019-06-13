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
        method = name + ".method"
        value = name + ".value"
        action = name + ".action"
        inputs = name + ".input_value"
        action_method = self.current_section[action]

        r = Element()
        r.method = self.current_section[method]
        r.value = self.current_section[value]
        r.action = self.current_section[action]
        if action_method == "send_keys":
            r.inputs = self.current_section[inputs]
        if action_method == "select":
            select = name + ".select"
            r.select = self.current_section[select]
        if action_method == "iframe":
            iframe = name + ".iframe"
            r.iframe = self.current_section[iframe]
        if action_method == "js":
            js = name + ".javaScript"
            r.js = self.current_section[js]
        return r


class Element:

    # , method, value, action, inputs="", select=""
    def __init__(self):
        self.__method = ""
        self.__value = ""
        self.__action = ""
        self.__inputs = ""
        self.__select = ""
        self.__iframe = ""
        self.__js = ""

    @property
    def js(self):
        return self.__js

    @js.setter
    def js(self, js):
        self.__js = js

    @property
    def iframe(self):
        return self.__iframe

    @iframe.setter
    def iframe(self, iframe):
        self.__iframe = iframe

    @property
    def select(self):
        return self.__select

    @select.setter
    def select(self, select):
        self.__select = select

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
