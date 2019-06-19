def wash_string(data):
    if isinstance(data,str):
        data = data.strip("\n")
        data = data.strip(" ")
        data = data.strip("“")
        data = data.strip("”")
        return data


def trim_space(data):
    if isinstance(data, str):
        return data.replace(" ", "").replace("\n", "")
    raise TypeError("{} is not string".format(data))


def to_lower_with_wash(string):
    string = wash_string(string)
    if isinstance(string, str):
        return string.lower()
    return string