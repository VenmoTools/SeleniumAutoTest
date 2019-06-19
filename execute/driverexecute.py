import config
from execute.execute import Executor
from util.tools.element import kind


class NormalExecutor(Executor):

    def execute(self, process):

        self.driver.get(config.case["base_url"])
        for c in process:
            # 执行浏览器动作
            self.browser_action(c, "B")
            # 执行之前的插件
            self.use_before_plugin(c)
            try:
                self.execute_element(kind(c))
            except Exception as e:
                self.use_error_plugin(c)
                raise RuntimeError("Step: {0} ErrorMsg:'{1}',case:'{2}'".format(c.id, e, current_case))
            # 执行浏览器动作
            self.browser_action(c, "A")
            # 执行之后的插件
            self.use_after_plugin(c)
