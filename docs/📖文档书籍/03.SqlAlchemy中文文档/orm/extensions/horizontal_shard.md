---
title: 水平分片
date: 2021-02-20 22:41:42
permalink: /sqlalchemy/orm/extensions/horizontal_shard/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
水平分片[¶](#module-sqlalchemy.ext.horizontal_shard "Permalink to this headline")
=================================================================================

水平分片支持。

定义了一个基本的“水平分割”系统，它允许会话跨多个数据库分发查询和持久性操作。

有关使用示例，请参阅源分布中包含的[Horizontal
Sharding](examples.html#examples-sharding)示例。

API 文档[¶](#api-documentation "Permalink to this headline")
-----------------------------------------------------------

 *class*`sqlalchemy.ext.horizontal_shard.`{.descclassname}`ShardedSession`{.descname}(*shard\_chooser*, *id\_chooser*, *query\_chooser*, *shards=None*, *query\_cls=\<class 'sqlalchemy.ext.horizontal\_shard.ShardedQuery'\>*, *\*\*kwargs*)[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession "Permalink to this definition")
:   基础：[`sqlalchemy.orm.session.Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

     `__init__`{.descname}(*shard\_chooser*, *id\_chooser*, *query\_chooser*, *shards=None*, *query\_cls=\<class 'sqlalchemy.ext.horizontal\_shard.ShardedQuery'\>*, *\*\*kwargs*)[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession.__init__ "Permalink to this definition")plainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain
    :   构建ShardedSession。

        参数：

        -   **shard\_chooser**[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession.params.shard_chooser)
            – A callable which, passed a Mapper, a mapped instance, and
            possibly a SQL clause, returns a shard ID.
            该ID可以基于对象内存在的属性或某种循环方案。如果该方案基于选择，则应设置实例上的任何状态以将其标记为参与该分片。
        -   **id\_chooser**[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession.params.id_chooser)
            – A callable, passed a query and a tuple of identity values,
            which should return a list of shard ids where the ID might
            reside. 数据库将按照此列表的顺序进行查询。
        -   **query\_chooser**[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession.params.query_chooser)
            – For a given Query, returns the list of shard\_ids where
            the query should be issued.
            所有返回的碎片结果将合并成一个列表。
        -   **shards**[¶](#sqlalchemy.ext.horizontal_shard.ShardedSession.params.shards)
            – A dictionary of string shard names to [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            objects.

 *class*`sqlalchemy.ext.horizontal_shard.`{.descclassname}`ShardedQuery`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.ext.horizontal_shard.ShardedQuery "Permalink to this definition")
:   基础：[`sqlalchemy.orm.query.Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")

    ` set_shard  T0> （ T1>  shard_id  T2> ） T3> ¶ T4>`{.descname}plainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain
    :   返回一个新的查询，限于单个分片ID。

        无论其他状态如何，返回查询的所有后续操作都将针对单个分片。


