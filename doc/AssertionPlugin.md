# 断言插件

## 断言关键字 
1. contains(包含)
2. exist(存在,待完成)
3. is(是否一致)
4. true(结果是否为True)
5. false(结果是否为False)
6. enable(元素是否可用)
7. display(元素是否可见)
8. selected(元素是否被选中)
9. notnull(不为空)

## 语法
is(内容<可以是文本也可以是元素执行动作>::'断言值')

### 元素关键字
+ title:断言浏览器title值
+ element: 获取元素
+ element_is: 判断元素类型
+ element_attr： 获取元素值
+ element_property: 获取元素属性
+ element_text: 获取元素文本信息
+ js: 执行js


### 元素语法
#### 获取网页标题

title

#### 获取元素属性值
使用反引号'`'
```
element_attr|`定位方式`,`定位值`,`属性名`|

```
例如：
```
element_attr|`id`,`username`,`data`|
```

#### 获取元素属性
使用反引号'`'
```
element_property|`定位方式`,`定位值`,`属性名`|

```
例如：
```
element_property|`id`,`username`,`data`|
```
#### 执行js代码

```
js|alter('hello')|
```

### 例子

#### 断言元素值
```html
<a class="big">你好</a>
```
```
is(element_attr|`class`,`.big`|::'你好')
```

#### 断言元素属性
```html
<a class="big" data="1">你好</a>
```
```
is(element_attr|`class`,`.big`,`data`|::'1')

```

#### 断言js执行结果

```
<div id="best-content" accuse="aContent" class="best-text mb-10">
    <div class="wgt-best-mask">
        <div class="wgt-best-showbtn">
        展开全部<span class="wgt-best-arrowdown"></span>
        </div>
    </div>
    hello world
</div>

```

```
is(js|`return document.getElementById("best-content").innerText;`|::'hello world')
```
