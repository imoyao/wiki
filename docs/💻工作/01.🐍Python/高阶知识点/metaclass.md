---
title: Python 中的元类

tags: 
  - Python
  - 元类
  - StackOverflow
  - TODO
categories: 
  - 💻 工作
  - 🐍Python
  - 高阶知识点
date: 2020-09-26 12:27:56
permalink: /pages/ddac56/
---

## 陌生的 metaclass

Python 中的**元类（metaclass）**是一个深度魔法，平时我们可能比较少接触到元类，本文将通过一些简单的例子来理解这个魔法。

## 类也是对象

在 Python 中，一切皆对象。字符串，列表，字典，函数是对象，**类也是一个对象**，因此你可以：

*   把类赋值给一个变量
*   把类作为函数参数进行传递
*   把类作为函数的返回值
*   在运行时动态地创建类

看一个简单的例子：
```plain
    class Foo(object):
        foo = True

    class Bar(object):
        bar = True

    def echo(cls):
        print cls

    def select(name):
        if name == 'foo':
            return Foo        # 返回值是一个类
        if name == 'bar':
            return Bar

    >>> echo(Foo)             # 把类作为参数传递给函数 echo
    <class '__main__.Foo'>
    >>> cls = select('foo')   # 函数 select 的返回值是一个类，把它赋给变量 cls
    >>> cls
    __main__.Foo
```
## 熟悉又陌生的 type
-----------

在日常使用中，我们经常使用 `object` 来派生一个类，事实上，在这种情况下，Python 解释器会调用 `type` 来创建类。

这里，出现了 `type`，没错，是你知道的 `type`，我们经常使用它来判断一个对象的类型，比如：
```plain
    class Foo(object):
        Foo = True

    >>> type(10)
    <type 'int'>
    >>> type('hello')
    <type 'str'>
    >>> type(Foo())
    <class '__main__.Foo'>
    >>> type(Foo)
    <type 'type'>
```
**事实上，`type` 除了可以返回对象的类型，它还可以被用来动态地创建类（对象）**。下面，我们看几个例子，来消化一下这句话。

使用 `type` 来创建类（对象）的方式如下：

> type(类名, 父类的元组（针对继承的情况，可以为空），包含属性和方法的字典（名称和值）)

### 最简单的情况

假设有下面的类：
```plain
    class Foo(object):
        pass
```
现在，我们不使用 `class` 关键字来定义，而使用 `type`，如下：
```plain
    Foo = type('Foo', (object, ), {})    # 使用 type 创建了一个类对象
```
上面两种方式是等价的。我们看到，`type` 接收三个参数：

*   第 1 个参数是字符串 'Foo'，表示类名
*   第 2 个参数是元组 (object, )，表示所有的父类
*   第 3 个参数是字典，这里是一个空字典，表示没有定义属性和方法

在上面，我们使用 `type()` 创建了一个名为 Foo 的类，然后把它赋给了变量 Foo，我们当然可以把它赋给其他变量，但是，此刻没必要给自己找麻烦。

接着，我们看看使用：
```plain
    >>> print Foo
    <class '__main__.Foo'>
    >>> print Foo()
    <__main__.Foo object at 0x10c34f250>
```
### 有属性和方法的情况

假设有下面的类：
```plain
    class Foo(object):
        foo = True
        def greet(self):
            print 'hello world'
            print self.foo
```
用 `type` 来创建这个类，如下：
```plain
    def greet(self):
        print 'hello world'
        print self.foo

    Foo = type('Foo', (object, ), {'foo': True, 'greet': greet})
```
上面两种方式的效果是一样的，看下使用：
```plain
    >>> f = Foo()
    >>> f.foo
    True
    >>> f.greet
    <bound method Foo.greet of <__main__.Foo object at 0x10c34f890>>
    >>> f.greet()
    hello world
    True
```
### 继承的情况

再来看看继承的情况，假设有如下的父类：
```python
    class Base(object):
        pass
```
我们用 Base 派生一个 Foo 类，如下：
```python
    class Foo(Base):
       foo = True
```
改用 `type` 来创建，如下：
```python
    Foo = type('Foo', (Base, ), {'foo': True})
```
## 什么是元类（metaclass）


**元类（metaclass）是用来创建类（对象）的可调用对象。**这里的可调用对象可以是函数或者类等。但一般情况下，我们使用类作为元类。对于实例对象、类和元类，我们可以用下面的图来描述：

类是实例对象的模板，元类是类的模板
    
```plain
    +----------+             +----------+             +----------+
    |          |             |          |             |          |
    |          | instance of |          | instance of |          |
    | instance +------------>+  class   +------------>+ metaclass|
    |          |             |          |             |          |
    |          |             |          |             |          |
    +----------+             +----------+             +----------+

```

我们在前面使用了 `type` 来创建类（对象），事实上，**`type` 就是一个元类**。

那么，元类到底有什么用呢？要你何用...

**元类的主要目的是为了控制类的创建行为。**我们还是先来看看一些例子，以消化这句话。

## 元类的使用


先从一个简单的例子开始，假设有下面的类：
```python
    class Foo(object):
        name = 'foo'
        def bar(self):
            print 'bar'
```
现在我们想给这个类的方法和属性名称前面加上 `my_` 前缀，即 name 变成 my\_name，bar 变成 my\_bar，另外，我们还想加一个 echo 方法。当然，有很多种做法，这里展示用元类的做法。

