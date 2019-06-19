# SeleniumAutoTest

[EnglishVersion](./Readmes/README.md)

## 介绍
该框架可以专注与写测试用例，将繁琐的编码工作统统干掉，使用插件式，可自定义插件，例如破解验证码，失败截图等
测试用例写完后只需指定使用的插件和测试用例，便可自动测试，生成报告，发送邮件

### 基本类及用途
### 基本角色：
用例：
+ Reader： 读取数据的工具，可以指定文件或者数据库或者自定义
+ Case: 一个元素的定位方式执行动作等（一个执行步骤）
+ Process: 一系列执行步骤(根据id排序)
+ Package: 运输的基本单元 用于将一个Process或者多个Process打包
+ Packages: 所有Package的集合
+ Packager: 负责将Case和Process结合并打包成Package形成Packages
+ Porter： 负责从Packager取到数据送给CaseManager
+ CaseManager： 负责从管理多个Porter和Packager


执行：
+ ExecuteCenter: 负责从CaseManager的搬运工手中获取Packages，并分发给Manager
+ Manager： 将packages中的每一个package分配给已注册的Executor
+ Executor: 负责将package解包获取Process并执行
+ PluginCenter: 插件中心，负责插件的注册管理等
+ Plugin：插件，将功能实现后注册到PluginCenter中，测试时将调用功能

其他：   
+ Generator:用于生成Test脚本
+ Report:执行用例生成报告

### 执行流程
由Reader读取测试用例(db,file) -> 形成每个执行步骤(Case) -> 多个执行步骤形成流程(Process)

Packager将Process打包（Package） -> 多个Package形成包集合(Packages，可扩展成异步操作，分布式操作)  

由Porter（搬运工）将Packages运送到CaseManager中 -> 由Manager进行调度给命令执行中心（ExecutorCenter）

ExecutorCenter进行解包分发给执行器 -> 各执行器执行分配给自己的任务

## 依赖库
1. selenium
2. xlrd


## PageObject约定
PageObject会根据测试用例自动生成xxx.ini文件，每次执行时都会清理


1.所有section都是一个测试流程所需的元素

2.所有元素命名方式:
```
元素名.method 表示该元素的定位方式
元素名.value  表示该元素的定位的值
```
3.定位方式的写法
```
   "id"：id定位
   "xpath"：xpath定位
   "link_text" link的文字
   "partial_link_text"：包含link的文字
   "name"：元素name
   "tag_name":元素标签名
   "class_name": 类名
   "css_selector": css选择器
```
4.元素名命名方式
```
命名：元素名_控件名
    元素的含义例如用户名，密码等含义使用驼峰命名
例如
    输入框：
         元素名_input:
               用户名输入框-> user_input
               密码输入框  -> pwd_input
               关键词搜索输入框  -> kw_search_input
    复选框:
         元素名_checkbox:
               自动登录复选框 -> autoLogin_checkbox
```
5.元素的行为
每个元素都会赋予一定的行为

按钮行为可以是点击，可以是拖动

输入框可以是点击，可以是输入

```
完整命名方式:
    元素名_控件名.action = 行为
例如:
    密码输入框
    registerPassword_input.method=id
    registerPassword_input.value=user_password
    registerPassword_input.action=send_keys
    registerPassword_input.input_value=123456
```

## 配置说明
配置文件放在managers/config.py

```python

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

# 注册的插件
plugins = [
    "assertion"
]


``` 

### 测试用例说明
测试用例暂时只支持excel,不过可以自己增加读取方式

用例说明：

|编号|描述|生成的元素名称|元素类别|定位方式|定位值|动作|输入值|等待方式|等待时间|执行动作|使用插件|断言条件|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|5|播放歌曲|playSong|按钮|xpath|//a[@title='播放']|点击||不等待|0||assertion:A|is(element_text\|\`xpath\`,\`//em[contains(text(),'我爱的人走了')]\`\|::'我爱的人走了')


####  插件

填写插件名，以逗号分割,需要指定什么时候执行B表示在执行测试用例之前执行，A表示在执行测试用例之后执行,E表示在发生异常时执行插件
 
不是使用插件可以置空或者为null
 
#### 断言方式:

断言使用断言插件完成，断言方式可自定义

#### 执行动作
执行动作表示浏览器要执行的动作,滚动条操作，窗口切换等

可以指定动作在什么时候执行

例如：

在执行测试用例之前执行：win_max:B

在执行测试用例之后执行：win_min:A

浏览器执行动作优先级比插件的高

|动作名|含义|
|win_max|最大化窗口|
|win_min|最小化窗口|
|win_full|窗口全屏|
|switch_last|切换到最后一个窗口|
|switch_first|切换到第一个窗口|
|switch_index(index)|切换到第index个窗口|
|alter_accept|点击确定|
|alter_dismiss|点击取消|
|alter_send(str)|在alter中发送str|
|page_forward|网友前进|
|page_back|网页后退|

#### 动作(元素动作)
[元所动作说明](doc/ElementAction.md)

## 使用方式
### 基本使用
```python
from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin
from report.Runner import Run
from report.report import Report
if __name__ == '__main__':
    r = Run()
    r.add_executor(NormalExecutor())
    r.add_plugin(AssertPlugin("assertion"))
    r.add_reader(ExcelReader())
    r.generator_file("case")
    report = Report()
    report.start()

```

### 自定义插件

注意：
断言插件默认已经被注册，名称为assertion

可以指定插件在什么时刻执行

例如：
在测试用例之前执行：assertion:B (before)
在测试用例之后执行：assertion:A (After)

```python
from plugin.base import BasePlugin
from exception.assertion import Assertion

class ScreenPlugin(BasePlugin):

    def start(self, driver,case):
        """
            driver为webdriver对象
            case为当前执行的case
        """
        if case.assertion not in driver.page_source:
            raise Assertion()
```

## 断言插件使用

断言插件在断言失败时会抛出AssertionError()

[断言插件使用说明](doc/AssertionPlugin.md)


## 测试报告
实现原理:
根据测试用例生成xx_test.py文件,然后使用unittest的testLoader,结合TestRunner实现

```python
conver = unittest.defaultTestLoader.discover("路径", pattern="*_test.py")
with open("result.html", 'wb') as f:
    HTMLTestRunner(title="测试标题", description="测试描述",
                   tester="测试员",
                   stream=f).run(cover)
```

#### 脚本生成器使用
```python
from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin
from report.Runner import Run
# 生成器
r = Run()
# 注册执行器
r.add_executor(NormalExecutor())
# 注册插件
r.add_plugin(AssertPlugin("assertion"))
# 注册Reader
r.add_reader(ExcelReader())
# 生成文件
r.generator_file("case")

```

#### 生成效果
```python
import unittest
from managers.manager import Manager
from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin

man = Manager()
man.select_reader(ExcelReader())
man.register_executor(NormalExecutor())
man.register_plugin(AssertPlugin('assertion'))
execute = man.get_execute()


class case(unittest.TestCase):
	
	def test_Test(self):
		 execute.run_by_name('Test')

```
## 版本
[历史版本查看](CHANGELOG.md)

## TODO

- [x] 框架骨架
- [x] 插件支持
- [x] 丰富元素动作
- [x] 断言插件
- [x] 测试报告生成(待完善)
- [x] 邮件支持
- [x] 丰富浏览器行为
- [ ] 丰富插件
- [ ] 异步执行 
- [ ] 从数据库读取测试用例
- [ ] 远程测试支持
- [ ] 作为Docker服务
