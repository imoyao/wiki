---
title: Python 全栈之路系列之面向对象进阶及类成员

tags: 
  - 编码
top: 2
categories: 
  - 💻 工作
  - 🐍Python
  - 全栈之路
  - 3-面向对象
date: 2020-05-23 18:21:46
permalink: /pages/15f60c/
---

## 再次了解多继承

先来一段代码

```Python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

class A:
    def bar(self):
        print("BAR")
        self.f1()

class B(A):
    def f1(self):
        print("B")

class C:
    def f1(self):
        print("C")

class D(C, B):
    pass

obj = D()
obj.bar()
```

---

执行结果
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day03/s1.py
BAR
C

Process finished with exit code 0
```
**流程释意：**
1. 创建了类 A、B、C、D；
2. `D`继承了`C`和`B`，`B`继承了`A`，`D`内什么都不做，`pass`；
3. 创建一个对象`obj`，类是`D`，当执行`D`的`bar`方法的时候会先从`C`里面寻找有没有`bar`方法；
4. `C`内没有`bar`方法，然后继续从`B`里面查找，`B`里面也没有，`B`的父类是`A`，`A`里面有`bar`方法，所以就执行了`A`的`bar`方法；
5. `A`的`bar`方法首先输出了`BAR`；
6. 然后又执行了`self.f1()`，`self`=`obj`，相当于执行了`obj.f1()`；
7. 执行`obj.f1()`的时候先从`C`里面查找有没有`f1`这个方法，`C`里面又`f1`这个方法；
8. 最后就执行`C`里面的`f1`方法了，输出了`C`

## 执行父类的构造方法
```Python
class Annimal(object):
    def __init__(self):
        print("Annimal的构造方法")
        self.ty = "动物"

class Cat(Annimal):
    def __init__(self):
        print("Cat的构造方法")
        self.n = "猫"
        # 寻找Cat类的父类，然后执行父类的构造方法
        super(Cat, self).__init__()
mao = Cat()
print(mao.__dict__)
```
执行结果
```python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day03/s1.py
Cat的构造方法
Annimal的构造方法
{'ty': '动物', 'n': '猫'}

Process finished with exit code 0
```
先执行了 Cat 的构造方法，然后又执行了 Annimal 的构造方法。
第二种执行父类的方法如下:

```Python
Annimal.__init__(self)
```
不推荐使用

## 利用反射查看面向对象成员归属

```Python
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

class Foo:
    def __init__(self, name):
        self.name = name

    def show(self):
        print('show')


obj = Foo("as")

# 如果是类，就只能找到类里的成员
print(hasattr(Foo, "show"))

# 如果是对象，既可以找到对象，也可以找类里的成员
print(hasattr(obj, "name"))
print(hasattr(obj, "show"))
```
执行结果
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day03/s2.py
True
True
True

Process finished with exit code 0
```
## 利用反射导入模块、查找类、创建对象、查找对象中的字段

`s1`脚本文件内容:
```Python
#!/usr/bin/env python
# _*_coding:utf-8 _*_

# 导入模块
m = __import__('s2', fromlist=True)

# 去模块中找类
class_name = getattr(m, "Foo")

# 根据类创建对象
obj = class_name("ansheng")

# 去对象中找name对应的值
print(getattr(obj, 'name'))
```
`s2`脚本文件内容
```Python
#!/usr/bin/env python
# _*_coding:utf-8 _*_

class Foo:
    def __init__(self, name):
        # 普通字段，保存在对象中
        self.name = name

```
执行结果:
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day04/s1.py
ansheng

Process finished with exit code 0

```
## 面向对象类成员之静态字段

静态字段存在类中，如下：

```Python
#!/usr/bin/env python
# _*_coding:utf-8 _*_

# 静态字段存在的意义就是将每个对象中重复的东西在类里面保存一份即可，这就是静态字段

class Provice:

    # 静态字段
    contry = "China"

    def __init__(self, name):
        self.name = name

    def show(self):
        print(Provice.contry, self.name)

hebei = Provice("河北")
hebei.show()

hubei = Provice("湖北")
hubei.show()
```
执行结果
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day04/s2.py
China 河北
China 湖北

Process finished with exit code 0
```
类里面的成员类去访问，对象内的成员用对象去访问。

## 面向对象类成员之静态方法

```Python
#!/usr/bin/env python
# _*_coding:utf-8 _*_

class Foo:

    # 静态方法括号内没有self，切方法前一行要加上@staticmethod
    @staticmethod
    def static():
    # def static(arg1, arg2): # 也可以设置参数
        print("static")

# 静态方法通过类名+方法名既可执行
Foo.static()
# Foo.static("arg1", "arg2") 通过类调用的时候传入对于的参数即可

# 静态方法也可以通过对象去访问，对于静态方法用类去访问
obj = Foo()
obj.static()
```
执行结果
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day04/s2.py
static
static

Process finished with exit code 0
```
## 面向对象类成员之类方法
```Python
#!/usr/bin/env python
# _*_coding:utf-8 _*_

class Foo:

    # 创建类方法的时候需要在方法前面加上@classmethod
    @classmethod
    def ClassMethod(cls): # 并且方法的括号内必须带有cls关键字，类方法的参数是当前类的类名
        print("类方法")

# 调用类方法
Foo.ClassMethod()
```
执行结果:
```Python
/usr/bin/python3.5 /home/ansheng/文档/Python_code/sublime/Week06/Day04/s2.py
类方法

Process finished with exit code 0
```

## 面向对象类成员内容梳理

字段

1.静态字段(每个对象都有一份)
2.普通字段(每个对象都不同的数据)

方法

1.静态方法(无需使用对象封装的内容)
2.类方法
3.普通方法(适用对象中的数据)

特性

1.普通特性(将方法未造成字段)

快速判断，类执行、对象执行：

1.self  -->  对象调用
2.无 self --> 类调用
