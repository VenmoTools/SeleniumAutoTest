import re


class Parser:

    @classmethod
    def parser_ele_drop_action_location(cls, line):
        """
        解析元素移动的坐标
        :param line:
        :return: 元组 x,y坐标
        """
        # to(x,y)
        if "to" not in line:
            raise SyntaxError("拖动元素语法错误,{}".format(line))

        res = re.findall("^to\((\d+?),(\d+?)\)$", line)
        if len(res) != 1:
            raise SyntaxError("拖动元素语法错误,{}".format(line))

        return res[0]

    @classmethod
    def parser_ele_drop_action_ele(cls, line):
        # to(ele(method,value))
        if "to" not in line:
            raise SyntaxError("拖动元素语法错误,{}".format(line))

        res = re.findall("^to\(ele\((\w+),(\w+)\)\)$", line)
        if len(res) != 1:
            raise SyntaxError("拖动元素语法错误,{}".format(line))

        return res[0]

    @classmethod
    def parser_scroll_by_js(cls, line):
        # scroll(js(to_down,1000))
        # scroll(js(to_down,top_max))
        # scroll(js(to,(192,138)))
        # scroll(ele(id,name))
        if "js" not in line and "scroll" not in line:
            raise SyntaxError("滚动条语法错误,{}".format(line))
        if "ele" in line:
            res = re.findall("ele\((\w+),(\w+)\)", line)
            if len(res) != 1:
                raise SyntaxError("滚动条语法错误,{}".format(line))
            return res[0]
        # ele\((\w+),(\w+)\)
        res = re.findall("^scroll\(js\((\w+),(\d+|\w+|\(.+\))\)\)$", line)
        if len(res) != 1:
            raise SyntaxError("滚动条语法错误,{}".format(line))

        return res[0]

    @classmethod
    def parser_select_value(cls,line):
        res = re.findall("\((index|value|text),(\w{1,30}|\d{1,20})\)", result.inputs)
        if len(res) != 1:
            raise SyntaxError("滚动条语法错误,{}".format(line))
        return res[0]
