---
title: 加载列
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/loading_columns/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
加载列[¶](#loading-columns "Permalink to this headline")
========================================================

本节介绍有关加载色谱柱的其他选项。

延迟列加载[¶](#deferred-column-loading "Permalink to this headline")
--------------------------------------------------------------------

此功能允许仅在直接访问时加载表的特定列，而不是使用[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")查询实体的时间。这个功能在有人想避免把无用但又很大的text字段或者二进制字段加载到内存时十分有效可以使用[`orm.deferred()`](#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")函数将各个列标记为“延迟”，从而可以单独延迟加载各个列，也可以将它们放入到一起加载的组中。在下面的例子中，我们定义了一个映射，当个人首次引用每个属性时，将在单独的单行SELECT语句中加载`.excerpt`和`.photo`对象实例：

    from sqlalchemy.orm import deferred
    from sqlalchemy import Integer, String, Text, Binary, Column

    class Book(Base):
        __tablename__ = 'book'

        book_id = Column(Integer, primary_key=True)
        title = Column(String(200), nullable=False)
        summary = Column(String(2000))
        excerpt = deferred(Column(Text))
        photo = deferred(Column(Binary))

经典映射始终将[`orm.deferred()`](#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")用于`properties`字典中与表绑定[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的用法：

    mapper(Book, book_table, properties={
        'photo':deferred(book_table.c.photo)
    })

延迟列可以与“组”名称相关联，以便在第一次访问它们时加载它们。下面的例子定义了一个带有`photos`延期组的映射。当访问一个`.photo`时，所有三张照片将被加载到一个SELECT语句中。访问时，`.excerpt`将单独加载：

    class Book(Base):
        __tablename__ = 'book'

        book_id = Column(Integer, primary_key=True)
        title = Column(String(200), nullable=False)
        summary = Column(String(2000))
        excerpt = deferred(Column(Text))
        photo1 = deferred(Column(Binary), group='photos')
        photo2 = deferred(Column(Binary), group='photos')
        photo3 = deferred(Column(Binary), group='photos')

您可以使用选项（包括[`orm.defer()`](#sqlalchemy.orm.defer "sqlalchemy.orm.defer")和[`orm.undefer()`](#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")）推迟或取消[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")级别的列：

    from sqlalchemy.orm import defer, undefer

    query = session.query(Book)
    query = query.options(defer('summary'))
    query = query.options(undefer('excerpt'))
    query.all()

[`orm.deferred()`](#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")
attributes which are marked with a “group” can be undeferred using
[`orm.undefer_group()`](#sqlalchemy.orm.undefer_group "sqlalchemy.orm.undefer_group"),
sending in the group name:

    from sqlalchemy.orm import undefer_group

    query = session.query(Book)
    query.options(undefer_group('photos')).all()

### 仅加载列[¶](#load-only-cols "Permalink to this headline")

使用[`orm.load_only()`](#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")可以选择任意一组列作为“仅加载”列，这些列将在推迟给定实体上的所有其他列时加载。

    from sqlalchemy.orm import load_only

    session.query(Book).options(load_only("summary", "excerpt"))

版本0.9.0中的新功能

### 多个实体的延期加载[¶](#deferred-loading-with-multiple-entities "Permalink to this headline")

要在加载多种类型实体的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")中指定列延迟选项，[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象可以指定启动哪个父实体：

    from sqlalchemy.orm import Load

    query = session.query(Book, Author).join(Book.author)
    query = query.options(
                Load(Book).load_only("summary", "excerpt"),
                Load(Author).defer("bio")
            )

为了沿着各种关系的路径指定列延期选项，选项支持链接，每个关系的加载样式首先被指定，然后链接到延期选项。例如，要加载`Book`实例，然后加入-eager-加载`Author`，然后将延迟选项应用于`Author`实体：

    from sqlalchemy.orm import joinedload

    query = session.query(Book)
    query = query.options(
                joinedload(Book.author).load_only("summary", "excerpt"),
            )

在父关系的加载样式应该保持不变的情况下，使用[`orm.defaultload()`](loading_relationships.html#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")：

    from sqlalchemy.orm import defaultload

    query = session.query(Book)
    query = query.options(
                defaultload(Book.author).load_only("summary", "excerpt"),
            )

版本0.9.0中的新功能：支持[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")和其他选项，可以更好地定位延迟选项。

### 列延迟API [¶](#column-deferral-api "Permalink to this headline")

 `sqlalchemy.orm.`{.descclassname}`deferred`{.descname}(*\*columns*, *\*\*kw*)[¶](#sqlalchemy.orm.deferred "Permalink to this definition")
:   指示一个基于列的映射属性，默认情况下将不会加载，除非被访问。

    参数：

    -   **\*列** [¶](#sqlalchemy.orm.deferred.params.*columns) -
        要映射的列。这通常是一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，但是为了支持在同一个属性下映射多个列，支持一个集合。
    -   **\*\*kw**[¶](#sqlalchemy.orm.deferred.params.**kw) – additional
        keyword arguments passed to [`ColumnProperty`](internals.html#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty").

    也可以看看

    [Deferred Column Loading](#deferred)

 `sqlalchemy.orm.`{.descclassname}`defer`{.descname}(*key*, *\*addl\_attrs*)[¶](#sqlalchemy.orm.defer "Permalink to this definition")
:   表明给定的面向列的属性应该被推迟，例如，直到访问才加载。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    例如。：

        from sqlalchemy.orm import defer

        session.query(MyClass).options(
                            defer("attribute_one"),
                            defer("attribute_two"))

        session.query(MyClass).options(
                            defer(MyClass.attribute_one),
                            defer(MyClass.attribute_two))

    要指定相关类的属性的延迟加载，可以一次指定一个令牌的路径，为链中的每个链接指定加载样式。要使链接的加载样式保持不变，请使用[`orm.defaultload()`](loading_relationships.html#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")：

        session.query(MyClass).options(defaultload("someattr").defer("some_column"))

    存在于特定路径上的[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象可以多次调用[`Load.defer()`](query.html#sqlalchemy.orm.strategy_options.Load.defer "sqlalchemy.orm.strategy_options.Load.defer")，每个对象都将在同一个父实体上运行：

        session.query(MyClass).options(
                        defaultload("someattr").
                            defer("some_column").
                            defer("some_other_column").
                            defer("another_column")
            )

    参数：

    -   **键** [¶](#sqlalchemy.orm.defer.params.key) - 待延期的属性。
    -   **\* addl\_attrs** [¶](#sqlalchemy.orm.defer.params.*addl_attrs)
        -
        弃用；此选项支持将旧路径指定为一系列属性的0.8格式，现在已被方法链式样式取代。

    也可以看看

    [Deferred Column Loading](#deferred)

    [`orm.undefer()`](#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")

` sqlalchemy.orm。 T0>  LOAD_ONLY  T1> （ T2>  * ATTRS  T3> ） T4> ¶ T5>`{.descclassname}
:   表明对于一个特定的实体，只应该加载给定的基于列的属性名称列表；所有其他人将被推迟。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    示例 - 给定类`User`，仅加载`name`和`fullname`属性：

        session.query(User).options(load_only("name", "fullname"))

    示例 - 给定一个关系`User.addresses  - >＆gt； 地址`，为`User.addresses`集合，但每个`Address`对象仅加载`email_address`属性：

        session.query(User).options(
                subqueryload("addresses").load_only("email_address")
        )

    对于具有多个实体的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，可以使用[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")构造函数专门引用前导实体：

        session.query(User, Address).join(User.addresses).options(
                    Load(User).load_only("name", "fullname"),
                    Load(Address).load_only("email_addres")
                )

    版本0.9.0中的新功能

 `sqlalchemy.orm.`{.descclassname}`undefer`{.descname}(*key*, *\*addl\_attrs*)[¶](#sqlalchemy.orm.undefer "Permalink to this definition")
:   表明给定的面向列的属性应该是未定的，例如，在整个实体的SELECT语句内指定。

    未定位的列通常在映射上设置为[`deferred()`](#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")属性。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    例子：

        # undefer two columns
        session.query(MyClass).options(undefer("col1"), undefer("col2"))

        # undefer all columns specific to a single class using Load + *
        session.query(MyClass, MyOtherClass).options(
            Load(MyClass).undefer("*"))

    参数：

    -   **键** [¶](#sqlalchemy.orm.undefer.params.key) -
        要被取消的属性。
    -   **\* addl\_attrs**
        [¶](#sqlalchemy.orm.undefer.params.*addl_attrs) -
        弃用；此选项支持将旧路径指定为一系列属性的0.8格式，现在已被方法链式样式取代。

    也可以看看

    [Deferred Column Loading](#deferred)

    [`orm.defer()`](#sqlalchemy.orm.defer "sqlalchemy.orm.defer")

    [`orm.undefer_group()`](#sqlalchemy.orm.undefer_group "sqlalchemy.orm.undefer_group")

` sqlalchemy.orm。 T0>  undefer_group  T1> （ T2> 名称 T3> ） T4> ¶ T5 >`{.descclassname}
:   指出给定的延期组名称中的列应该是未定的。

    未定位的列在映射上设置为[`deferred()`](#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")属性并包含“组”名称。

    例如：

        session.query(MyClass).options(undefer_group("large_attrs"))

    要取消相关实体上的一组属性，可以使用关系加载器选项（如[`orm.defaultload()`](loading_relationships.html#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")）来拼写路径：

        session.query(MyClass).options(
            defaultload("someattr").undefer_group("large_attrs"))

    版本0.9.0更改： [`orm.undefer_group()`](#sqlalchemy.orm.undefer_group "sqlalchemy.orm.undefer_group")现在特定于一个分立的实体加载路径。

    也可以看看

    [Deferred Column Loading](#deferred)

    [`orm.defer()`](#sqlalchemy.orm.defer "sqlalchemy.orm.defer")

    [`orm.undefer()`](#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")

列包[¶](#column-bundles "Permalink to this headline")
-----------------------------------------------------

[`Bundle`](query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")可用于在一个名称空间下查询列组。

版本0.9.0中的新功能

该捆绑允许列组合在一起：

    from sqlalchemy.orm import Bundle

    bn = Bundle('mybundle', MyClass.data1, MyClass.data2)
    for row in session.query(bn).filter(bn.c.data1 == 'd1'):
        print(row.mybundle.data1, row.mybundle.data2)

在获取结果时，可以对该包进行分类以提供自定义行为。在查询执行时，方法[`Bundle.create_row_processor()`](query.html#sqlalchemy.orm.query.Bundle.create_row_processor "sqlalchemy.orm.query.Bundle.create_row_processor")被给予[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")和一组“行处理器”函数；这些处理器函数在给出结果行时将返回单个属性值，然后可以将其调整为任何类型的返回数据结构。下面举例说明用直接的Python字典替换通常的[`KeyedTuple`](query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")返回结构：

    from sqlalchemy.orm import Bundle

    class DictBundle(Bundle):
        def create_row_processor(self, query, procs, labels):
            """Override create_row_processor to return values as dictionaries"""
            def proc(row):
                return dict(
                            zip(labels, (proc(row) for proc in procs))
                        )
            return proc

在版本1.0中改变： `proc()`可调用现在传递给自定义[`Bundle`](query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")类的`create_row_processor()`只接受一个“行”参数。

上述包的结果将返回字典值：

    bn = DictBundle('mybundle', MyClass.data1, MyClass.data2)
    for row in session.query(bn).filter(bn.c.data1 == 'd1'):
        print(row.mybundle['data1'], row.mybundle['data2'])

[`Bundle`](query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")结构也被集成到[`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")的行为中，在用作单个属性查询时，它将复合属性作为对象返回。
