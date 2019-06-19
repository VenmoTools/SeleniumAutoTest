import os
import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import config
from execute.object import Element
from util.tools.element import convert
from util.tools.pasers import Parser
from util.tools.strings import to_lower_with_wash


class Driver:

    def __init__(self, os="windows"):
        self.os = os
        self.__driver = None

    def start(self, browser, driverpath):
        if not self.__check_path(driverpath):
            raise ValueError("驱动路径错误:" + driverpath)
        self.__driver = self.__init_browser(browser, driverpath)

    def __init_browser(self, browser, driverpath):
        name = to_lower_with_wash(browser)
        if name == "firefox":
            return webdriver.Firefox(executable_path=driverpath,
                                     service_log_path=os.path.join(config.selenium["log_path"],
                                                                   config.selenium["log_name"]))
        elif name == "chrome":
            return webdriver.Chrome(executable_path=driverpath,
                                    service_log_path=os.path.join(config.selenium["log_path"],
                                                                  config.selenium["log_name"]))
        elif name == "ie":
            return webdriver.Ie(executable_path=driverpath, service_log_path=os.path.join(config.selenium["log_path"],
                                                                                          config.selenium["log_name"]))
        elif name == "edge":
            return webdriver.Edge(executable_path=driverpath,
                                  service_log_path=os.path.join(config.selenium["delete_log"],
                                                                config.selenium["log_name"]))
        else:
            raise ValueError(browser + " 不支持")

    def get(self, url):
        self.__driver.get(url)

    def __check_path(self, path):
        if self.os == "windows":
            return self.__check_path_win(path)
        elif self.os == "linux":
            return True

    def __check_path_win(self, path):
        # C:\xxx\xxx\xx.exe
        if isinstance(path, str):
            path = path[1:]
            if not path.startswith(":"):
                return False
            return path.endswith(".exe")
        raise ValueError(path + "不是字符串")

    def sleep(self, sec):
        """
        固定时长等待
        :param sec:等待时间
        :return:
        """
        if sec < 0:
            raise ValueError("等待时间必须为正整数")
        time.sleep(sec)

    def implicitly_wait(self, sec):
        """
        显式等待
        :param sec:等待时间
        :return:
        """
        if sec < 0:
            raise ValueError("等待时间必须为正整数")
        self.__driver.implicitly_wait(sec)

    def find_with_timeout(self, by, value, timeout=30):
        by = convert(by)
        ele = WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((by, value)))
        if isinstance(ele, WebElement):
            return ele
        return

    def close(self):
        self.__driver.close()

    def get_element(self, info):
        if isinstance(info, tuple):
            method, value = info
            return self.find_element(method, value)
        raise ValueError(info + "不是元组类型")

    def execute_element(self, result):
        """
        支持的方式：
            js 脚本
            点击
            输入
            选择框
            切换iframe
            拖动元素
            滚动条
        :param result:
        :return:
        """
        ele = self.find_with_timeout(result.method, result.value, 5)
        if isinstance(result, Element):
            # 按钮
            if result.action == "click":
                return ele.click()
            # 输入框
            if result.action == "send_keys":
                return ele.send_keys(result.inputs)
            # 选择框
            if result.action == "select":
                # sex_select.select = (text,男)
                # todo: deselect
                method, value = Parser.parser_select_value(result.inputs)
                select = Select(ele)
                if method == "index":
                    select.select_by_index(value)
                    return ele
                if method == "text":
                    select.select_by_visible_text(value)
                    return ele
                if method == "value":
                    select.select_by_value(value)
                    return ele
            # 切换iframe
            if result.action == "iframe":
                self.__driver.switch_to.frame(ele)
                return ele
            # 执行js代码
            if result.action == "js":
                self.__driver.execute_script(result.inputs)
                return ele
            # 拖动元素
            if result.action == "drop":
                # to(x,y)
                # to(ele(method,value))
                action = ActionChains(self.__driver)
                if "ele" in result.inputs:
                    methods, values = Parser.parser_ele_drop_action_ele(result.inputs)
                    to_ele = self.find_with_timeout(methods, values)
                    action.click_and_hold(ele).move_to_element(to_ele).release().perform()
                else:
                    x, y = Parser.parser_ele_drop_action_location(result.inputs)
                    action.click_and_hold(ele).move_by_offset(x, y).release().perform()
                return ele
            # 滚动条
            if result.action == "scroll":
                methods, values = Parser.parser_scroll_by_js(result.inputs)
                if "ele" in result.inputs:
                    local = self.find_with_timeout(methods, values).location
                    self.__driver.execute_script(
                        "document.documentElement.scrollTo({1},{0})".format(local["x"], local["y"]))
                if methods.lower() == "to_left":
                    if values == "max_left":
                        return self.__driver.execute_script(
                            "document.documentElement.scrollLeft=0".format(values))
                    if values == "max_right":
                        return self.__driver.execute_script(
                            "document.documentElement.scrollLeft=document.documentElement.scrollLeftMax".format(values))
                    self.__driver.execute_script("document.documentElement.scrollLeft={}".format(values))
                elif methods.lower() == "to_top":
                    if values == "max_top":
                        return self.__driver.execute_script(
                            "document.documentElement.scrollTop=scrollMaxX".format(values))
                    if values == "max_down":
                        return self.__driver.execute_script(
                            "document.documentElement.scrollTop=scrollMaxY".format(values))
                    self.__driver.execute_script("document.documentElement.scrollTop={}".format(values))
                elif methods.lower() == "to_index":
                    try:
                        x, y = re.findall("^\((\d+),(\d+)\)$", values)[0]
                    except IndexError:
                        raise SyntaxError("滚动条语法错误,{}".format(result.inputs))
                    self.__driver.execute_script("document.documentElement.scrollTo({1},{0})".format(x, y))
            # 双机
            if result.action == "dclick":
                return ActionChains(self.__driver).double_click(ele).perform()
            # 键盘操作
        else:
            raise ValueError("{} is not Element".format(result.__class__))

    def find_element(self, method, value):
        """
        定位元素
        :param method: 定位方式
        :param value: 值
        :return:
        """
        method = convert(method)
        return self.__driver.find_element(method, value)

    def select_element(self, method, value):
        """
        option元素选择
        :param method:定位方式
        :param value:值
        :return:
        """
        method = convert(method)
        ele = self.__driver.find_element(method, value)
        return Select(ele)

    def drop_element(self, method1, value1, method2, value2):
        action = ActionChains(self.__driver)
        method1 = convert(method1)
        method2 = convert(method2)
        source = self.__driver.find_element(method1, value1)
        target = self.__driver.find_element(method2, value2)
        return action.drag_and_drop(source, target)

    def move_to(self, method1, value1, x, y):
        action = ActionChains(self.__driver)
        method1 = convert(method1)
        ele = self.__driver.find_element(method1, value1)
        return action.click_and_hold(ele).move_by_offset(x, y).release().perform(ele)

    @property
    def web_driver(self):
        return self.__driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
