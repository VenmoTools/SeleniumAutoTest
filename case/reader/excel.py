import xlrd

from case.reader.base import BaseReader

"""
{
    "package_name":"", #一个流程名
    "cases":[
        "name":[
            {},
            {}
        ],
    ]
}

"""


class ExcelReader(BaseReader):

    """
    从excel文件读取数据，可以自定义，生成的数据必须是dict

    """

    def __init__(self, path):
        self.path = path
        self.work = xlrd.open_workbook(path)
        self.data = {}

    def set_name(self, name):
        self.data["name"] = name

    def get_file_name(self):
        if isinstance(self.path, str):
            arr = self.path.split("/")
            name = arr[len(arr) - 1]
            name = name[:name.index(".")]
            return name

    def read(self):
        step = []
        self.set_name(self.get_file_name())
        for name in self.work.sheet_names():
            data = {}
            sheet = self.work.sheet_by_name(name)
            data[name] = self.read_one(sheet)
            step.append(data)
        self.data["cases"] = step
        return self.data

    def read_one(self, sheet):
        """
        每一个step必须要与定义的case属性名一致
        :param sheet:
        :return:
        """
        res = []
        for i in range(1, sheet.nrows):
            data = {"id": sheet.cell_value(rowx=i, colx=0),
                    "desc": sheet.cell_value(rowx=i, colx=1),
                    "element_name": sheet.cell_value(rowx=i, colx=2),
                    "element_type": sheet.cell_value(rowx=i, colx=3),
                    "method": sheet.cell_value(rowx=i, colx=4),
                    "value": sheet.cell_value(rowx=i, colx=5),
                    "action": sheet.cell_value(rowx=i, colx=6),
                    "input": sheet.cell_value(rowx=i, colx=7),
                    "wait_method": sheet.cell_value(rowx=i, colx=8),
                    "wait_time": sheet.cell_value(rowx=i, colx=9),
                    "execute_action": sheet.cell_value(rowx=i, colx=10),
                    "plugins": sheet.cell_value(rowx=i, colx=11),
                    "assertion":sheet.cell_value(rowx=i, colx=12)
                    }
            res.append(data)
        return res


if __name__ == '__main__':
    r = ExcelReader("/home/amdins/桌面/teach/seleniums/selenium/case.xlsx")
    res = r.read()
