from execute.execute import Executor
import config


class NormalExecutor(Executor):

    def execute(self, process):

        self.driver.get(config.case["base_url"])
        for c in process:
            # 执行之前的插件
            self.use_before_plugin(c)
            try:
                self.execute_element(self.kind(c))
            except Exception as e:
                raise RuntimeError("Step: {0} ErrorMsg:'{1}',case:'{2}'".format(c.id, e, current_case))
            # 执行之后的插件
            self.use_after_plugin(c)

