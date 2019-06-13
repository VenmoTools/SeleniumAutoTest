from execute.execute import Executor


class NormalExecutor(Executor):

    def execute(self, process):
        self.driver.get("http://192.168.1.35:8080/DBShop/")
        for c in process:
            plugins = self.get_use_plugin(c)
            for pl in plugins:
                plugin = self.plugins[pl]
                plugin.start(self.driver.web_driver, c)
            self.execute_element(self.kind(c))
