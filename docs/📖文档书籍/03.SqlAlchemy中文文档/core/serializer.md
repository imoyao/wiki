---
title: 表达式串行器扩展
date: 2021-02-20 22:41:36
permalink: /sqlalchemy/core/serializer/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
表达式串行器扩展[¶](#module-sqlalchemy.ext.serializer "Permalink to this headline")
===================================================================================

Serializer /
Deserializer 对象与 SQLAlchemy 查询结构一起使用，允许“上下文”反序列化。

任何基于 sqlalchemy.sql 的 SQLAlchemy 查询结构。\*或 sqlalchemy.orm。\*可以使用。映射器，表格，列，会话等结构引用的内容不是以序列化形式持久化的，而是在反序列化时与查询结构重新关联。

用法与标准 Python pickle 模块的用法几乎相同：

    from sqlalchemy.ext.serializer import loads, dumpsplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain
    metadata = MetaData(bind=some_engine)
    Session = scoped_session(sessionmaker())

    # ... define mappers

    query = Session.query(MyClass).
        filter(MyClass.somedata=='foo').order_by(MyClass.sortkey)

    # pickle the query
    serialized = dumps(query)

    # unpickle.  Pass in metadata + scoped_session
    query2 = loads(serialized, metadata, Session)

    print query2.all()

与使用生腌菜时类似的限制适用；映射类本身必须是可以选择的，这意味着它们可以从模块级命名空间导入。

序列化器模块仅适用于查询结构。它不需要：

-   用户定义类的实例。它们在典型情况下不包含对引擎，会话或表达式结构的引用，并且可以直接序列化。
-   要完全从序列化结构加载的表元数据（即，尚未在应用程序中声明）。常规 pickle.loads()/
    dumps()可用于完全转储任何`MetaData`对象，通常是在某个先前时间点从现有数据库反映的对象。串行器模块专门用于相反的情况，其中表元数据已经存在于内存中。

 `sqlalchemy.ext.serializer.`{.descclassname}`Serializer`{.descname}(*\*args*, *\*\*kw*)[¶](#sqlalchemy.ext.serializer.Serializer "Permalink to this definition")
:   

 `sqlalchemy.ext.serializer.`{.descclassname}`Deserializer`{.descname}(*file*, *metadata=None*, *scoped\_session=None*, *engine=None*)[¶](#sqlalchemy.ext.serializer.Deserializer "Permalink to this definition")
:   

 `sqlalchemy.ext.serializer.`{.descclassname}`dumps`{.descname}(*obj*, *protocol=0*)[¶](#sqlalchemy.ext.serializer.dumps "Permalink to this definition")
:   

 `sqlalchemy.ext.serializer.`{.descclassname}`loads`{.descname}(*data*, *metadata=None*, *scoped\_session=None*, *engine=None*)[¶](#sqlalchemy.ext.serializer.loads "Permalink to this definition")
:   

