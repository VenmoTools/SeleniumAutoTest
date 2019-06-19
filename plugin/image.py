import os
import time

import config
from plugin.base import BasePlugin
from util.tools.file import FileUtil


class ScreenPlugin(BasePlugin):

    def start(self, driver, case):
        name = time.strftime("%Y-%m-%d %H:%M:%S'", time.localtime(time.time()))
        path = os.path.join(FileUtil.create_dir(config.image["path"], "images"), "{0}_{1}.png".format(name, case.id))
        driver.web_driver.save_screenshot(path)
