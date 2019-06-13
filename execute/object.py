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

    def get_with_action(self, name):
        if self.current_section is None:
            raise InitError("请选择当前的section")
        method = name + ".method"
        value = name + ".value"
        action = name + ".action"
        inputs = name + ".input_value"
        action_method = self.current_section[action]
        if action_method == "send_keys":
            return Result(self.current_section[method], self.current_section[value], self.current_section[action],
                          self.current_section[inputs])
        return Result(self.current_section[method], self.current_section[value], self.current_section[action])


class Result:

    def __init__(self, method, value, action, inputs=""):
        self.__method = method
        self.__value = value
        self.__action = action
        self.__inputs = inputs

    @property
    def method(self):
        return self.__method

    @property
    def value(self):
        return self.__value

    @property
    def action(self):
        return self.__action

    @property
    def inputs(self):
        return self.__inputs

    def __str__(self):
        return "method: [{0}],value: [{1}],action: [{2}],input: [{3}]".format(self.method, self.value, self.action,
                                                                              self.inputs)


class InitError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

