---
title: Python 全栈之路系列之基础篇

tags: 
  - 编码
top: 1
categories: 
  - 💻 工作
  - 🐍Python
  - 全栈之路
  - 1-基础篇
date: 2020-05-23 18:21:46
permalink: /pages/40527e/
---

## Python 的诞生

Python 是著名的"`龟叔`"`Guido van Rossum(吉多·范罗苏姆)`在 1989 年圣诞节期间，为了打发无聊的圣诞节而编写的一个编程语言。

![guide](https://ansheng.me/wp-content/uploads/2016/12/1483014338667.jpg)

Python 语法很多来自 C，但又受到 ABC 语言的强烈影响，来自 ABC 语言的一些规定直到今天还富有争议，比如强制缩进，但这些语法规定让 Python 变得更易读。

`Guido van Rossum`著名的一句话就是**`Life is short, you need Python`**，译为：**`人生苦短，我用Python`**，一直到现在，无论在任何介绍 Python 这门强大的语言时，都会有提到。

截至到目前`2017年1月6日`，Python 在`Tiobe`的排名还是很靠前的，而且近几年来说 Python 上升的趋势还是特别稳定的，这两年一直保持在第四位，甚至已经超越 PHP 和 C#。

![Tiobe](https://ansheng.me/wp-content/uploads/2017/01/1483685458.png)

查询网站：http://www.tiobe.com/tiobe_index?page=index

我们还可以再解释下下通过`import this`查看 Python 语言的设计哲学：

```python
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

Python 唯一的缺点就是他的性能，它达不到像 C 和 C++这种编译性语言运行的那么快，但是我们通常都不需要考虑这个问题，因为有`PYPY`，它的运行速度比默认的`Cpython`要快很多。

## 在 Win10 下安装 Python3

**下载 Python 解释器**

64 位下载地址：https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe
32 位下载地址：https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe

**安装 Python 解释器**

下载下来之后双击安装，在安装的时候稍微需要注意一下就是需要修改默认的安装路径和和自动注册到系统环境变量勾选上。

![python](https://ansheng.me/wp-content/uploads/2017/01/1483690871.png)

![python](https://ansheng.me/wp-content/uploads/2017/01/1483691055.png)

然后就可以点击`Install`按钮进行安装了。

![python](https://ansheng.me/wp-content/uploads/2017/01/1483691189.png)

> 因为我们已经勾选自动注册环境变量，所以在这里就不需要修改环境变量，直接运行即可；

**DOS 测试**

右键开始菜单选择`命令提示符`，打开 CMD 窗口，

![python](https://ansheng.me/wp-content/uploads/2017/01/1483691401.png)

![python](https://ansheng.me/wp-content/uploads/2017/01/1483691480.png)

在 cmd 窗口中输入`python -V`指令查看安装的 Python 版本：

![python](https://ansheng.me/wp-content/uploads/2017/01/1483691631.png)

如果你得到的结果和我一样，那么你就安装好了`windows`下的`python`环境。

因为在`Mac os`和其他`unix`和`Linux`版本下都已经自带了 Python，这里我就不做太多介绍了。

## Python 实现方式

Python 身为一门编程语言，但是他是有多种实现方式的，这里的实现指的是符合 Python 语言规范的 Python 解释程序以及标准库等。

Python 的实现方式主要分为三大类

1. Cpython
2. Jpython
3. IronPython

### CPython

`Cpython`是默认的 Python 解释器，这个名字根据它是可移植的`ANSI C`语言代码编写而成的这事实而来的。

当执行 Python 执行代码的时候，会启用一个 Python 解释器，将源码`(.py)`文件读取到内存当中，然后编译成字节码`(.pyc)`文件，最后交给 Python 的虚拟机`(PVM)`逐行解释并执行其内容，然后释放内存，退出程序。

![python-day01-04](https://ansheng.me/wp-content/uploads/2016/12/1483015581.png)

当第二次在执行当前程序的时候，会先在当前目录下寻找有没有同名的 pyc 文件，如果找到了，则直接进行运行，否则重复上面的工作。

pyc 文件的目的其实就是为了实现代码的重用，为什么这么说呢？因为 Python 认为只要是 import 导入过来的文件，就是可以被重用的，那么他就会将这个文件编译成 pyc 文件。

python 会在每次载入模块之前都会先检查一下 py 文件和 pyc 文件的最后修改日期，如果不一致则重新生成一份 pyc 文件，否则就直接读取运行。

### Jython

Jython 是个 Python 的一种实现方式，Jython 编译 Python 代码为 Java 字节码，然后由 JVM（Java 虚拟机）执行，这意味着此时 Python 程序与 Java 程序没有区别，只是源代码不一样。此外，它能够导入和使用任何 Java 类像 Python 模块。

### IronPython

IronPython 是 Python 的 C#实现，并且它将 Python 代码编译成 C#中间代码（与 Jython 类似），然后运行，它与.NET 语言的互操作性也非常好。

## Python 简单入门

### Hello Word

一般情况下程序猿的第一个小程序都是简单的输出`Hello Word!`，当然 Python 也不例外，下面就让我们来用 Python 输出一句`Hello Word!`吧！

创建一个以 py 结尾的文件

```python
[root@ansheng python_code]# touch hello.py
```

其内容为

```python
#!/usr/vin/env python

print "Hello Word!"
```

用 Python 执行

```bash
[root@ansheng python_code]# python hello.py
Hello Word!
```
输出的内容为`Hello Word!`，OK，你的第一次一句木有了^_^

### 指定 Python 解释器

在 Python 文件的开头加入以下代码就制定了解释器。

第一种方式

```python
#!/usr/bin/python

import sys
print(sys.version)  # 输出Python版本
```
告诉 shell 这个脚本用`/usr/bin/python`执行

第二种方式

```python
#!/usr/bin/env python

import sys
print(sys.version)  # 输出Python版本
```

在操作系统环境不同的情况下指定执行这个脚本用 python 来解释。

### 执行 Python 文件

执行 Python 文件的方式有两种

例如`hello.py`的文件内容为

```python
#!/usr/bin/env python
print "Life is short, you need Pytho"
```

第一种执行方式

```bash
[root@ansheng python_code]# python my.py
Life is short, you need Pytho
```

如果使用`python my.py`这种方式执行，那么`#!/usr/bin/python`会被忽略，等同于注释。

第二种执行方式

```bash
[root@ansheng python_code]# chmod +x my.py
[root@ansheng python_code]# ./my.py
Life is short, you need Pytho
```

如果使用`./my.py`来执行，那么`#!/usr/bin/python`则是指定解释器的路径，在执行之前`my.py`这个文件必须有执行权限。

`python my.py` 实则就是在`my.py`文件顶行加入了`#!/usr/bin/python`

### 指定字符编码

python 制定字符编码的方式有多种，而编码格式是要写在解释器的下面的，常用的如下面三种:

第一种

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_
```

第二种

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
```

第三种

```python
#!/usr/bin/env python
# coding:utf-8
```

## 代码注释

### 单行注释

单行注释只需要在代码前面加上`#`号

```python
# 注释内容
```

### 多行注释

多行注释用三个单引号或者三个双引号躲起来

```python
"""
注释内容
"""
```

### 实例

`py`脚本原文件内容

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

print "My name is Ansheng"
print "I'm a Python developer"
print "My blog URL: https://blog.ansheng.me"
print "Life is short, you need Pytho"
```

源文件输出的内容

```bash
[root@ansheng python_code]# python note.py
My name is Ansheng
I'm a Python developer
My blog URL: https://blog.ansheng.me
Life is short, you need Pytho
```

#### 单行注释演示

代码改为

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

print "My name is Ansheng"
print "I'm a Python developer"
print "My blog URL: https://blog.ansheng.me"
#print "Life is short, you need Pytho"
```

执行结果

```bash
[root@ansheng python_code]# python note.py
My name is Ansheng
I'm a Python developer
My blog URL: https://blog.ansheng.me
```

结果`Life is short, you need Pytho`print 出来

####  多行注释演示

代码改为

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

print "My name is Ansheng"
"""
print "I'm a Python developer"
print "My blog URL: https://blog.ansheng.me"
print "Life is short, you need Pytho"
"""
```

执行结果

```bash
[root@ansheng python_code]# python note.py
My name is Ansheng
```

结果`I'm a Python developer`、`My blog URL: https://blog.ansheng.me`、`Life is short, you need Pytho`都没有 print 出来

### print 输出多行

既然用单个单引号或者多引号可以注释多行，那么能不能 print 多行呢？

代码

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

print """
My name is Ansheng
I'm a Python developer
My blog URL: https://blog.ansheng.me
Life is short, you need Python.
"""
```

执行结果

```bash
[root@ansheng python_code]# python note.py

My name is Ansheng
I'm a Python developer
My blog URL: https://blog.ansheng.me
Life is short, you need Python.

```

显然这是可以得 ^_^

## 变量

变量的命名规则:

1. 变量名只能包含数字、字母、下划线
2. 不能以数字开头
3. 变量名不能使 python 内部的关键字

Python 内部已占用的关键字

```python
['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']
```

在 Python 中变量是如何工作的？

1. 变量在他第一次赋值时创建；
2. 变量在表达式中使用时将被替换它们所定义的值；
3. 变量在表达式中使用时必须已经被赋值，否则会报`name 'xxx' is not defined`;
4. 变量像对象一样不需要在一开始进行声明；

**动态类型模型**

首先让我们抛出一个简单的问题为什么要学习动态类型模型。

如下如语句中我声明了一个变量`age`，值为`21`

```python
>>> age = 21
>>> age
21
>>> type(21)
# 数字类型
<class 'int'>
```

上述代码中我给`age`赋值为`21`，但是并没有指定它的值为`数字`类型，那么 Python 怎么知道他是一个`数字类型`呢？其实，你会发现，Python 在运行的过程中已经决定了这个值是什么类型，而不用通过指定类型的方式。

### 垃圾收集

在 Python 基础中还有一个比较重要的概念就是垃圾回收机制，下面我们通过代码来验证：

```python
>>> a = 1
>>> b = a
>>> id(a),id(b)
(4297546560, 4297546560)
```

上面的实例代码中发生了什么？

首先我们声明了一个变量`a`和变量`b`,`a`等于`1`，`b`等于`a`，其实就是把 b 的值通过指针指向 a 的值，通过`id()`内置函数我们可以清楚地看到这两个变量指向的是同一块内存区域。

再继续下面实例代码

```python
>>> name = 'ansheng'
>>> name = 'as'
>>> name
'as'
```

通过上面这个实例，可以清楚的理解到`垃圾回收机制`是如何工作的：

1. 创建一个变量`name`，值通过指针指向`'ansheng'`的内存地址；
2. 如果`'ansheng'`这个值之前没有在内存中创建，那么现在创建他，并让这个内存地址的引用数+1，此时等于 1；
3. 然后对变量`name`重新赋值，让其指针指向`'as'`的内存地址；
4. 那么此时`'ansheng'`值的引用数现在就变成 0，当 Python 一旦检测到某个内存地址的引用数等于 0 时，就会把这个内存地址给删掉，从而释放内存；
5. 最后 name 值的指针指向了`'as'`的内存地址，所以`name`就等于`'as'`

### 定义变量

```python
>>> name = "ansheng"
>>> print name
ansheng
```

## 基本的数据类型

### 字符串(str)

定义字符串类型是需要用单引号或者双引号包起来的

```python
>>> name = "ansheng"
>>> print(type(name))
<type 'str'>
```

或者

```python
>>> name = 'ansheng'
>>> print(type(name))
<type 'str'>
```

### 数字(int)

整数类型定义的时候变量名后面可以直接跟数字，不要用双引号包起来。

```python
>>> age = 20
>>> print(type(age))
<type 'int'>
```

### 布尔值

布尔值就只有`True(真)`，`Flash(假)`

```python
>>> if True:
...  print("0")
... else:
...  print("1")
...
0
```

**解释：**如果为真则输出 0，否则输出 1

## 流程控制

### if 语句

`if`语句是用来检查一个条件：如果条件为真(true)，我们运行一个语句块（你为 if 块），否则(else)，我们执行另一个语句块（称为 else 块），else 子语句是可选的。

#### 单条件

例题：如果 num 变量大于 1，那么就输出 num 大，否则就输出 num 小，num 值为 5。

代码

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
num = 5

if num > 1:
 print("num大")
else:
 print("num小")
```

结果

```bash
[root@ansheng python_code]# python num.py
num大
```

#### 多条件

例题：如果 num 变量大于 5，那么就输出 num 大于 5，如果 num 变量小于 5，那么就输出 num 小于 5，否则就输出 num 等于 5，num 值为 5。

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
num = 5

if num > 5:
 print("num大于5")
elif num < 5:
 print("num小于5")
else:
 print("num等于5")
```

结果

```bash
[root@ansheng python_code]# python num.py
num等于5
```

### while 循环

while 语句用于循环执行程序，即在某条件下，循环执行某段程序，以处理需要重复处理的相同任务。
执行流程图如下

![while](https://ansheng.me/wp-content/uploads/2016/12/1483015647.png)

实例：

定义一个变量 count，默认值为 1，然后进去 while 循环，让其输出 1-10，如果大于 10 则退出。

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

count = 1

print "Start...."

while count < 11:
 print "The count is:",count
 count += 1

print "End...."
```

执行结果如下

```bash
[root@ansheng python_code]# python while.py
Start....
The count is: 1
The count is: 2
The count is: 3
The count is: 4
The count is: 5
The count is: 6
The count is: 7
The count is: 8
The count is: 9
The count is: 10
End....
```

### break

跳出当前循环体，下面代码不再执行，继续执行循环后面的代码

实例

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

count = 1

print "Start...."

while count < 11:
 if count == 5:   #如果count等于5，那么我就退出当前循环体
  break
 print "The count is:",count
 count += 1

print "End...."
```

输出结果

```bash
[root@ansheng python_code]# python while.py
Start....
The count is: 1
The count is: 2
The count is: 3
The count is: 4
End....
```

### continue

跳出本次循环，继续下一次循环

代码

```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

count = 1

print "Start...."

while count < 11:
 if count == 5:		#如果count等于5，那么我就让其+1，然后不执行下面的代码，继续下一次循环
  count += 1
  continue
 print "The count is:",count
 count += 1

print "End...."
```

输出结果

```代码
[root@ansheng python_code]# python while.py
Start....
The count is: 1
The count is: 2
The count is: 3
The count is: 4
The count is: 6
The count is: 7
The count is: 8
The count is: 9
The count is: 10
End....
```

### 条件判断

条件判断适用于`if`、`while`等。

等于

```python
if 1 == 1:
```

不等于

```python
if 1 != 2:
```

小于

```python
if 1 < 1
```

大于

```python
if 1 > 1:
```

并且

```python
if 1 == 1 and 1 > 0:
```

或者

```python
if 2 > 1 or 2 == 2:
```

永远为真

```python
if True:
```

永远为假

```python
if False:
```

## 交互式输入

Python 的交互式输入使用的是`input()`函数实现的，注意在`Python2.7.x`版本的时候可以使用`raw_input()`和`input()`函数，但是在`Python3.5.x`版本的时候就没有`raw_input()`函数了,只能够使用`input()`

例题：用户在执行脚本的时候，让他输入自己的名字，然后打印出来。

代码
```python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

username = input("请输入你的名字：")
print("你的名字是：", username)
```

执行结果

```bash
[root@ansheng python_code]# python input.py
请输入你的名字：安生   # 输入你的名字
你的名字是： 安生      # 打印出你的名字
```

## 练习题

### 使用 while 循环输入 1 2 3 4 5 6   8 9 10

**`思路：`** 首先定义一个变量 num,值为 1,然后用 while 循环输出 1-10 的内容,在 while 循环内加入 if 语句,判断当前的值如果是 7,那么就让 7+1,加完之后跳出本次循环,不执行下面的 print,7 跳出本次循环之后,第二轮的时候 num 就是 8 了,而不是 7.

代码

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_

num = 1
while num < 11:
    if num == 7:
        num += 1
        continue
    print(num)
    num += 1
```

输出内容为：

```bash
1
2
3
4
5
6
8
9
10
```

### 求 1-100 的所有数的和

**`思路：`**定义两个变量，分别是 count 和 num，利用 while 语句循环输出 1-100，然后每次就让 count+num，这样循环一百次之后相加的结果就是 1 到 100 的和了。

代码

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_

count = 1
num = 0
while count < 101:
    num = num + count
    count += 1

print(num)
```

输出结果

```python
5050
```
### 输出 1-100 内的所有奇数

**`思路：`** 利用`%`整数相除的余，如果余数是 1 那么当前的 count 就是奇数，如果余 0，那么当前的 count 就是偶数。

代码

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_

count = 1

while count < 101:
    num = count % 2
    if num == 1:
        print(count)
    count += 1
```

结果自己执行看

### 输出 1-100 内的所有偶数

代码

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_

count = 1

while count < 101:
    num = count % 2
    if num == 0:
        print(count)
    count += 1
```

结果自己执行看

### 求 1-2+3-4+5 ... 99 的所有数的和

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_

count = 1

while count < 100:
    if count == 1:
        num = count
    elif count % 2 == 1:
        num = num + count
    elif count % 2 == 0:
        num = num - count
    count += 1

print(num)
```

结果

```shell
50
```

### 用户登陆

需求：写一个脚本，用户执行脚本的时候输入用户名和密码，如果用户名或者密码连续三次输入错误则退出，如果输入正确则显示登陆成功，然后退出。

用户名和密码自己定义

- 图解用户登录流程

![python-day01-10](https://ansheng.me/wp-content/uploads/2016/12/1483015715.png)

- 代码

```python
#!/use/bin/env python
# _*_ coding:utf-8 _*_
import getpass

# username：ansheng
# userpass：666666

count = 3

while count > 0:
    username = input("User Name:")
    userpass = getpass.getpass("pass:")
    if username == "ansheng" and userpass == "666666":
        print "User:", username, ",login successful!"
        break
    else:
        count -= 1
        if count != 0:
            print "Login failed", count
        else:
            print("The maximum number of login!")
```

登陆成功演示

```bash
User Name:ansheng  #输入用户名
pass:              #输入密码，密码是看不到的，因为调用了getpass模块
User: ansheng ,login successful!  #显示用户ansheng，登陆成功
```

登陆失败演示

```bash
User Name:as
pass:
Login failed 2
User Name:an
pass:
Login failed 1
User Name:ansea
pass:
The maximum number of login!
```

账号或密码连续三次输入错误则退出程序，并且每次提醒用户升序多少次登陆的机会。