1.首先，定义一个元类，按照默认习惯，类名以 Metaclass 结尾，代码如下：
```python
    class PrefixMetaclass(type):
        def __new__(cls, name, bases, attrs):
            # 给所有属性和方法前面加上前缀 my_
            _attrs = (('my_' + name, value) for name, value in attrs.items())

            _attrs = dict((name, value) for name, value in _attrs)  # 转化为字典
            _attrs['echo'] = lambda self, phrase: phrase  # 增加了一个 echo 方法

            return type.__new__(cls, name, bases, _attrs)  # 返回创建后的类
```
上面的代码有几个需要注意的点：

*   PrefixMetaClass 从 `type` 继承，这是因为 PrefixMetaclass 是用来创建类的
*   `__new__` 是在 `__init__` 之前被调用的特殊方法，它用来创建对象并返回创建后的对象，对它的参数解释如下：
    *   cls：当前准备创建的类
    *   name：类的名字
    *   bases：类的父类集合
    *   attrs：类的属性和方法，是一个字典

2.接着，我们需要指示 Foo 使用 PrefixMetaclass 来定制类。

在 Python2 中，我们只需在 Foo 中加一个 `__metaclass__` 的属性，如下：
```python
    class Foo(object):
        __metaclass__ = PrefixMetaclass
        name = 'foo'
        def bar(self):
            print 'bar'
```
在 Python3 中，这样做：
```python
    class Foo(metaclass=PrefixMetaclass):
        name = 'foo'
        def bar(self):
            print('bar')
```
现在，让我们看看使用：
```plain
    >>> f = Foo()
    >>> f.name    # name 属性已经被改变
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-774-4511c8475833> in <module>()
    ----> 1 f.name

    AttributeError: 'Foo' object has no attribute 'name'
    >>>
    >>> f.my_name
    'foo'
    >>> f.my_bar()
    bar
    >>> f.echo('hello')
    'hello'
```
可以看到，Foo 原来的属性 name 已经变成了 my\_name，而方法 bar 也变成了 my\_bar，这就是元类的魔法。

再来看一个继承的例子，下面是完整的代码：
```python
    class PrefixMetaclass(type):
        def __new__(cls, name, bases, attrs):
            # 给所有属性和方法前面加上前缀 my_
            _attrs = (('my_' + name, value) for name, value in attrs.items())

            _attrs = dict((name, value) for name, value in _attrs)  # 转化为字典
            _attrs['echo'] = lambda self, phrase: phrase  # 增加了一个 echo 方法

            return type.__new__(cls, name, bases, _attrs)

    class Foo(object):
        __metaclass__ = PrefixMetaclass   # 注意跟 Python3 的写法有所区别
        name = 'foo'
        def bar(self):
            print 'bar'

    class Bar(Foo):
        prop = 'bar'
```
其中，PrefixMetaclass 和 Foo 跟前面的定义是一样的，只是新增了 Bar，它继承自 Foo。先让我们看看使用：
```plain
    >>> b = Bar()
    >>> b.prop     # 发现没这个属性
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-778-825e0b6563ea> in <module>()
    ----> 1 b.prop

    AttributeError: 'Bar' object has no attribute 'prop'
    >>> b.my_prop
    'bar'
    >>> b.my_name
    'foo'
    >>> b.my_bar()
    bar
    >>> b.echo('hello')
    'hello'
```
我们发现，Bar 没有 prop 这个属性，但是有 my\_prop 这个属性，这是为什么呢？

原来，当我们定义 `class Bar(Foo)` 时，Python 会首先在当前类，即 Bar 中寻找 `__metaclass__`，如果没有找到，就会在父类 Foo 中寻找 `__metaclass__`，如果找不到，就继续在 Foo 的父类寻找，如此继续下去，如果在任何父类都找不到 `__metaclass__`，就会到模块层次中寻找，如果还是找不到，就会用 type 来创建这个类。

这里，我们在 Foo 找到了 `__metaclass__`，Python 会使用 PrefixMetaclass 来创建 Bar，也就是说，元类会隐式地继承到子类，虽然没有显示地在子类使用 `__metaclass__`，这也解释了为什么 Bar 的 prop 属性被动态修改成了 my\_prop。

写到这里，不知道你理解元类了没？希望理解了，如果没理解，就多看几遍吧~

## 小结

*   在 Python 中，类也是一个对象。
*   类创建实例，元类创建类。
*   元类主要做了三件事：
    *   拦截类的创建
    *   修改类的定义
    *   返回修改后的类
*   当你创建类时，解释器会调用元类来生成它，定义一个继承自 object 的普通类意味着调用 type 来创建它。

## 参考资料

*   [oop - What are metaclasses in Python? - StackOverflow](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)
    上文翻译：[[翻译 stackoverflow]What are metaclasses in Python? - leetao94 的个人空间 - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/leetao944/blog/4440694)
*   [深刻理解 Python 中的元类(metaclass) - 伯乐在线](http://blog.jobbole.com/21351/)
*   [使用元类 - 廖雪峰的官方网站](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319106919344c4ef8b1e04c48778bb45796e0335839000)
*   [Python 基础：元类](http://www.cnblogs.com/russellluo/p/3409602.html)
*   [在 Python 中使用 class decorator 和 metaclass](http://blog.zhangyu.so/python/2016/02/19/class-decorator-and-metaclass-in-python/)
### 待整理
- [陌生的 metaclass - Python 之旅 - 极客学院 Wiki](https://wiki.jikexueyuan.com/project/explore-python/Class/metaclass.html)
- [Python 元类 (MetaClass) 小教程 | 三点水](https://lotabout.me/2018/Understanding-Python-MetaClass/)
- [一文带你完全理解 Python 中的 metaclass - 简书](https://www.jianshu.com/p/224ffcb8e73e)