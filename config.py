import os

# 当前文件路径
current_path = os.path.dirname(__file__)

# 元素名称转换映射关系
element_name = {
    "输入框": "_input",
    "按钮": "_button",
    "下拉列表": "_select",
    "iframe": "_iframe",
    "js": "_java_script",
    "链接": "_link",
}

url = {
    # 生成缓存路径
    "page_object_file_path": current_path,
    "delete": True
}

selenium = {
    # selenium使用的浏览器
    "browser": "firefox",
    # 当前平台，如果没有指定默认使用当前系统
    "os": "linux",
    # 浏览器驱动地址
    "driver_path": "/home/amdins/桌面/geckodriver",
    "log_path": current_path,
    "log_name": "geckodriver.log",
    "delete_log": True
}

report = {
    # 生成的测试脚本路径（是文件夹！）
    "file_url": "/home/amdins/桌面/text",
    # 测试报告路径
    "report_file_path": "home/amdins/桌面/text/report.html"
}

email = {
    "use_email": False,
    # 邮件使用的服务器
    "stmp_server_addr": "smtp.yeah.net",
    # 邮件中发送者邮箱
    "author": "VenmoSnake@example.com",
    # 邮件中接受者邮箱
    "recv_email": "Report@exmaple.com",
    # 邮箱服务器用户名
    "username": "Administrator",
    # 邮箱服务器密码
    "password": "AdministratorPwd",
    # 使用的邮箱模板，default表示使用默认的,如果使用自定义模板需要指定模板路径
    "template": "default",
    # 邮箱发送的信息
    "message": "Test Case",
    # 邮箱的Subject
    "title": "Test"
}

case = {
    # 选择测试用例的类型 excel表示用excel文件中读取，db表示从数据库读取
    "type": "excel",
    # 文件路径或者db的uri
    "url": "/home/amdins/桌面/SeleniumAutoTest/case.xlsx",
    # 生成的case信息文件路径
    "case_info": current_path,
    # 是否序列化Packages
    "serialize_packages": True,
    # 是否删除序列化文件
    "delete_serialize_packages": True,
    # 序列化路径
    "serialize_path": current_path,
    # 用例起始url
    "base_url": "https://music.163.com/"
}
image = {
    "path": current_path
}

# 注册的插件
plugins = [
    "assertion"
]
