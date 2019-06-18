from hashlib import sha1

from util.package.base import BasePackage


class Packages:

    def __init__(self):
        self.__packages = []
        self.__index = 0
        self.info = {}
        self.revers = {}
        self.man = {}
        self.id = "0" * 40

    def add_package(self, package):
        if isinstance(package, BasePackage) and package is not None:
            if package.id != "" and package.name != "":
                # 生成信息 package_id ：package_name
                self.info[package.id] = package.name
                self.revers[package.name] = package.id
            else:
                raise ValueError("package`s name and id is Empty")
            self.__packages.append(package)
            # todo:优化
            self.man[package.id] = self.__packages
            return 0
        return -1

    def gen_id(self):
        strs = "{}".format(self.__packages.__class__)
        self.id = sha1(strs.encode("utf8")).hexdigest()

    def __getitem__(self, item):
        """
        根据id获取对应的name
        :param item:
        :return:
        """
        # 如果长度为40表示使用id来获取
        if len(item) == 40:
            return self.info[item]
        # 如果不是则使用name来获取
        return self.revers[item]

    def __contains__(self, item):
        # 如果长度为40表示使用id来获取
        if len(item) == 40:
            return item in self.info
        # 如果不是则使用name来获取
        return item in self.revers

    def __missing__(self, key):
        return "No such key {}".format(key)

    def reset_index(self):
        self.__index = 0

    def all_packages(self):
        if self.id == "0" * 40:
            self.gen_id()
        return self.__packages

    def get_package_by_name(self, name):
        return self.man[self.revers[name]]

    def __len__(self):
        return len(self.__packages)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < len(self.__packages):
            data = self.__packages[self.__index]
            self.__index += 1
            return data
        else:
            self.__index = 0
            raise StopIteration()


if __name__ == '__main__':
    a = Packages()

    print(len(a))
