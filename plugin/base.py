class BasePlugin:

    def __init__(self, name):
        self.name = name

    def start(self, driver,case):
        """
        执行插件功能
        :param driver: webdriver对象
        :param case:  当前执行的case
        :return:
        """
        if driver is not None:
            raise NotImplementedError()
