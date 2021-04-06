---
title: 构造函数和对象初始化
date: 2021-02-20 22:41:40
permalink: /sqlalchemy/core/constructors/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
构造函数和对象初始化[¶](#constructors-and-object-initialization "Permalink to this headline")
=============================================================================================

映射不会对该类的构造函数（`__init__`）方法施加任何限制或要求。您可以自由地为您希望的函数请求任何参数，为 ORM 未知的实例分配属性，并且通常在编写 Python 类的构造函数时执行通常要做的任何其他操作。

当从数据库行重新创建对象时，SQLAlchemy ORM 不会调用`__init__`。ORM 的过程有点类似于 Python 标准库的`pickle`模块，调用低级别的`__new__`方法，然后直接在实例上静静地恢复属性，而不是调用`__init__`

如果您需要在数据库加载的实例准备就绪之前对其进行设置，那么可以使用`@reconstructor`修饰器将方法标记为`__init__`每次加载或重建实例时，SQLAlchemy 都会在没有参数的情况下调用此方法。这对于重新创建通常在`__init__`中分配的瞬态属性非常有用：
```python
    from sqlalchemy import orm

    class MyMappedClass(object):
        def __init__(self, data):
            self.data = data
            # we need stuff on all instances, but not in the database.
            self.stuff = []

        @orm.reconstructor
        def init_on_load(self):
            self.stuff = []
```
在执行`obj = MyMappedClass()`时，Python 将`__init__`
normal 和`data`参数是必需的。当像`query(MyMappedClass).one()`那样在[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")操作期间加载实例时，会调用`init_on_load`。

任何方法都可以标记为[`reconstructor()`](#sqlalchemy.orm.reconstructor "sqlalchemy.orm.reconstructor")，甚至可以标记为`__init__`方法。SQLAlchemy 将调用没有参数的重构器方法。该实例的标量（非集合）数据库映射属性将可用于该函数中。急切加载的集合通常还不可用，通常只包含第一个元素。在此阶段对对象所做的 ORM 状态更改将不会记录下一次 flush()操作，因此重构器中的活动应保守。

[`reconstructor()`](#sqlalchemy.orm.reconstructor "sqlalchemy.orm.reconstructor")是一个更大的“实例级”事件系统的快捷方式，可以使用事件 API 进行订阅
- 请参阅[`InstanceEvents`](events.html#sqlalchemy.orm.events.InstanceEvents "sqlalchemy.orm.events.InstanceEvents")事件。

`sqlalchemy.orm。 T0> 重建 T1> （ T2>  FN  T3> ） T4> ¶ T5 >`{.descclassname}
:   装饰方法作为'重建'钩子。

Designates a method as the “reconstructor”, an `__init__`-like method that will be called by the ORM after the
instance has been loaded from the database or otherwise

重构器将被调用，不带任何参数。该实例的标量（非集合）数据库映射属性将可用于该函数中。急切加载的集合通常还不可用，通常只包含第一个元素。在此阶段对对象所做的ORM状态更改将不会记录下一次flush()操作，因此重构器中的活动应保守。
