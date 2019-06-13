from util.package.base import BasePackage


class Packages:

    def __init__(self):
        self.__packages = []
        self.__index = 0
        self.info = {}
        self.revers = {}
        self.man = {}

    def add_package(self, package):
        if isinstance(package, BasePackage) and package is not None:
            if package.id != "" and package.name != "":
                self.info[package.id] = package.name
                self.revers[package.name] = package.id
            else:
                raise ValueError("package`s name and id is Empty")
            self.__packages.append(package)
            # todo:优化
            self.man[package.id] = self.__packages
            return 0
        return -1

    def reset_index(self):
        self.__index = 0

    def all_packages(self):
        return self.__packages

    def get_package_by_name(self, name):
        return self.man[self.revers[name]]

    def __len__(self):
        return self.__packages

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
