def wash_string(data):
    if isinstance(data,str):
        data = data.strip("\n")
        data = data.strip(" ")
        data = data.strip("“")
        data = data.strip("”")
        return data