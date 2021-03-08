---
title: 可转位
date: 2021-02-20 22:41:42
permalink: /sqlalchemy/orm/extensions/indexable/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
可转位[¶ T0\>](#module-sqlalchemy.ext.indexable "Permalink to this headline")
=============================================================================

在具有[`Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")类型的列上定义具有“索引”属性的 ORM 映射类上的属性。

“index”表示该属性与具有预定义索引的[`Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")列的元素相关联以访问它。[`Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")类型包括[`ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")，[`JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")和[`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")等类型。

The [`indexable`](#module-sqlalchemy.ext.indexable "sqlalchemy.ext.indexable")
extension provides [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")-like
interface for any element of an [`Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")
typed column. 在简单的情况下，它可以被视为[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
- 映射的属性。

版本 1.1 中的新功能

概要[¶ T0\>](#synopsis "Permalink to this headline")
----------------------------------------------------

将`Person`作为包含主键和JSON数据字段的模型。虽然此字段可能包含任何数量的编码元素，但我们希望单独将名为`name`的元素称为专用属性，其行为与独立列相同：

    from sqlalchemy import Column, JSON, Integerplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.ext.indexable import index_property

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        data = Column(JSON)

        name = index_property('data', 'name')

以上，现在，`name`属性的行为与映射列相似。我们可以编写一个新的`Person`并设置`name`：

    >>> person = Person(name='Alchemist')plainplain

该值现在可以访问：

    >>> person.nameplainplain
    'Alchemist'

在幕后，JSON 字段被初始化为一个新的空字典并且字段被设置：

    >>> person.dataplain
    {"name": "Alchemist'}

该领域是可变的：

    >>> person.name = 'Renamed'plain
    >>> person.name
    'Renamed'
    >>> person.data
    {'name': 'Renamed'}

当使用[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")时，我们对可索引结构所做的更改也会自动作为历史记录进行跟踪；我们不再需要使用[`MutableDict`](mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")来跟踪工作单元的这种变化。

删除也正常工作：

    >>> del person.name
    >>> person.data
    {}

以上，`person.name`的删除将从字典中删除值，但不会删除字典本身。

缺少的密钥会产生`AttributeError`：

    >>> person = Person()
    >>> person.name
    ...
    AttributeError: 'name'

这些属性也可以在课堂上进行访问。下面，我们举例说明用于生成索引 SQL 标准的`Person.name`：

    >>> from sqlalchemy.orm import Sessionplainplain
    >>> session = Session()
    >>> query = session.query(Person).filter(Person.name == 'Alchemist')

上述查询等同于：

    >>> query = session.query(Person).filter(Person.data['name'] == 'Alchemist')plain

可以链接多个[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")对象以产生多级索引：

    from sqlalchemy import Column, JSON, Integer
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.ext.indexable import index_property

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        data = Column(JSON)

        birthday = index_property('data', 'birthday')
        year = index_property('birthday', 'year')
        month = index_property('birthday', 'month')
        day = index_property('birthday', 'day')

以上，一个查询如：

    q = session.query(Person).filter(Person.year == '1980')plainplain

在 Postgresql 后端，上述查询将呈现为：

    SELECT person.id, person.dataplainplain
    FROM person
    WHERE person.data -> %(data_1)s -> %(param_1)s = %(param_2)s

默认值[¶](#default-values "Permalink to this headline")
-------------------------------------------------------

[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")
includes special behaviors for when the indexed data structure does not
exist, and a set operation is called:

-   对于给定整数索引值的[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")，默认数据结构将是`None`值的 Python 列表，至少与索引值一样长；该值将被设置在列表中的位置。这意味着对于索引值为零的列表，在设置给定值之前，列表将初始化为`[None]`，对于索引值 5，列表将初始化为`设置前设为[无， 无， 无， 无， 无]`给定值的第五个元素。请注意，现有的列表**不是**扩展到位以接收值。
-   对于给定任何其他类型的索引值（例如字符串）的[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")，Python 字典将用作默认数据结构。
-   可以使用[`index_property.datatype`](#sqlalchemy.ext.indexable.index_property.params.datatype "sqlalchemy.ext.indexable.index_property")参数将默认数据结构设置为可调用的任何 Python，覆盖以前的规则。

子类[¶ T0\>](#subclassing "Permalink to this headline")
-------------------------------------------------------

[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")
can be subclassed, in particular for the common use case of providing
coercion of values or SQL expressions as they are accessed.
下面是 Postgresql
JSON 类型使用的一个常用方法，我们希望还包括自动转换加上`astext()`：

    class pg_json_property(index_property):plainplainplainplain
        def __init__(self, attr_name, index, cast_type):
            super(pg_json_property, self).__init__(attr_name, index)
            self.cast_type = cast_type

        def expr(self, model):
            expr = super(pg_json_property, self).expr(model)
            return expr.astext.cast(self.cast_type)

上面的子类可以与 Postgresql 特定版本的[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")一起使用：

    from sqlalchemy import Column, Integerplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.dialects.postgresql import JSON

    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        data = Column(JSON)

        age = pg_json_property('data', 'age', Integer)

实例级别的`age`属性与之前一样；然而，在渲染 SQL 时，Postgresql 的`->>`运算符将用于索引访问，而不是`->`的常用索引操作符：

    >>> query = session.query(Person).filter(Person.age < 20)plainplain

上面的查询将呈现：

    SELECT person.id, person.data
    FROM person
    WHERE CAST(person.data ->> %(data_1)s AS INTEGER) < %(param_1)s

API 参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 *class*`sqlalchemy.ext.indexable.`{.descclassname}`index_property`{.descname}(*attr\_name*, *index*, *datatype=None*, *mutable=True*, *onebased=True*)[¶](#sqlalchemy.ext.indexable.index_property "Permalink to this definition")
:   基础：[`sqlalchemy.ext.hybrid.hybrid_property`](hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")

    属性生成器。生成的属性描述对应于[`Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")列的对象属性。

    版本1.1中的新功能

    也可以看看

    [`sqlalchemy.ext.indexable`](#module-sqlalchemy.ext.indexable "sqlalchemy.ext.indexable")

     `__init__`{.descname}(*attr\_name*, *index*, *datatype=None*, *mutable=True*, *onebased=True*)[¶](#sqlalchemy.ext.indexable.index_property.__init__ "Permalink to this definition")
    :   创建一个新的[`index_property`](#sqlalchemy.ext.indexable.index_property "sqlalchemy.ext.indexable.index_property")。

        参数：

        -   **attr\_name**[¶](#sqlalchemy.ext.indexable.index_property.params.attr_name)
            – An attribute name of an Indexable typed column, or other
            attribute that returns an indexable structure.
        -   **index**
            [¶](#sqlalchemy.ext.indexable.index_property.params.index) -
            用于获取和设置此值的索引。这应该是整数的Python端索引值。
        -   **数据类型**
            [¶](#sqlalchemy.ext.indexable.index_property.params.datatype)
            -
            字段为空时使用的缺省数据类型。默认情况下，这是从使用的索引类型派生的；一个整数索引的Python列表，或任何其他风格的索引的Python字典。对于列表，该列表将被初始化为至少`index`个元素的无值列表。
        -   **mutable**[¶](#sqlalchemy.ext.indexable.index_property.params.mutable)
            – if False, writes and deletes to the attribute will be
            disallowed.
        -   **onebased**
            [¶](#sqlalchemy.ext.indexable.index_property.params.onebased)
            -
            假设此值的SQL表示是基于one的；也就是说，SQL中的第一个索引是1，而不是零。


