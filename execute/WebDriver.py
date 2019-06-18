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
from util.tools.strings import wash_string


class Driver:

    def __init__(self, os="windows"):
        self.os = os
        self.__driver = None

    def start(self, browser, driverpath):
        if not self.__check_path(driverpath):
            raise ValueError("驱动路径错误:" + driverpath)
        self.__driver = self.__init_browser(browser, driverpath)

    def __init_browser(self, browser, driverpath):
        name = self.to_lower(browser)
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

    def to_lower(self, string):
        string = wash_string(string)
        if isinstance(string, str):
            return string.lower()
        return string

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
        by = self.__convert(by)
        ele = WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((by, value)))
        if isinstance(ele, WebElement):
            return ele
        return

    def __convert(self, string):
        # class_name
        if isinstance(string, str):
            arr = string.split("_")
            res = " ".join(arr)
            support = ["id", "xpath", "link text", "partial link text", "name", "tag name", "class name",
                       "css selector"]
            if res not in support:
                raise ValueError("定位方式错误,必须是以下几种,{0}".format(support))
            return res

        raise ValueError(string + "不是字符串类型")

    def close(self):
        self.__driver.close()

    def get_element(self, info):
        if isinstance(info, tuple):
            method, value = info
            return self.find_element(method, value)
        raise ValueError(info + "不是元组类型")

    # todo:元素拖动
    def execute_element(self, result):
        """
        支持的方式：
            js 脚本
            点击
            输入
            选择框
            切换iframe
        :param result:
        :return:
        """
        ele = self.find_with_timeout(result.method, result.value, 5)
        if isinstance(result, Element):
            if result.action == "click":
                return ele.click()
            if result.action == "send_keys":
                return ele.send_keys(result.inputs)
            if result.action == "select":
                # sex_select.select = (text,男)
                # todo: deselect
                select = Select(ele)
                res = re.findall("\((index|value|text),(\w{1,30}|\d{1,20})\)", result.select)
                try:
                    method, value = res[0]
                    if method == "index":
                        select.select_by_index(value)
                        return ele
                    if method == "text":
                        select.select_by_visible_text(value)
                        return ele
                    if method == "value":
                        select.select_by_value(value)
                        return ele
                except ValueError:
                    raise ValueError("'{}',格式错误".format(result.select))
            if result.action == "iframe":
                self.__driver.switch_to.frame(ele)
                return ele
            if result.action == "js":
                self.__driver.execute_script(result.js)
                return ele
            # if result.action == "drop":

        else:
            raise ValueError("{} is not Element".format(result.__class__))

    def find_element(self, method, value):
        """
        定位元素
        :param method: 定位方式
        :param value: 值
        :return:
        """
        method = self.__convert(method)
        return self.__driver.find_element(method, value)

    def select_element(self, method, value):
        """
        option元素选择
        :param method:定位方式
        :param value:值
        :return:
        """
        method = self.__convert(method)
        ele = self.__driver.find_element(method, value)
        return Select(ele)

    def drop_element(self, method1, value1, method2, value2):
        action = ActionChains(self.__driver)
        method1 = self.__convert(method1)
        method2 = self.__convert(method2)
        source = self.__driver.find_element(method1, value1)
        target = self.__driver.find_element(method2, value2)
        return action.drag_and_drop(source, target)

    def move_to(self, method1, value1, x, y):
        action = ActionChains(self.__driver)
        method1 = self.__convert(method1)
        ele = self.__driver.find_element(method1, value1)
        return action.click_and_hold(ele).move_by_offset(x, y).release().perform(ele)

    @property
    def web_driver(self):
        return self.__driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
