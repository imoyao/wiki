---
title: 突变跟踪
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/extensions/mutable/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
突变跟踪[¶](#module-sqlalchemy.ext.mutable "Permalink to this headline")
========================================================================

提供对跟踪对标量值进行就地更改的支持，这些标量值将在拥有父对象时传播到 ORM 更改事件中。

New in version 0.7: [`sqlalchemy.ext.mutable`](#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")
replaces SQLAlchemy’s legacy approach to in-place mutations of scalar
values; see [Mutation event extension, supersedes
“mutable=True”](changelog_migration_07.html#migration-mutation-extension).

建立标量列值的可变性[¶](#establishing-mutability-on-scalar-column-values "Permalink to this headline")
------------------------------------------------------------------------------------------------------

一个“可变”结构的典型例子是 Python 字典。在[Column and Data
Types](core_types.html)中介绍的示例之后，我们从一个自定义类型开始，它将 Python 字典在持久化之前编组为 JSON 字符串：

    from sqlalchemy.types import TypeDecorator, VARCHARplain
    import json

    class JSONEncodedDict(TypeDecorator):
        "Represents an immutable structure as a json-encoded string."

        impl = VARCHAR

        def process_bind_param(self, value, dialect):
            if value is not None:
                value = json.dumps(value)
            return value

        def process_result_value(self, value, dialect):
            if value is not None:
                value = json.loads(value)
            return value

`json`的用法仅用于示例。[`sqlalchemy.ext.mutable`](#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展名可用于目标 Python 类型可变的任何类型，包括[`PickleType`](core_type_basics.html#sqlalchemy.types.PickleType "sqlalchemy.types.PickleType")，[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")等。

当使用[`sqlalchemy.ext.mutable`](#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展名时，该值本身会跟踪引用它的所有父项。下面，我们演示一下[`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")字典对象的简单版本，它将[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")
mixin 应用于普通的 Python 字典：

    from sqlalchemy.ext.mutable import Mutableplain

    class MutableDict(Mutable, dict):
        @classmethod
        def coerce(cls, key, value):
            "Convert plain dictionaries to MutableDict."

            if not isinstance(value, MutableDict):
                if isinstance(value, dict):
                    return MutableDict(value)

                # this call will raise ValueError
                return Mutable.coerce(key, value)
            else:
                return value

        def __setitem__(self, key, value):
            "Detect dictionary set events and emit change events."

            dict.__setitem__(self, key, value)
            self.changed()

        def __delitem__(self, key):
            "Detect dictionary del events and emit change events."

            dict.__delitem__(self, key)
            self.changed()

上面的字典类采用子类化 Python 内置的`dict`的方法来生成一个 dict 子类，该子类通过`__setitem__`发送所有的突变事件。There are variants on this approach, such
as subclassing `UserDict.UserDict` or
`collections.MutableMapping`; the part that’s
important to this example is that the [`Mutable.changed()`](#sqlalchemy.ext.mutable.Mutable.changed "sqlalchemy.ext.mutable.Mutable.changed")
method is called whenever an in-place change to the datastructure takes
place.

我们还重新定义了将用于转换任何非`MutableDict`实例的值的[`Mutable.coerce()`](#sqlalchemy.ext.mutable.Mutable.coerce "sqlalchemy.ext.mutable.Mutable.coerce")方法，例如由`json`模块，转换为适当的类型。定义此方法是可选的；我们也可以创建我们的`JSONEncodedDict`，以便它始终返回`MutableDict`的一个实例，并且确保所有调用代码明确使用`MutableDict`。当[`Mutable.coerce()`](#sqlalchemy.ext.mutable.Mutable.coerce "sqlalchemy.ext.mutable.Mutable.coerce")未被覆盖时，应用于不是可变类型实例的父对象的任何值将引发`ValueError`。

我们新的`MutableDict`类型提供了一个类方法[`as_mutable()`](#sqlalchemy.ext.mutable.Mutable.as_mutable "sqlalchemy.ext.mutable.Mutable.as_mutable")，我们可以在列元数据中使用它来与类型关联。此方法捕获给定类型的对象或类，并关联侦听器，该侦听器将检测此类型的所有未来映射，并将事件侦听工具应用于映射的属性。比如，用经典的表格元数据：

    from sqlalchemy import Table, Column, Integer

    my_data = Table('my_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', MutableDict.as_mutable(JSONEncodedDict))
    )

在上面，[`as_mutable()`](#sqlalchemy.ext.mutable.Mutable.as_mutable "sqlalchemy.ext.mutable.Mutable.as_mutable")返回`JSONEncodedDict`的实例（如果类型对象不是已经存在的实例），它将拦截所有映射此类型的属性。下面我们根据`my_data`表建立一个简单映射：

    from sqlalchemy import mapper

    class MyDataClass(object):
        pass

    # associates mutation listeners with MyDataClass.data
    mapper(MyDataClass, my_data)

现在将通知`MyDataClass.data`成员更改其值。

使用声明时，使用方式没有区别：

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class MyDataClass(Base):
        __tablename__ = 'my_data'
        id = Column(Integer, primary_key=True)
        data = Column(MutableDict.as_mutable(JSONEncodedDict))

对`MyDataClass.data`成员进行任何就地更改都会将该属性标记为父对象上的“脏”：

    >>> from sqlalchemy.orm import Sessionplainplain

    >>> sess = Session()
    >>> m1 = MyDataClass(data={'value1':'foo'})
    >>> sess.add(m1)
    >>> sess.commit()

    >>> m1.data['value1'] = 'bar'
    >>> assert m1 in sess.dirty
    True

使用[`associate_with()`](#sqlalchemy.ext.mutable.Mutable.associate_with "sqlalchemy.ext.mutable.Mutable.associate_with")，`MutableDict`可以与`JSONEncodedDict`的所有未来实例关联。这与[`as_mutable()`](#sqlalchemy.ext.mutable.Mutable.as_mutable "sqlalchemy.ext.mutable.Mutable.as_mutable")类似，只是它将无条件地截取所有映射中所有出现的`MutableDict`，而不需要单独声明它：

    MutableDict.associate_with(JSONEncodedDict)

    class MyDataClass(Base):
        __tablename__ = 'my_data'
        id = Column(Integer, primary_key=True)
        data = Column(JSONEncodedDict)

### 支持酸洗[¶](#supporting-pickling "Permalink to this headline")

[`sqlalchemy.ext.mutable`](#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展的关键依赖于`weakref.WeakKeyDictionary`在值对象上的位置，该对象存储了键入该属性的父映射对象的映射名称，它们与此值关联。`WeakKeyDictionary` objects are not picklable, due to the fact that they contain
weakrefs and function callbacks.
在我们的例子中，这是一件好事，因为如果这个字典是可挑选的，它可能会导致我们的值对象的 pickle 大小过大，而这些对象是在父级上下文之外自行挑选的。这里的开发人员责任只是提供一个从 pickle 流中排除[`_parents()`](#sqlalchemy.ext.mutable.MutableBase._parents "sqlalchemy.ext.mutable.MutableBase._parents")集合的`__getstate__`方法：

    class MyMutableType(Mutable):
        def __getstate__(self):
            d = self.__dict__.copy()
            d.pop('_parents', None)
            return d

用我们的字典例子，我们需要返回字典本身的内容（并且还在\_\_
setstate\_\_上恢复它们​​）：

    class MutableDict(Mutable, dict):
        # ....

        def __getstate__(self):
            return dict(self)

        def __setstate__(self, state):
            self.update(state)

如果可变值对象被粘贴到一个或多个也是pickle一部分的父对象上，那么[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")
mixin 将重新建立[`Mutable._parents`](#sqlalchemy.ext.mutable.Mutable._parents "sqlalchemy.ext.mutable.Mutable._parents")

在复合材料上建立可变性[¶](#establishing-mutability-on-composites "Permalink to this headline")
----------------------------------------------------------------------------------------------

组合是一种特殊的 ORM 特性，它允许为单个标量属性分配一个对象值，该值表示来自底层映射表中一个或多个列的“合成”信息。通常的例子是几何“点”，并在[Composite
Column Types](composites.html#mapper-composite)中介绍。

在版本 0.7 中更改： [`orm.composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")的内部已大大简化，默认情况下不再启用就地突变检测；相反，用户定义的值必须自行检测更改并将其传播给所有拥有的父项。[`sqlalchemy.ext.mutable`](#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展提供了helper类[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")，它是[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")类中的轻微变体。

与[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")一样，用户定义的组合类将[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")作为一个 mixin 的子类，并通过[`MutableComposite.changed()`](#sqlalchemy.ext.mutable.MutableComposite.changed "sqlalchemy.ext.mutable.MutableComposite.changed")方法。对于复合类，通常通过使用 Python 描述符（即`@property`）或者通过特殊的 Python 方法`__setattr__()`来进行检测。Below we expand upon the `Point` class introduced in [Composite Column
Types](composites.html#mapper-composite) to subclass
[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
and to also route attribute set events via `__setattr__` to the [`MutableComposite.changed()`](#sqlalchemy.ext.mutable.MutableComposite.changed "sqlalchemy.ext.mutable.MutableComposite.changed")
method:

    from sqlalchemy.ext.mutable import MutableComposite

    class Point(MutableComposite):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __setattr__(self, key, value):
            "Intercept set events"

            # set the attribute
            object.__setattr__(self, key, value)

            # alert all parents to the change
            self.changed()

        def __composite_values__(self):
            return self.x, self.y

        def __eq__(self, other):
            return isinstance(other, Point) and \
                other.x == self.x and \
                other.y == self.y

        def __ne__(self, other):
            return not self.__eq__(other)

The [`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
class uses a Python metaclass to automatically establish listeners for
any usage of [`orm.composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
that specifies our `Point` type.
下面，当`Point`映​​射到`Vertex`类时，将建立侦听器，它将将`Point`对象的变化事件路由到`Vertex.start`和`Vertex.end`属性：

    from sqlalchemy.orm import composite, mapper
    from sqlalchemy import Table, Column

    vertices = Table('vertices', metadata,
        Column('id', Integer, primary_key=True),
        Column('x1', Integer),
        Column('y1', Integer),
        Column('x2', Integer),
        Column('y2', Integer),
        )

    class Vertex(object):
        pass

    mapper(Vertex, vertices, properties={
        'start': composite(Point, vertices.c.x1, vertices.c.y1),
        'end': composite(Point, vertices.c.x2, vertices.c.y2)
    })

对`Vertex.start`或`Vertex.end`成员进行任何就地更改都会将该属性标记为父对象上的“脏”：

    >>> from sqlalchemy.orm import Sessionplain

    >>> sess = Session()
    >>> v1 = Vertex(start=Point(3, 4), end=Point(12, 15))
    >>> sess.add(v1)
    >>> sess.commit()

    >>> v1.end.x = 8
    >>> assert v1 in sess.dirty
    True

### 胁迫可变复合材料[¶](#coercing-mutable-composites "Permalink to this headline")

复合类型也支持[`MutableBase.coerce()`](#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")方法。在[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")的情况下，仅针对属性集操作调用[`MutableBase.coerce()`](#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")方法，而不是调用操作。Overriding
the [`MutableBase.coerce()`](#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")
method is essentially equivalent to using a [`validates()`](mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")
validation routine for all attributes which make use of the custom
composite type:

    class Point(MutableComposite):
        # other Point methods
        # ...

        def coerce(cls, key, value):
            if isinstance(value, tuple):
                value = Point(*value)
            elif not isinstance(value, Point):
                raise ValueError("tuple or Point expected")
            return value

New in version 0.7.10,0.8.0b2: Support for the
[`MutableBase.coerce()`](#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")
method in conjunction with objects of type [`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite").

### 支持酸洗[¶](#id1 "Permalink to this headline")

As is the case with [`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable"),
the [`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
helper class uses a `weakref.WeakKeyDictionary`
available via the [`MutableBase._parents()`](#sqlalchemy.ext.mutable.MutableBase._parents "sqlalchemy.ext.mutable.MutableBase._parents")
attribute which isn’t picklable. If we need to pickle instances of
`Point` or its owning class `Vertex`, we at least need to define a `__getstate__` that doesn’t include the `_parents`
dictionary. 下面我们定义一个`__getstate__`和一个`__setstate__`，它们包装了我们的`Point`类的最小形式：

    class Point(MutableComposite):
        # ...

        def __getstate__(self):
            return self.x, self.y

        def __setstate__(self, state):
            self.x, self.y = state

与[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")一样，[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")增加了父对象关系状态的酸洗过程，以使[`MutableBase._parents()`](#sqlalchemy.ext.mutable.MutableBase._parents "sqlalchemy.ext.mutable.MutableBase._parents")集合恢复为所有`Point`对象。

API参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

*class* `sqlalchemy.ext.mutable。`{.descclassname} `MutableBase`{.descname} [¶](#sqlalchemy.ext.mutable.MutableBase "Permalink to this definition")
:   通用基类为[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")和[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")。

    ` _parents  T0> ¶ T1>`{.descname}
    :   父对象上的字典 - \>属性名称。

        这个属性是一个所谓的“memoized”属性。它在第一次访问时使用新的`weakref.WeakKeyDictionary`进行初始化，并在后续访问时返回相同的对象。

     *classmethod*`coerce`{.descname}(*key*, *value*)[¶](#sqlalchemy.ext.mutable.MutableBase.coerce "Permalink to this definition")
    :   给定一个值，将其强制转换为目标类型。

        可以被自定义子类覆盖以将输入数据强制转换为特定类型。

        默认情况下，引发`ValueError`。

        根据父类是[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")类型还是[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")类型，在不同场景中调用此方法。在前者的情况下，它既被称为属性集操作，也被称为ORM加载操作。对于后者，它只在属性集操作期间被调用；
        [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")构造的机制在加载操作期间处理强制。

        参数：

        -   **key**[¶](#sqlalchemy.ext.mutable.MutableBase.coerce.params.key)
            – string name of the ORM-mapped attribute being set.
        -   **值**
            [¶](#sqlalchemy.ext.mutable.MutableBase.coerce.params.value)
            - 传入值。

        返回：

        该方法应该返回强制值，或者如果强制无法完成，则会引发`ValueError`。

*class* `sqlalchemy.ext.mutable。`{.descclassname} `Mutable`{.descname} [¶](#sqlalchemy.ext.mutable.Mutable "Permalink to this definition")
:   基础：[`sqlalchemy.ext.mutable.MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

    Mixin定义变化事件向父对象的透明传播。plainplain

    有关使用信息，请参阅[Establishing Mutability on Scalar Column
    Values](#mutable-scalars)中的示例。

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

    ` _get_listen_keys  T0> （ T1> 属性 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* `_get_listen_keys()` *method of* [`MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

        给定描述符属性，返回属性键的`set()`，它表示此属性状态的变化。

        这通常只是`set([attribute.key])`，但可以被覆盖以提供额外的键。例如。一个[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")使用与组成复合值的列相关联的属性键来扩充该集合。

        在拦截[`InstanceEvents.refresh()`](events.html#sqlalchemy.orm.events.InstanceEvents.refresh "sqlalchemy.orm.events.InstanceEvents.refresh")和[`InstanceEvents.refresh_flush()`](events.html#sqlalchemy.orm.events.InstanceEvents.refresh_flush "sqlalchemy.orm.events.InstanceEvents.refresh_flush")事件的情况下，会查看此集合，这些事件传递已刷新的属性名称列表；该列表与该组进行比较以确定是否需要采取行动。

        版本1.0.5中的新功能

     `_listen_on_attribute`{.descname}(*attribute*, *coerce*, *parent\_cls*)[¶](#sqlalchemy.ext.mutable.Mutable._listen_on_attribute "Permalink to this definition")
    :   *inherited from the* `_listen_on_attribute()` *method of* [`MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

        将此类型建立为给定映射描述符的变种侦听器。

    ` _parents  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`_parents`](#sqlalchemy.ext.mutable.MutableBase._parents "sqlalchemy.ext.mutable.MutableBase._parents")
        *attribute of* [`MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

        父对象上的字典 - \>属性名称。

        这个属性是一个所谓的“memoized”属性。它在第一次访问时使用新的`weakref.WeakKeyDictionary`进行初始化，并在后续访问时返回相同的对象。

     *classmethod*`as_mutable`{.descname}(*sqltype*)[¶](#sqlalchemy.ext.mutable.Mutable.as_mutable "Permalink to this definition")
    :   将SQL类型与此可变的Python类型关联。

        这建立了侦听器，它将检测针对给定类型的ORM映射，并向这些映射添加突变事件跟踪器。

        该类型作为一个实例无条件返回，因此[`as_mutable()`](#sqlalchemy.ext.mutable.Mutable.as_mutable "sqlalchemy.ext.mutable.Mutable.as_mutable")可以内联使用：

            Table('mytable', metadata,
                Column('id', Integer, primary_key=True),
                Column('data', MyMutableType.as_mutable(PickleType))
            )

        请注意，返回的类型始终是一个实例，即使给出了一个类，并且只有与该类型实例专门声明的列才会接收其他检测。

        要将特定的可变类型与特定类型的所有匹配关联起来，请使用特定[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")子类的[`Mutable.associate_with()`](#sqlalchemy.ext.mutable.Mutable.associate_with "sqlalchemy.ext.mutable.Mutable.associate_with")类方法建立全局关联。

        警告

        由此方法建立的监听器对所有映射器都是*全局*，并且*不是*垃圾收集。对于应用程序永久性的类型，只能使用[`as_mutable()`](#sqlalchemy.ext.mutable.Mutable.as_mutable "sqlalchemy.ext.mutable.Mutable.as_mutable")，否则会导致内存使用率无限增长。

     *classmethod*`associate_with`{.descname}(*sqltype*)[¶](#sqlalchemy.ext.mutable.Mutable.associate_with "Permalink to this definition")
    :   将此包装与给定类型的所有未来映射列相关联。

        这是一种自动调用`associate_with_attribute`的便捷方法。

        警告

        由此方法建立的监听器对所有映射器都是*全局*，并且*不是*垃圾收集。对于应用程序永久性的类型，只能使用[`associate_with()`](#sqlalchemy.ext.mutable.Mutable.associate_with "sqlalchemy.ext.mutable.Mutable.associate_with")，而不要使用ad-hoc类型，否则这会导致内存使用率无限增长。

     *classmethod*`associate_with_attribute`{.descname}(*attribute*)[¶](#sqlalchemy.ext.mutable.Mutable.associate_with_attribute "Permalink to this definition")
    :   将此类型建立为给定映射描述符的变种侦听器。

    `改变 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   无论何时发生更改事件，子类都应调用此方法。

     `coerce`{.descname}(*key*, *value*)[¶](#sqlalchemy.ext.mutable.Mutable.coerce "Permalink to this definition")
    :   *inherited from the* [`coerce()`](#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")
        *method of* [`MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

        给定一个值，将其强制转换为目标类型。

        可以被自定义子类覆盖以将输入数据强制转换为特定类型。

        默认情况下，引发`ValueError`。

        根据父类是[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")类型还是[`MutableComposite`](#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")类型，在不同场景中调用此方法。在前者的情况下，它既被称为属性集操作，也被称为ORM加载操作。对于后者，它只在属性集操作期间被调用；
        [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")构造的机制在加载操作期间处理强制。

        参数：

        -   **key**[¶](#sqlalchemy.ext.mutable.Mutable.coerce.params.key)
            – string name of the ORM-mapped attribute being set.
        -   **值**
            [¶](#sqlalchemy.ext.mutable.Mutable.coerce.params.value) -
            传入值。

        返回：

        该方法应该返回强制值，或者如果强制无法完成，则会引发`ValueError`。

*class* `sqlalchemy.ext.mutable。`{.descclassname} `MutableComposite`{.descname} [¶](#sqlalchemy.ext.mutable.MutableComposite "Permalink to this definition")
:   基础：[`sqlalchemy.ext.mutable.MutableBase`](#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")

    Mixin，定义SQLAlchemy“复合”对象上的变化事件的透明传播给其拥有的父对象或父对象。plain

    有关使用信息，请参阅[Establishing Mutability on
    Composites](#mutable-composites)中的示例。

    `改变 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   无论何时发生更改事件，子类都应调用此方法。

*class* `sqlalchemy.ext.mutable。`{.descclassname} `MutableDict`{.descname} [¶](#sqlalchemy.ext.mutable.MutableDict "Permalink to this definition")
:   基础：[`sqlalchemy.ext.mutable.Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")，`__builtin__.dict`

    实现[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")的字典类型。

    [`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")对象实现了一个字典，该字典在字典内容发生更改时（包括添加或删除值时）会将更改事件发送到基础映射。

    Note that [`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    does **not** apply mutable tracking to the *values themselves*
    inside the dictionary.
    因此，对于追踪*递归*字典结构（如JSON结构）的深层变化的用例来说，这不是一个充分的解决方案。为了支持这个用例，构建一个[`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")的子类，它为放置在字典中的值提供适当的转换，使它们也是“可变的”，并将事件发送到其父结构。

    0.8版本中的新功能

    也可以看看

    [`MutableList`](#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")

    [`MutableSet`](#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")

    `明确 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

     *classmethod*`coerce`{.descname}(*key*, *value*)[¶](#sqlalchemy.ext.mutable.MutableDict.coerce "Permalink to this definition")
    :   将普通字典转换为此类的实例。

    `弹出 T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    ` popitem  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

    `setdefault`{.descname} （ *key*，*value* ） [](#sqlalchemy.ext.mutable.MutableDict.setdefault "Permalink to this definition")
    :   

    `更新`{.descname} （ *\* a*，*\*\* kw* ） [T5\>](#sqlalchemy.ext.mutable.MutableDict.update "Permalink to this definition")
    :   

*class* `sqlalchemy.ext.mutable。`{.descclassname} `MutableList`{.descname} [¶](#sqlalchemy.ext.mutable.MutableList "Permalink to this definition")
:   基础：[`sqlalchemy.ext.mutable.Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")，`__builtin__.list`

    实现[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")的列表类型。plain

    [`MutableList`](#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")对象实现了一个列表，当列表内容发生更改时（包括添加或删除值时），这些列表将发出更改事件到底层映射。

    Note that [`MutableList`](#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")
    does **not** apply mutable tracking to the *values themselves*
    inside the list.
    因此，对于追踪*递归*可变结构（如JSON结构）的深层变化的用例来说，这不是一个充分的解决方案。为了支持这个用例，建立一个[`MutableList`](#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")的子类，为放置在字典中的值提供适当的转换，以便它们也是“可变的”，并将事件发送到其父结构。

    版本1.1中的新功能

    也可以看看

    [`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")

    [`MutableSet`](#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")

    `追加 T0> （ T1>  X  T2> ） T3> ¶ T4>`{.descname}
    :   

    `明确 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

     *classmethod*`coerce`{.descname}(*index*, *value*)[¶](#sqlalchemy.ext.mutable.MutableList.coerce "Permalink to this definition")
    :   将普通列表转换为此类的实例。

    `延伸 T0> （ T1>  X  T2> ） T3> ¶ T4>`{.descname}
    :   

    `插入`{.descname} （ *i*，*x* ） [](#sqlalchemy.ext.mutable.MutableList.insert "Permalink to this definition")
    :   

    `弹出 T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    `除去 T0> （ T1>  I  T2> ） T3> ¶ T4>`{.descname}
    :   

    `逆转 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

    `排序 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

*class* `sqlalchemy.ext.mutable。`{.descclassname} `MutableSet`{.descname} [¶](#sqlalchemy.ext.mutable.MutableSet "Permalink to this definition")
:   基础：[`sqlalchemy.ext.mutable.Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")，`__builtin__.set`

    实现[`Mutable`](#sqlalchemy.ext.mutable.Mutable "sqlalchemy.ext.mutable.Mutable")的集合类型。

    [`MutableSet`](#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")对象实现了一个集合，当集合的内容发生更改时（包括添加或删除值时），该集合将发生更改事件到底层映射。

    Note that [`MutableSet`](#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")
    does **not** apply mutable tracking to the *values themselves*
    inside the set.
    因此，它不能用于追踪*递归*可变结构的深层变化的用例。为了支持这个用例，建立一个[`MutableSet`](#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")的子类，为放置在字典中的值提供适当的转换，使它们也是“可变的”，并将事件发送到它们的父结构。

    版本1.1中的新功能

    也可以看看

    [`MutableDict`](#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")

    [`MutableList`](#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")

    `添加 T0> （ T1>  ELEM  T2> ） T3> ¶ T4>`{.descname}
    :   

    `明确 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   

     *classmethod*`coerce`{.descname}(*index*, *value*)[¶](#sqlalchemy.ext.mutable.MutableSet.coerce "Permalink to this definition")
    :   将普通集转换为此类的实例。

    ` difference_update  T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    `丢弃 T0> （ T1>  ELEM  T2> ） T3> ¶ T4>`{.descname}
    :   

    ` intersection_update  T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    `弹出 T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    `除去 T0> （ T1>  ELEM  T2> ） T3> ¶ T4>`{.descname}
    :   

    ` symmetric_difference_update  T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   

    `更新 T0> （ T1>  * ARG  T2> ） T3> ¶ T4>`{.descname}
    :   


