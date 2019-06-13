# SeleniumAutoTest

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
# 设置缓存文件的路径
url = {
    "page_object_file_path": "./"
}
# 配置selenium
selenium = {
    "browser": "firefox",# 指定使用的浏览器
    "os": "linux", # 指定使用的操作系统，如果没有指定将使用当前系统
    "driver_path": "/home/amdins/桌面/geckodriver" # 驱动地址
}
``` 

### 测试用例说明
测试用例暂时只支持excel,不过可以自己增加读取方式

用例说明：

|编号|描述|生成的元素名称|元素类别|定位方式|定位值|动作|输入值|等待方式|等待时间|执行动作|使用插件|断言条件|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|1|登录链接跳转|loginLink|按钮|link_text|登录|点击|不等待|0|null|null|assertion:B,screen:B|contains(title,'登录')|

####  插件

填写插件名，以逗号分割,需要指定什么时候执行B表示在执行测试用例之前执行，A表示在执行测试用例之后执行
 
不是使用插件可以置空或者为null
 
#### 断言方式:

断言使用断言插件完成，断言方式可自定义

#### 执行动作
执行动作表示浏览器要执行的动作,滚动条操作，窗口切换等（暂未完成）

## 使用方式
### 基本使用
```python
from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from managers.manager import Manager
from plugin.assertplugin import AssertPlugin

if __name__ == '__main__':
    # 指定读取的Reader
    r = ExcelReader("/home/amdins/桌面/teach/seleniums/selenium/case.xlsx")
    man = Manager()
    # 使用指定的Reader
    man.select_reader(r)
    # 使用默认的执行器
    man.register_executor(NormalExecutor())
    # 注册所使用的插件
    man.register_plugin(AssertPlugin("assertion"))
    # 解析
    man.porking()
    # 执行
    man.get_execute().run_by_name("case")
```

### 自定义插件

注意：
断言插件默认已经被注册，名称为assertion

可以指定插件在什么时刻执行

例如：
在测试用例之前执行：assertion:B

断言插件暂时没有完成！

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

## TODO

- [x] 框架骨架
- [x] 插件支持
- [ ] 测试报告生成
- [ ] 邮件支持
- [ ] 丰富插件
- [ ] 异步执行 
- [ ] 丰富元素动作
- [ ] 丰富浏览器行为
- [ ] 从数据库读取测试用例
- [ ] 远程测试支持
- [ ] 作为Docker服务
