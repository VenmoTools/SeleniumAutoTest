import os
import re
import time
from hashlib import sha1

import config
from case.cases.base import BaseCase
from util.package.base import BasePackage
from util.processor.process import Processor
from util.tools.element import kind
from util.tools.file import FileUtil


class ProcessPackage(BasePackage):
    """
    一个package存放一个Process
    """

    def gen_id(self):
        now = time.time().hex().encode("utf8")
        self.__id = sha1(now).hexdigest()

    def __init__(self, name):
        super().__init__(name)
        self.__case = None
        self.gen_id()

    def pack(self, data):
        self.names.append(data.name)
        self.__case = data

    def unpack(self):
        return self.__case


class GenPo:

    def __init__(self, filename):
        self.file = self.file(filename)
        self.filename = filename
        self.exist = []
        self.exists()
        self.__key_to_value = {
            "输入": "send_keys",
            "点击": "click",
            "iframe": "iframe",
            "js": "js",
            "选择框": "select",
            "拖动": "drop",
            "双击": "dclick",
            "按键": "press_key"
        }

    def file(self, filename):
        dirs = os.path.join(config.url["page_object_file_path"], "temp")
        if os.path.exists(dirs):
            FileUtil.remove(dirs)
        os.mkdir(dirs)
        filename = os.path.join(dirs, filename)
        if os.path.exists(filename):
            os.remove(filename)
        return open(file=filename, mode="x", encoding="utf8")

    def execute(self, cmd):
        if isinstance(cmd, ProcessPackage):
            process = cmd.unpack()
        elif isinstance(cmd, Processor):
            process = cmd
        else:
            raise ValueError("{0} 必须是ProcessPackage或者Processor".format(cmd))
        self.write(process)

    def write_section(self, name):
        self.file.write("[{0}]\n".format(name))

    def write_attr(self, case):
        if isinstance(case, BaseCase):
            self.file.write("{0}.method={1}\n".format(kind(case), case.method))
            self.file.write("{0}.value={1}\n".format(kind(case), case.value))
            self.file.write(self.__action(case))

    def __action(self, case):
        if isinstance(case, BaseCase):
            if case.action == "点击":
                data = "{0}.action={1}\n".format(kind(case), "click")
                return data
            else:
                try:
                    name = kind(case)
                    data = "{0}.action={1}\n".format(name, self.__key_to_value[case.action])
                    data += "{0}.input_value={1}\n".format(name, case.input)
                    return data
                except KeyError:
                    raise ValueError("{} not support".format(case.action))
        raise TypeError("{} is not BaseCase".format(case.__class__))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def close(self):
        self.file.close()

    def write(self, process):
        if isinstance(process, Processor):
            if process.name in self.exist:
                return
                # raise ValueError(exec.name + "已经存在")
            self.write_section(process.name)
            for i in process:
                self.write_attr(i)
            self.exist.append(process.name)
            return
        raise ValueError(process.name + "必须是Processor对象")

    def exists(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                for line in f.readlines():
                    res = re.findall("\[[\w]{0,50}\]", line)
                    self.exist.append("".join(res).strip("[").strip("]"))


if __name__ == '__main__':
    now = time.time().hex().encode("utf8")
    res = sha1(now).hexdigest()
    print(len(res))
