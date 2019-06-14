# SeleniumAutoTest

[中文请点击](Readmes/README.md)

## Introduction

The framework can focus on and write test cases, the tedious coding work is all dry,
can customize plug-ins, such as cracking verification codes, failed screenshots, etc.
After the test case is written, you can automatically test, generate reports, 
and send mail by simply specifying the plug-ins and test cases used


# Getting Started

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
# Basic class and use 

+ Reader: A tool for reading data, you can specify a file or database or customize
+ Case: The positioning method of an element performs actions, etc. (one execution step)
+ Process: A series of execution steps (sorted by id)
+ Package: The basic unit of transportation is used to package a Process or multiple Processes
+ Packages: Collection of all packages
+ Packager: Responsible for combining Case and Process into Packages to form Packages
+ Porter: Responsible for fetching data from Packager to CaseManager
+ CaseManager: Responsible for managing multiple Porters and Packagers
+ ExecuteCenter: Responsible for obtaining Packages from CaseManager's porters and distributing them to Manager
+ Manager: Assign each package in packages to a registered Executor
+ Executor: Responsible for unpacking the package to get Process and execute
+ PluginCenter: Plugin Center, responsible for plugin registration management, etc.
+ Plugin: Plugin, register the function to PluginCenter after the function is implemented, and call the function when testing
+ Generator: used to generate Test scripts
+ Report: Execute use case generation report

# Implementation process

Read the test case (db, file) by Reader -> Form each execution step (Case) -> Multiple execution steps to form the process (Process)

Packager Packages Process -> Multiple Packages Form Packages (Packages, Scalable to Asynchronous Operations, Distributed Operations)

Shipment of Packages to CaseManager by Porter -> Scheduled by Manager to Command Execution Center (ExecutorCenter)

ExecutorCenter unpacks and distributes to the executor -> each executor performs the task assigned to itself

# Dependent library
1. PIL 
2. pytesseract
3. matplotlib
4. opencv
5. selenium

# PageObject syntax convention
PageObject will automatically generate xxx.ini files based on test cases, which will be cleaned each time it is executed.


1.All sections are elements required for a test flow

2.All elements are named:
```
elementName.method -> indicates how the element is positioned
elementName.value  -> represents the value of the element's position
```
3.Elemental positioning
```
"id": id targeting
"xpath": xpath targeting
"link_text" link text
"partial_link_text": text containing link
"name": element name
"tag_name": element tag name
"class_name": class name
"css_selector": css selector
```
4.Element name naming
```
Name: 
     elementName_controlName
     The meaning of the elements such as username, password, etc. are named using a camel
     
E.g:
     Input box:
          ElementName _input:
                Username input box -> user_input
                Password input box -> pwd_input
                Keyword search input box -> kw_search_input
     Checkbox:
          ElementName _checkbox:
                Automatic login checkbox -> autoLogin_checkbox     
```
5.Elemental behavior

Each element gives a certain behavior

Button behavior can be click, can be drag

The input box can be a click, it can be an input

```
Complete naming:
     Element name_control name.action = behavior
E.g:
     Password input box
     registerPassword_input.method=id
     registerPassword_input.value=user_password
     registerPassword_input.action=send_keys
     registerPassword_input.input_value=123456
```
# Configuration instructions

The configuration file is placed in managers/config.py

```python

# Set the path to the cache file
url = {
    "page_object_file_path": "./"
}
#  Configure selenium
selenium = {
    "browser": "firefox",# specifies the browser to use
    "os": "linux", # specifies the operating system to be used, if not specified, the current system will be used.
    "driver_path": "/home/amdins/桌面/geckodriver" # Browser driver address
}
# Configure the path to store test scripts
report = {
    "file_url": "/home/amdins/桌面/text"
}
# Configure settings for storing test cases
case = {
    "type": "excel", # set the read case type
    "url": "/home/amdins/桌面/SeleniumAutoTest/case.xlsx", #  If it is a database, the url is the database link address
}
# All plugin names need to be registered in the plugins
plugins = [
    "assertion"
]
```

# Test case description
Test cases only support excel for the time being, but you can increase the reading method yourself.

Use case description:

|id|description|Generated element name|Element category|Targeting|Positioning value|action|input value|Waiting mode|waiting time|Execution action|Using plugins|Assertion condition|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|1|Login link jump|loginLink|button|link_text|login|click|notWaiting|0|null|null|assertion:B,screen:B|contains(title|none|::'LoginPage')|

