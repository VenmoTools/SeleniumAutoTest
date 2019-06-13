import os
import re
import time
from hashlib import sha1

from case.cases.base import BaseCase
from managers import config
from util.package.base import BasePackage
from util.processor.process import Processor


class ProcessPackage(BasePackage):

    def gen_id(self):
        now = time.time().hex().encode("utf8")
        self.id = sha1(now).hexdigest()

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

    def file(self, filename):
        dir = os.path.join(config.url["page_object_file_path"], "temp")
        if os.path.exists(dir):
            self.remove(dir)
        os.mkdir(dir)
        filename = os.path.join(dir, filename)
        if os.path.exists(filename):
            os.remove(filename)
        return open(file=filename, mode="x", encoding="utf8")

    def remove(self, path):
        for f in os.listdir(path):
            os.remove(os.path.join(path,f))
        os.removedirs(path)

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
            self.file.write("{0}.method={1}\n".format(self.__gen_name(case), case.method))
            self.file.write("{0}.value={1}\n".format(self.__gen_name(case), case.value))
            self.file.write(self.__action(case))

            # todo:所有控件

    def __gen_name(self, case):
        if isinstance(case, BaseCase):
            if case.element_type == "输入框":
                return case.element_name + "_input"
            if case.element_type == "按钮":
                return case.element_name + "_button"

    def __action(self, case):
        if isinstance(case, BaseCase):
            if case.action == "点击":
                data = "{0}.action={1}\n".format(self.__gen_name(case), "click")
                return data
            if case.action == "输入":
                data = "{0}.action={1}\n".format(self.__gen_name(case), "send_keys")
                data += "{0}.input_value={1}\n".format(self.__gen_name(case), case.input)
                return data

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
                    # []
                    res = re.findall("\[[\w]{0,50}\]", line)
                    self.exist.append("".join(res).strip("[").strip("]"))
