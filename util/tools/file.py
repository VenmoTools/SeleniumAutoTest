import os

import config


class FileUtil:
    @classmethod
    def remove(cls, dirs):
        try:
            if os.path.exists(dirs):
                os.remove(dirs)
        except Exception:
            for file in os.listdir(dirs):
                abs_file = os.path.join(dirs, file)
                if os.path.isfile(abs_file):
                    os.remove(abs_file)
                elif os.path.isdir(abs_file):
                    os.removedirs(abs_file)
            os.removedirs(dirs)

    @classmethod
    def create_dir(cls, path, name):
        res = os.path.join(path, name)
        if os.path.exists(res):
            return
        os.mkdir(res)
        return res

file = os.path.join(config.case["case_info"], "temp.file")
FileUtil.remove(file)
