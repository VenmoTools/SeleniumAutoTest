from execute.execute import Executor


class NormalExecutor(Executor):

    def execute(self, process):
        self.driver.get("http://192.168.1.35:8080/DBShop/")
        for c in process:
            # 执行之前的插件
            self.use_before_plugin(c)
            self.execute_element(self.kind(c))
            # 执行之后的插件
            self.use_after_plugin(c)
