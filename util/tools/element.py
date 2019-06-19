import config


def kind(case):
    try:
        return case.element_name + config.element_name[case.element_type]
    except KeyError:
        raise SyntaxError("{} is not supported".format(case.element_type))


def convert(string):
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
