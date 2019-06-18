"""
1 导入包
2 模块变量
3 类：
    1. 类变量
    2. 类方法
    3. test常用函数
    4. 测试用例


"""
import os

import config


class GenMethod:

    def __init__(self):
        self.name = ""
        self.param = []
        self.content = []
        self.annotation = []
        self.class_self = True

    def change(self):
        self.class_self = False

    def add_name(self, name):
        self.name = name

    def add_param(self, data):
        self.param.append(data)

    def add_content(self, content):
        self.content.append(content)

    def add_annotation(self, annotation):
        self.annotation.append(annotation)

    def gen(self):
        """
        \t{0}\n
        \tdef {1}(self{2}):\n
        \t\t{3}

        :return:
        """
        template = """\t{0}\n\tdef {1}({2}{3}):\n\t\t {4}"""

        # 处理类方法和实例方法
        types = "self"
        if not self.class_self:
            self.annotation.append("@classmethod")
            types = "cls"
        # 处理函数参数
        params = ""
        if len(self.param) > 0:
            params += ","
            params += ",".join(self.param)
        # 处理内容
        content = "\n\t\t".join(self.content)

        # 处理注解
        annotations = "\n\t".join(self.annotation)

        return template.format(annotations, self.name, types, params, content)


class GenClass:

    def __init__(self):
        self.class_name = ""
        self.has_father = False
        self.father = []
        self.class_var = []
        self.annotation = []
        self.methods = []

    def set_name(self, name):
        if "Test" in name:
            self.class_name = name
        else:
            self.class_name = "Test{}".format(name)

    def add_class_var(self, var):
        self.class_var.append(var)

    def add_annotation(self, anno):
        self.annotation.append(anno)

    def add_method(self, method):
        if isinstance(method, GenMethod):
            self.methods.append(method.gen())

    def add_father(self, father):
        self.father.append(father)

    def gen(self):
        template = """{0}\nclass {1}{2}:\n{3}"""
        self.has_father = True if len(self.father) > 0 else False
        # 类注解
        anno = "\n".join(self.annotation)
        father = ""
        if self.has_father:
            data = ",".join(self.father)
            father = "(%s)" % data

        method = "\tpass"

        if len(self.methods) > 0:
            method = ""
            method += "\n".join(self.methods)

        return template.format(anno, self.class_name, father, method)


class GenTest:

    def __init__(self, name):
        self.package = ["import unittest"]
        self.mod_var = []
        self.clazz = GenClass()
        self.clazz.set_name(name)
        self.clazz.add_father("unittest.TestCase")

    def add_package(self, package):
        self.package.append(package)

    def add_mod_var(self, var):
        self.mod_var.append(var)

    def register_exec(self, name):
        con = "run.exc_one('%s')" % name
        self.add_test_case(name=name, content=con)

    def add_set_up(self, content):
        method = GenMethod()
        method.add_name("setUp")
        if isinstance(content, list):
            for line in content:
                method.add_content(line)
        elif isinstance(content, str):
            method.add_content(content)
        self.clazz.add_method(method)

    def add_tear_down(self, content):
        method = GenMethod()
        method.add_name("tearDown")
        if isinstance(content, list):
            for line in content:
                method.add_content(line)
        elif isinstance(content, str):
            method.add_content(content)
        self.clazz.add_method(method)

    def add_set_class_up(self, content):
        method = GenMethod()
        method.add_name("setUpClass")
        method.change()
        if isinstance(content, list):
            for line in content:
                method.add_content(line)
        elif isinstance(content, str):
            method.add_content(content)
        self.clazz.add_method(method)

    def add_tear_class_down(self, content):
        method = GenMethod()
        method.add_name("tearDownClass")
        method.change()
        if isinstance(content, list):
            for line in content:
                method.add_content(line)
        elif isinstance(content, str):
            method.add_content(content)
        self.clazz.add_method(method)

    def add_test_case(self, content, name, param=None):
        method = GenMethod()
        method.add_name("test_{0}".format(name))
        if isinstance(content, list):
            for line in content:
                method.add_content(line)
        elif isinstance(content, str):
            method.add_content(content)
        self.clazz.add_method(method)

    def gen(self):

        template = """{0}\n\n{1}\n\n{2}"""

        packages = "\n".join(self.package)
        mod = ""
        if len(self.mod_var) > 0:
            mod += "\n".join(self.mod_var)
        classs = self.clazz.gen()

        return template.format(packages, mod, classs)

    def save_file(self, filename):
        pa = os.path.join(config.report["file_url"], filename)
        if not os.path.exists(config.report["file_url"]):
            os.mkdir(config.report["file_url"])
        with open(pa, "w", encoding="utf8") as f:
            f.write(self.gen())


if __name__ == '__main__':
    test = GenTest("TestLogin")
    test.add_set_up("self.driver = webdriver.Firefox(executable_path='/home/amdins/桌面/geckodriver')")
    test.add_tear_down("self.driver.close()")
    test.add_test_case(name="open", content="self.driver.get('http://192.168.1.35:8080/DBShop')")
    filename = "gen_test.py"
    with open(filename, "w")as f:
        f.write(test.gen())