# Plugin
Fill in the plugin name, separated by commas, you need to specify when to execute B to execute before executing the test case, and A to execute after executing the test case.
 
Not using a plugin can be empty or null

# Assertion mode
Assertions are done using the assertion plugin, and the assertion mode is customizable

# Action (element action)

The element actions are as follows:
1. Click (click on the element)
2. Input (need to write the input value in the input value)
3. Select (select the box, enter the value you need to write the content in the input value eg: (text, male), indicating that the option to use the text mode to select the value of male)
4. js (js code to be executed needs to write the input content in the input value)
5. iframe (switch iframe, the default value is change)

# Custom plugin

note:
Assertion plugin is already registered by default, the name is assertion

Can specify when the plugin is executing

E.g:
Execute before the test case: assertion: B (before)
Execute after the test case: assertion: A (After)


```python
from plugin.base import BasePlugin
from exception.assertion import Assertion

class ScreenPlugin(BasePlugin):

    def start(self, driver,case):
        """
            Driver for webdriver object
            Case is the current execution case
        """
        if case.assertion not in driver.page_source:
            raise Assertion()
```
# Assertion plugin introduction

Assertion plugin throws AssertionError() when assertion fails

## grammars

### Assertive keyword
1. contains
2. exist (to be completed)
3. is (consistent)
4. true (whether the result is True)
5. false (whether the result is False)
6. enable (the element is available)
7. display (the element is visible)
8. selected (whether the element is selected)
9. notnull (not empty)


### Usage
Is (content <can be text or element execution action>:: 'assertion value')

Element keyword
+ title: assert the browser title value
+ element: get the element
+ element_is: determine the element type
+ element_attr: get the element value
+ element_property: get the element attribute
+ element_text: get the element text information
+ js: execute javascript command

### Elemental grammar
#### Get the page title

Title

#### Get element attribute values
Use back quotation marks '`'
```
element_attr|`location method`, `location value`, `property name`|

```
E.g:
```
element_attr|`id`,`username`,`data`|
```

#### Get element properties
Use back quotation marks '`'
```
element_property|`location method`, `location value`, `property name`|

```
E.g:
```
element_property|`id`,`username`,`data`|
```
#### Executing js code

```
js|alter('hello')|
```

### Example

#### Assertion element value
```html
<a class="big">hello</a>
```
```
is(element_text|`class`,`.big`|::'hello')
```

#### Assertion element attribute
```html
<a class="big" data="1">hello</a>
```
```
is(element_attr|`class`,`.big`,`data`|::'1')

```

#### Assert javascript command execution result

```
<div id="best-content" accuse="aContent" class="best-text mb-10">
    <div class="wgt-best-mask">
        <div class="wgt-best-showbtn">
        show all<span class="wgt-best-arrowdown"></span>
        </div>
    </div>
    hello world
</div>

```

```
is(js|`return document.getElementById("best-content").innerText;`|::'hello world')
```

## testing report
Implementation principle:
Generate xx_test.py file according to test case, then use unittest's testLoader, combined with TestRunner


```python
cover = unittest.defaultTestLoader.discover("<path>", pattern="*_test.py")
with open("result.html", 'wb') as f:
    HTMLTestRunner(title="name of test", description="case description",
                   tester="who test",
                   stream=f).run(cover)
```

## Script generator usage
```python
from case.reader.excel import ExcelReader
from execute.driverexecute import NormalExecutor
from plugin.assertplugin import AssertPlugin
from report.Runner import Run
# generator
r = Run()
# register executor
r.add_executor(NormalExecutor())
# register plugin
r.add_plugin(AssertPlugin("assertion"))
# register Reader
r.add_reader(ExcelReader())
# generate file
r.generator_file("case")

```

#### Generate Result
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


# TODO List
- [x] frame skeleton
- [x] plugin support
- [x] rich element action
- [x] assertion plugin
- [x] Test report generation (to be improved)
- [ ] Email support
- [ ] Rich plugin
- [ ] Asynchronous execution
- [ ] Rich browser behavior
- [ ] Read test cases from the database
- [ ] Remote test support
- [ ] as a Docker service

# Forgive me for using google translation
