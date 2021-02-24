---
title: changelog_03
date: 2021-02-20 22:41:27
permalink: /sqlalchemy/785a96/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.3 更新日志[¶](#changelog "Permalink to this headline")
=======================================================

0.3.11 [¶ T0\>](#change-0.3.11 "Permalink to this headline")
------------------------------------------------------------

发布日期：2007 年 10 月 14 日

### ORM [¶ T0\>](#change-0.3.11-orm "Permalink to this headline")

-   **[orm]**使用 join()沿两个不同的 m2m 表添加了从 A-\>
    B 加入的检查。这会在 0.3 中产生一个错误，但在使用别名时可能在 0.4 中。[¶](#change-795ef475f7d4b812b08e3c6d684d0937)

    参考文献：[＃687](http://www.sqlalchemy.org/trac/ticket/687)

-   **[orm]**修正了 Session.merge()中的一个小异常抛出错误（[¶](#change-88ee862c631f69b98c54fa871a991656)

-   **[orm]**固定的错误，其中映射器，链接到一个表没有 PK 列的连接，不会检测到连接的表没有 PK。[¶](#change-bd9e04477cd60c6d6a7a4cebb7f0913a)

-   **[orm]**修正了从自定义继承条件中确定合适的同步子句的错误[¶](#change-1e038d2dbcdd2153030e7394dfd58f3d)

    参考文献：[＃769](http://www.sqlalchemy.org/trac/ticket/769)

-   **[orm]**backref remove object operation doesn’t fail if the
    other-side collection doesn’t contain the item, supports noload
    collections[¶](#change-0e43e8232535b10db727543c77f728bd)

    参考文献：[＃813](http://www.sqlalchemy.org/trac/ticket/813)

### 发动机[¶ T0\>](#change-0.3.11-engine "Permalink to this headline")

-   **[engine]**修正了当使用池设置 threadlocal 时可能发生的另一个偶然争用情况[¶](#change-a8031639e187f84e4aa5334fd71c2098)

### SQL [¶ T0\>](#change-0.3.11-sql "Permalink to this headline")

-   **[sql]**调整像 func.count（t.c.col.distinct()）这样的子句的 DISTINCT 优先级
    [¶](#change-606aa4f88278c9f53504856ea6950d76)

-   **[sql]**修复了内部'\$'字符的检测：bind \$ params
    [¶](#change-d8d45d29d80bd66d00ef851e04a3f82b)

    参考文献：[＃719](http://www.sqlalchemy.org/trac/ticket/719)

-   **[sql]**不要假设连接条件只包含列对象[¶](#change-d5969ca86631966109273bba06c34ca5)

    参考文献：[＃768](http://www.sqlalchemy.org/trac/ticket/768)

-   **[sql]**adjusted operator precedence of NOT to match ‘==’ and
    others, so that \~(x==y) produces NOT (x=y), which is compatible
    with MySQL \< 5.0 (doesn’t like “NOT
    x=y”)[¶](#change-adee1f3a5bf6063740c4e5d0d8759576)

    参考文献：[＃764](http://www.sqlalchemy.org/trac/ticket/764)

### MySQL 的[¶ T0\>](#change-0.3.11-mysql "Permalink to this headline")

-   **[mysql]**生成模式时固定指定 YEAR 列[¶](#change-0925c07610677ed2716dea213bbd0a75)

### 源码[¶ T0\>](#change-0.3.11-sqlite "Permalink to this headline")

-   **[sqlite]**
    passthrough 字符串日期[¶](#change-cb3f35b104dcbe7a26298edfc829c240)

### MSSQL [¶ T0\>](#change-0.3.11-mssql "Permalink to this headline")

-   **[mssql]**增加了对 TIME 列的支持（使用 DATETIME 进行模拟）[¶](#change-9ae1839db8b6431a7d9a951df9db226f)

    参考文献：[＃679](http://www.sqlalchemy.org/trac/ticket/679)

-   **[mssql]**增加了对 BIGINT，MONEY，SMALLMONEY，UNIQUEIDENTIFIER 和 SQL\_VARIANT 的支持[¶](#change-22d1b8a85d2e3fad306665d645da0f78)

    参考文献：[＃721](http://www.sqlalchemy.org/trac/ticket/721)

-   **[mssql]**索引名现在在从反映表中删除时引用[¶](#change-b1949f314913ce8e14c5552e9e90e924)

    参考文献：[＃684](http://www.sqlalchemy.org/trac/ticket/684)

-   **[mssql]**can now specify a DSN for PyODBC, using a URI like
    mssql:///?dsn=bob[¶](#change-dc27077ba3230cb424fcf4b4b8185ac1)

### 预言[¶ T0\>](#change-0.3.11-oracle "Permalink to this headline")

-   **[oracle]**从“二进制”类型中删除了 LONG\_STRING，LONG\_BINARY，所以类型对象不会尝试读取它们的值作为 LOB。[¶](#change-5f0bd7c8398c9a49d384e169dded9299)

    参考文献：[＃622](http://www.sqlalchemy.org/trac/ticket/622)，[＃751](http://www.sqlalchemy.org/trac/ticket/751)

### 火鸟[¶ T0\>](#change-0.3.11-firebird "Permalink to this headline")

-   由于票＃370（正确的方式）**[firebird]**
    supports\_sane\_rowcount()设置为 False
    [¶](#change-68a13c0986d622612ea9b90a1e732d21)

-   **[firebird]**固定反映 Column 的可空属性[¶](#change-6d153f889ecfbaa34265a173aef5720d)

### 杂项[¶ T0\>](#change-0.3.11-misc "Permalink to this headline")

-   当反映来自其他模式的表时，放置在主键上的“默认”（即通常是序列名称）具有无条件引用的“模式”名称，以便需要引用的模式名称是**[postgres]**精细。对于不需要引用但不会造成危害的模式名称，它稍微不必要。[¶](#change-c26caf7b92713b64413c6519ddfa159a)

0.3.10 [¶ T0\>](#change-0.3.10 "Permalink to this headline")
------------------------------------------------------------

发布时间：2007 年 7 月 20 日星期五

### 一般[¶ T0\>](#change-0.3.10-general "Permalink to this headline")

-   **[general]**a new mutex that was added in 0.3.9 causes the
    pool\_timeout feature to fail during a race condition; threads would
    raise TimeoutError immediately with no delay if many threads push
    the pool into overflow at the same time.
    这个问题已得到解决。[¶](#change-d21e68c9886bf315a5224f8aedf8c2f0)

### ORM [¶ T0\>](#change-0.3.10-orm "Permalink to this headline")

-   **[orm]**cleanup to connection-bound sessions,
    SessionTransaction[¶](#change-abc5c622ebf7f48299346d88e835234a)

### SQL [¶ T0\>](#change-0.3.10-sql "Permalink to this headline")

-   **[sql]**获取连接绑定的元数据以使用隐式执行[¶](#change-f1f6a898d9d4aad0cfea3d441d7da52c)

-   **[sql]**foreign key specs can have any chararcter in their
    identifiers[¶](#change-513834dddb580f41af0e07c8084eedb6)

    参考文献：[＃667](http://www.sqlalchemy.org/trac/ticket/667)

-   **[sql]**将交换性意识添加到二进制子句比较中，改进了 ORM 延迟加载优化[¶](#change-2b2c84c6ab73af1cb0a95c1ef7da18e8)

    参考文献：[＃664](http://www.sqlalchemy.org/trac/ticket/664)

### 杂项[¶ T0\>](#change-0.3.10-misc "Permalink to this headline")

-   **[postgres]**固定的最大标识符长度（63）[¶](#change-ad87700ec6114efcef15a751769a83f7)

    参考文献：[＃571](http://www.sqlalchemy.org/trac/ticket/571)

0.3.9 [¶ T0\>](#change-0.3.9 "Permalink to this headline")
----------------------------------------------------------

发布日期：2007 年 7 月 15 日

### 一般[¶ T0\>](#change-0.3.9-general "Permalink to this headline")

-   **[general]**更好的错误消息为 NoSuchColumnError
    [¶](#change-15b74e04e779630532bed8eb2cb6e6c1)

    参考文献：[＃607](http://www.sqlalchemy.org/trac/ticket/607)

-   **[general]**终于想出了如何获取 setuptools 的版本，可以作为 sqlalchemy
    .\_\_ version \_\_ [¶](#change-1a63992eb7fa15d2defa97764255fbc0)

    参考文献：[＃428](http://www.sqlalchemy.org/trac/ticket/428)

-   **[general]**the various “engine” arguments, such as “engine”,
    “connectable”, “engine\_or\_url”, “bind\_to”, etc.
    都存在，但不推荐使用。它们全部被单一术语“绑定”取代。您还可以使用 metadata.bind
    = [¶](#change-a914144f1b4a77794f443fe172406549)设置 MetaData 的“绑定”

### ORM [¶ T0\>](#change-0.3.9-orm "Permalink to this headline")

-   **[orm]**向前兼容 0.4：向 Query 添加 one()，first()和 all()。几乎所有来自 0.4 的 Query 功能都出现在 0.3.9 中，用于前向兼容目的。[¶](#change-301449c29e0fd8c8dbf2a0cbf6bbb0a7)

-   **[orm]**
    reset\_joinpoint()这次确实真的有效，诺言！可以让你重新加入根：query.join（['a'，'b']）。filter（）。reset\_joinpoint()。join（['a'，'c']）。filter
    ）。all 中的 all()在所有 join()调用中都从“root”开始[¶](#change-3d04848b5b90892e4896d27e42104550)

-   **[orm]**向 mapper()构造步骤添加了同步，以避免预先存在的映射器在另一个线程中编译时的线程冲突[¶](#change-a0eabad47f40a8f2c05402d784e913e5)

    参考文献：[＃613](http://www.sqlalchemy.org/trac/ticket/613)

-   **[orm]**a warning is issued by Mapper when two primary key columns
    of the same name are munged into a single attribute.
    这在映射到连接（或继承）时经常发生。[¶](#change-7511ce30f30748be291cfdd03fd2985c)

-   **[orm]**synonym() properties are fully supported by all Query
    joining/ with\_parent
    operations[¶](#change-2b84bfaaf17d2ee58aef7c2087b5d1a2)

    参考文献：[＃598](http://www.sqlalchemy.org/trac/ticket/598)

-   **[orm]**在删除多对多的项目时修复了非常愚蠢的错误 uselist =
    False 关系[¶](#change-29072b60d67f065003dc3d3c58fc4f41)

-   **[orm]**请记住关于 polymorphic\_union 的所有内容吗？用于连接表继承？有趣的事情……你可以通过 outerjoin()将所有的表串联在一起。但是，如果涉及具体表，UNION 仍然适用（因为没有任何关联）。[¶](#change-7c527faac0be51d0670878009672f72e)

-   **[orm]**针对急切加载的小修复，以更好地处理正在使用直接“外连接”子句的多态映射器[¶](#change-fe5f2850304952163433155f047967b3)

### SQL [¶ T0\>](#change-0.3.9-sql "Permalink to this headline")

-   **[sql]**ForeignKey to a table in a schema that’s not the default
    schema requires the schema to be explicit; i.e.
    ForeignKey(‘alt\_schema.users.id’)[¶](#change-5facd76a849bbd35a1d758bee9da40c8)

-   **[sql]**MetaData can now be constructed with an engine or url as
    the first argument, just like
    BoundMetaData[¶](#change-cf52683aa8efacf1647755b6e2f1acf9)

-   **[sql]**现在不推荐使用 BoundMetaData，MetaData 是直接替代。[¶](#change-2539cd0d61dd58d959c61c6876dc1209)

-   **[sql]**
    DynamicMetaData 已重命名为 ThreadLocalMetaData。DynamicMetaData 名称已被弃用，并且是 ThreadLocalMetaData 或常规元数据的别名，如果 threadlocal
    = False [¶](#change-10f3b9882e40dd9a45d7188ae6a8237c)

-   **[sql]**composite primary key is represented as a non-keyed set to
    allow for composite keys consisting of cols with the same name;
    occurs within a Join.
    帮助继承场景制定正确的 PK。[¶](#change-03586a372d9beeedd862f01e0addc777)

-   **[sql]**improved ability to get the “correct” and most minimal set
    of primary key columns from a join, equating foreign keys and
    otherwise equated columns.
    这也主要是为了帮助继承场景制定主键列的最佳选择。[¶](#change-afa1167f3e5743e5abd5356d62de6046)

    参考文献：[＃185](http://www.sqlalchemy.org/trac/ticket/185)

-   **[sql]**为 Sequence.create()/
    drop()，ColumnDefault.execute()[添加了'bind'参数](#change-9c7cdd3f8030a2d57cf94f1f1f892b4c)

-   **[sql]**列可以在具有不同于列名的“key”属性（包括主键列）的反映表中重写[¶](#change-81ad0a30acb500499415014b6aefd421)

    参考文献：[＃650](http://www.sqlalchemy.org/trac/ticket/650)

-   **[sql]**固定“歧义列”结果检测，当 dupe
    col 名称存在于结果中时[¶](#change-4b5d1e9e40c66d1b53a831c30e88292a)

    参考文献：[＃657](http://www.sqlalchemy.org/trac/ticket/657)

-   **[sql]**some enhancements to “column targeting”, the ability to
    match a column to a “corresponding” column in another selectable.
    这主要影响 ORM 映射到复杂联接的能力[¶](#change-dc154cb277d63d3f13716fab650411d5)

-   **[sql]**MetaData and all SchemaItems are safe to use with pickle.
    缓慢的桌面反射可以被转储到一个腌制的文件中以后再使用。取出后，只需将引擎重新连接到元数据即可。[¶](#change-a0f1f7110e545dcbde1e4a60d9b028cc)

    参考文献：[＃619](http://www.sqlalchemy.org/trac/ticket/619)

-   **[sql]**在 QueuePool 的“溢出”计算中添加了一个互斥量，以防止可能绕过 max\_overflow 的争用条件[¶](#change-c1578db6e36277a7adc101ca74177397)

-   **[sql]**固定分组的复合选择给出正确的结果。会在某些情况下在 sqlite 中断开，但是这些情况无论如何都会产生不正确的结果，sqlite 不支持分组复合选择[¶](#change-3b19729cd27655192e7f677db9437a75)

    参考文献：[＃623](http://www.sqlalchemy.org/trac/ticket/623)

-   **[sql]**运算符的固定优先级，以便正确应用括号[¶](#change-1a5573250745da4cc296c5478a905559)

    参考文献：[＃620](http://www.sqlalchemy.org/trac/ticket/620)

-   **[sql]**调用.in\_()（即没有参数）将返回“CASE WHEN（IS NULL）THEN
    NULL ELSE 0 END =
    1）”，在任何情况下都会返回 False，而不是抛出错误[¶](#change-f3c83d18250d490e0c0e719048bb5c78)

    参考文献：[＃545](http://www.sqlalchemy.org/trac/ticket/545)

-   **[sql]**fixed “where”/”from” criterion of select() to accept a
    unicode string in addition to regular string - both convert to
    text()[¶](#change-29d36e2ae856641782a99036963ac096)

-   **[sql]**added standalone distinct() function in addition to
    column.distinct()[¶](#change-d5193859e2955a59dd9b9689c9c46766)

    参考文献：[＃558](http://www.sqlalchemy.org/trac/ticket/558)

-   **[sql]**result.last\_inserted\_ids() should return a list that is
    identically sized to the primary key constraint of the table.
    被动地创建并且不能通过 cursor.lastrowid 获得的值将是 None。[¶](#change-22737e38569c4710d50bad784dc3c2f6)

-   **[sql]**长标识符检测固定使用\>而不是\>
    =用于最大标识长度[¶](#change-133fed2970fe02b19469b87df37569d2)

    参考文献：[＃589](http://www.sqlalchemy.org/trac/ticket/589)

-   **[sql]**fixed bug where
    selectable.corresponding\_column(selectable.c.col) would not return
    selectable.c.col, if the selectable is a join of a table and another
    join involving the same table.
    搞砸了 ORM 决策[¶](#change-4b796f178bce68c33756958792addb5e)

    参考文献：[＃593](http://www.sqlalchemy.org/trac/ticket/593)

-   **[sql]**将 Interval 类型添加到 types.py
    [¶](#change-01be6714d969a9a05321795a1a05462e)

    参考文献：[＃595](http://www.sqlalchemy.org/trac/ticket/595)

### MySQL 的[¶ T0\>](#change-0.3.9-mysql "Permalink to this headline")

-   **[mysql]**固定捕获一些暗示连接断开的错误[¶](#change-a2ea4c40b80240eda48ac840435d5023)

    参考文献：[＃625](http://www.sqlalchemy.org/trac/ticket/625)

-   **[mysql]**固定模运算符的转义[¶](#change-d2c713d82a5cc3352589d3b97a4f1a75)

    参考文献：[＃624](http://www.sqlalchemy.org/trac/ticket/624)

-   **[mysql]**将'fields'添加到保留字[¶](#change-ccc1148a1c82ef495cc71ca9962442b9)

    参考文献：[＃590](http://www.sqlalchemy.org/trac/ticket/590)

-   **[mysql]**各种反射增强/修复[¶](#change-706aff419d104524d8aee408e01fca4b)

### 源码[¶ T0\>](#change-0.3.9-sqlite "Permalink to this headline")

-   **[sqlite]**重新安排了方言初始化，所以有时间警告 pysqlite1 太旧了。[¶](#change-cda34421fe7120853f316f8e8cfbc11b)

-   **[sqlite]**
    sqlite 更好地处理与各种日期/时间/日期时间列混合和匹配的日期/时间/时间对象[¶](#change-123da4b941ba10797888a9215510d452)

-   **[sqlite]**字符串 PK 列插入不会被 OID 覆盖[¶](#change-ecc1a278352da6fe50070d9f2df39fc6)

    参考文献：[＃603](http://www.sqlalchemy.org/trac/ticket/603)

### MSSQL [¶ T0\>](#change-0.3.9-mssql "Permalink to this headline")

-   **[mssql]**修复 pyodbc 的端口选项处理[¶](#change-2bfbe63bd44f73945555c6ffb24c094e)

    参考文献：[＃634](http://www.sqlalchemy.org/trac/ticket/634)

-   **[mssql]**now able to reflect start and increment values for
    identity columns[¶](#change-1e148d4d69c64d022729a0015335e1e8)

-   **[mssql]**preliminary support for using scope\_identity() with
    pyodbc[¶](#change-439f3b4aba1eb4036d66b94a0f22614d)

### 预言[¶ T0\>](#change-0.3.9-oracle "Permalink to this headline")

-   **[oracle]**
    datetime 修复：获得亚秒 TIMESTAMP 工作，添加了支持类型日期的 OracleDate，只有年/月/日[¶](#change-7c280ed8cae1ff8178c595a4ad188950)

    参考文献：[＃604](http://www.sqlalchemy.org/trac/ticket/604)

-   **[oracle]**添加方言标志“auto\_convert\_lobs”，默认为 True；将导致在结果集中检测到的任何 LOB 对象被强制进入 OracleBinary，以便在没有类型映射的情况下自动读取 LOB（即，如果发布了文本 execute()）。[¶
    t2 \>](#change-fe2a41d1863a635eb6874cd35fb20b48)

-   **[oracle]** mod 运算符'％'产生 MOD
    [¶](#change-1785061d703c74bd4913416cc528e437)

    参考文献：[＃624](http://www.sqlalchemy.org/trac/ticket/624)

-   **[oracle]**converts cx\_oracle datetime objects to Python
    datetime.datetime when Python 2.3
    used[¶](#change-ae5989d376a6e417a66cf93a4214f7d1)

    参考文献：[＃542](http://www.sqlalchemy.org/trac/ticket/542)

-   **[oracle]**在 Oracle
    TEXT 类型[中固定 unicode 转换¶](#change-2cdcc2d95fcff22d45cbf69a4828bb78)

### 杂项[¶ T0\>](#change-0.3.9-misc "Permalink to this headline")

-   **[ext]**iteration over dict association proxies is now dict-like,
    not InstrumentedList-like (e.g. over keys instead of
    values)[¶](#change-eb702c9d953f71913b8f13239bd1ace3)

-   **[ext]**关联代理不再紧密地绑定到源集合，而是用 thunk 构建而不是[¶](#change-00e6c94fbb4056e8fd8396d98317361e)

    参考文献：[＃597](http://www.sqlalchemy.org/trac/ticket/597)

-   **[ext]**将 selectone\_by()添加到 assignmapper
    [¶](#change-2e4b108cd893d88498c7604cffd62078)

-   **[postgres]**固定模运算符的转义[¶](#change-d2c713d82a5cc3352589d3b97a4f1a75)

    参考文献：[＃624](http://www.sqlalchemy.org/trac/ticket/624)

-   **[postgres]**增加了对域[¶](#change-64c391579ec741ebb893bf0eda8954dd)的反射支持

    参考文献：[＃570](http://www.sqlalchemy.org/trac/ticket/570)

-   **[postgres]**类型解析为空类型而不是引发错误[¶](#change-7155ff564edfbf3f017269ef87e325b1)

-   **[postgres]**上面的“schema”中的修复修复了从 alt-schema 表到外部公共模式表的外键反映[¶](#change-059d6872923fb7b2dd4dbe3e1b480fa1)

0.3.8 [¶ T0\>](#change-0.3.8 "Permalink to this headline")
----------------------------------------------------------

发布日期：2007 年 6 月 2 日

### ORM [¶ T0\>](#change-0.3.8-orm "Permalink to this headline")

-   **[orm]**在查询中添加了 reset\_joinpoint()方法，将“连接点”移回到起始映射器。0.4 会改变 join()的行为来重置所有情况下的“连接点”，所以这是一种临时方法。为了向前兼容，确保使用单个 join()，即 join（['a'，'b'，'c']）来指定跨多个关系的连接。[¶](#change-220bb837574d279c29a38a113e5fe6cc)

-   **[orm]**修正了 query.instances()中的错误，该错误不会处理超过附加映射器或一个附加列。[¶](#change-83691e3c49fa12bf686a08d0a5af2c40)

-   **[orm]**“delete-orphan”不再意味着“删除”。正在不断努力分离这两种操作的行为。[¶](#change-0a134f37a0801fcebac51e263334c46e)

-   **[orm]**多对多关系正确设置关联表上删除操作的绑定参数的类型[¶](#change-a7c0ffc4d0d71da2376e9be63199b048)

-   **[orm]**many-to-many relationships check that the number of rows
    deleted from the association table by a delete operation matches the
    expected results[¶](#change-cb313a2a343c37587dcb6a44a61e9cd5)

-   **[orm]**session.get() and session.load() propagate \*\*kwargs
    through to query[¶](#change-903aed08735804f496b188549879ab4f)

-   **[orm]**修复了多态查询，它允许将原始的 polymorphic\_union 嵌入到相关的子查询中[¶](#change-4900a187a33ec9e4b25fecb93f373349)

    参考文献：[＃577](http://www.sqlalchemy.org/trac/ticket/577)

-   **[orm]**修复了 select\_by（=

    ）风格的连接与多对多关系，r2556 中引入的 bug
    [](#change-8a65a9ccd3b899be79463c57097742a8) t3 \> T2\>

-   **[orm]**映​​射器()的“primary\_key”参数传播到“多态”映射器。这个列表中的主键列被标准化为映射器本地表格的主键列。[¶](#change-364da54ef89796ce592a65df9986c2de)

-   **[orm]**在 sa.orm.strategies 记录器中恢复了“lazy loading
    clause”的记录，在 0.3.7 中被删除[¶](#change-49c52ba1ca54032ac76f17ea1ac98f39)

-   **[orm]**改进了对映射到 select()语句的映射器的属性的预先加载支持；即 eagerloader 可以更好地定位正确的可选属性，以便连接它的 LEFT
    OUTER JOIN。[¶](#change-c4c11ecc4b62a615e38a3a2aa51ea362)

### SQL [¶ T0\>](#change-0.3.8-sql "Permalink to this headline")

-   **[sql]**
    \_Label 类重写 compare\_self 以返回其最终对象。意思是，如果你说 someexpr.label（'foo'）==
    5，它会产生正确的“someexpr ==
    5”。[¶](#change-b633ad04bf23c91721ac0943b6db5eca)

-   **[sql]**\_Label propagates “\_hide\_froms()” so that scalar selects
    behave more properly with regards to FROM clause
    \#574[¶](#change-2f98e49a9c61f9fdc7c291653364afe9)

-   **[sql]**通过（在映射程序查询中严重使用 oid）将 oid\_column 用作顺序时修复了长名称生成[¶](#change-e7872b2b2a3bbd38c13e8950a8e540bf)

-   **[sql]**significant speed improvement to ResultProxy, pre-caches
    TypeEngine dialect implementations and saves on function calls per
    column[¶](#change-936ba4bd4f829a2f737cd53def3e14fc)

-   **[sql]**parenthesis are applied to clauses via a new \_Grouping
    construct.
    使用运算符优先级更智能地将括号应用于子句，提供更干净的子句嵌套（不会改变放置在其他子句中的子句，即不包含'parens'标志）[¶](#change-fc92e69994fc285cf4e0fd2f1f78cec5)

-   **[sql]**添加了'modifier'关键字，其功能类似于 func。除了不添加括号外。
    T2\>例如 select（[modifier.DISTINCT（...）]）等。[¶](#change-bb4e8c5c4e8e15649157fd777ceefdc2)

-   **[sql]**移除了“在 UNION”限制的选择中没有分组 by“[¶](#change-6c51873f355f528caf99b2451980c036)

    参考文献：[＃578](http://www.sqlalchemy.org/trac/ticket/578)

### MySQL 的[¶ T0\>](#change-0.3.8-mysql "Permalink to this headline")

-   **[mysql]**现在几乎所有的 MySQL 列类型都支持声明和反射。添加了 NCHAR，NVARCHAR，VARBINARY，TINYBLOB，LONGBLOB，YEAR
    [¶](#change-9641b6abc326362d6deac112eace4afb)

-   **[mysql]** sqltypes.Binary
    passthrough 现在总是建立一个 BLOB，避免了很老的数据库版本的问题[¶](#change-18085e3f56d8b900bc96c38dd5a26b45)

-   **[mysql]**支持列级别 CHARACTER
    SET 和 COLLATE 声明，以及 ASCII，UNICODE，NATIONAL 和 BINARY 简写。[¶](#change-9724aa42d8520597d817509db4f12ea8)

### 火鸟[¶ T0\>](#change-0.3.8-firebird "Permalink to this headline")

-   **[firebird]**将最大标识符长度设置为 31
    [¶](#change-0a0b981a70a945c67ba5720e526c1f3c)

-   **[firebird]**supports\_sane\_rowcount() set to False due to ticket
    \#370. versioned\_id\_col feature wont work in
    FB.[¶](#change-ee8ef044cfb4e438086a05caa7914ae7)

-   **[firebird]**一些执行修复[¶](#change-4caef4c969ab8a7577cc51fc60890d5e)

-   **[firebird]**新的关联代理实现，实现对列表，字典和基于集合的关系集合的完整代理[¶](#change-794981a4b2ff6f2c7dd837ecebbc73c5)

-   **[firebird]**添加了 orderslist，一个自定义列表类，用于将对象属性与列表中的对象位置同步[¶](#change-63cb2d366f99e745287c162781638285)

-   **[firebird]**在 select()中不会绕过 SelectResultsExt。[¶](#change-26aa9970c7ff168af29ed9bc9c0eed85)

-   **[firebird]**将 filter()，filter\_by()添加到了 assignmapper
    [¶](#change-59a547b4472cbf0c7ab99ad2df75dfd1)

### 杂项[¶ T0\>](#change-0.3.8-misc "Permalink to this headline")

-   **[engines]**将 detach()添加到 Connection，允许将底层 DBAPI 连接从其池中分离，关闭 dereference
    / close()而不是被池重用。[¶ t2
    \>](#change-dac5031c19faee84b91961d912ecba94)

-   **[engines]**在 Connection 中添加了 invalidate()，立即使 Connection 和它的底层 DBAPI 连接失效。[¶](#change-4f0f262d9c14896c7b7e1477cfee8d6e)

0.3.7 [¶ T0\>](#change-0.3.7 "Permalink to this headline")
----------------------------------------------------------

发布于：2007 年 4 月 29 日

### ORM [¶ T0\>](#change-0.3.7-orm "Permalink to this headline")

-   **[orm]**fixed critical issue when, after options(eagerload()) is
    used, the mapper would then always apply query “wrapping” behavior
    for all subsequent LIMIT/OFFSET/DISTINCT queries, even if no eager
    loading was applied on those subsequent
    queries.[¶](#change-b70a16716f8cf919b358494b261c6e83)

-   **[orm]**添加了 query.with\_parent（someinstance）方法。使用父实例的延迟加入标准搜索目标实例。采用可选的字符串“属性”来隔离期望的关系。还添加了静态 Query.query\_from\_parent（实例，属性）版本。[¶](#change-7861d96f724ca34ac55a3d701575ffac)

    参考文献：[＃541](http://www.sqlalchemy.org/trac/ticket/541)

-   **[orm]**improved query.XXX\_by(someprop=someinstance) querying to
    use similar methodology to with\_parent, i.e. using the “lazy”
    clause which prevents adding the remote instance’s table to the SQL,
    thereby making more complex conditions
    possible[¶](#change-3a8b0fc4795043a6b42596d769387cb9)

    参考文献：[＃554](http://www.sqlalchemy.org/trac/ticket/554)

-   **[orm]**added generative versions of aggregates, i.e. sum(), avg(),
    etc. 进行查询。通过 query.apply\_max()，apply\_sum()等使用＃552 [¶
    T0\>](#change-0a56acf715d490dcc5adea669d5277ac)

-   **[orm]**固定使用 distinct()或 distinct =
    True 与 join()以及类似的[¶](#change-007141aca01632f5db21be3524e7e4b1)

-   **[orm]**对应于 label / bindparam 名称的生成，eager
    loader 为使用 md5 哈希创建的别名生成确定性名称。[¶](#change-cc8527d248fb3499b4a18f6718a08f7c)

-   **[orm]**improved/fixed custom collection classes when giving it
    “set”/ “sets.Set” classes or subclasses (was still looking for
    append() methods on them during lazy
    loads)[¶](#change-5519681da8ec6c0511745ace0e07a5e5)

-   **[orm]**restored old “column\_property()” ORM function (used to be
    called “column()”) to force any column expression to be added as a
    property on a mapper, particularly those that aren’t present in the
    mapped selectable.
    这允许将任何类型的“标量表达式”作为关系添加（尽管它们与急切的加载有关）。[¶](#change-2352eeb7d6a38352d971f1ff1053808f)

-   **[orm]**修复了针对多态映射器的多对多关系[¶](#change-af6355eefc1aad1a89924b3f68f75920)

    参考文献：[＃533](http://www.sqlalchemy.org/trac/ticket/533)

-   **[orm]**在 session.merge()方面取得进展，并将其用法与 entity\_name
    [¶](#change-9f1f52abb6da3c56fff913386ceb7882)

    参考文献：[＃543](http://www.sqlalchemy.org/trac/ticket/543)

-   **[orm]**the usual adjustments to relationships between inheriting
    mappers, in this case establishing relation()s to subclass mappers
    where the join conditions come from the superclass’
    table[¶](#change-065b2f4a27d4207c1c01b7aaade4db8a)

### SQL [¶ T0\>](#change-0.3.7-sql "Permalink to this headline")

-   **[sql]**keys() of result set columns are not lowercased, come back
    exactly as they’re expressed in cursor.description.
    注意这会导致 colname 在 oracle 中全部大写。[¶](#change-73d7e6b1e7916be07e30cac965961ce9)

-   **[sql]**preliminary support for unicode table names, column names
    and SQL statements added, for databases which can support them.
    与 sqlite 和 postgres 到目前为止。Mysql
    *主要是*，除了 has\_table()函数不起作用。反射也起作用。[¶](#change-c37360d8b51c05ae857e5b9716bddbcb)

-   **[sql]**
    Unicode 类型现在是 String 的直接子类，它现在包含所有“convert\_unicode”逻辑。这有助于更好地处理 db 中发生的各种 unicode 情况，例如 MS-SQL，并允许 Unicode 数据类型的子类化。[¶](#change-fffe5705a0f33aa08fa8f28f1ec39a83)

    参考文献：[＃522](http://www.sqlalchemy.org/trac/ticket/522)

-   **[sql]**现在可以在 in\_()子句中使用 ClauseElements，例如绑定参数等。＃476
    [¶ T0\>](#change-801d06dffa1b17f7712f296ca71f5a79)

-   **[sql]**reverse operators implemented for CompareMixin elements,
    allows expressions like “5 + somecolumn” etc. ＃474 [¶
    T0\>](#change-2fdb206fa85f07e5f47bba08e0c06013)

-   **[sql]**the “where” criterion of an update() and delete() now
    correlates embedded select() statements against the table being
    updated or deleted.
    这与嵌套 select()语句的相关性相同，并且可以通过嵌入式 select()中的 correlate
    = False 标志禁用。[¶](#change-ff895df76dd194eb810e5ca68bd903dd)

-   **[sql]**column labels are now generated in the compilation phase,
    which means their lengths are dialect-dependent.
    所以在 oracle 上，被截断为 30 个字符的标签将在 postgres 上出现 63 个字符。另外，真正的标签名总是作为访问者附加在父节点 Selectable 上，因此不需要知道“截断”标签名称。[¶](#change-88d7569964a508ab2262f1926b13c92d)

    参考文献：[＃512](http://www.sqlalchemy.org/trac/ticket/512)

-   **[sql]**column label and bind param “truncation” also generate
    deterministic names now, based on their ordering within the full
    statement being compiled.
    这意味着相同的语句会在应用程序重新启动时产生相同的字符串，并允许 DB 查询计划缓存更好地工作。[¶](#change-3a29e9cb61a8969eac7d12324eb44f91)

-   **[sql]**the “mini” column labels generated when using subqueries,
    which are to work around glitchy SQLite behavior that doesn’t
    understand “foo.id” as equivalent to “id”, are now only generated in
    the case that those named columns are selected from (part
    of)[¶](#change-07643dfce558c48c88fcd3c0dbbc207c)

    参考文献：[＃513](http://www.sqlalchemy.org/trac/ticket/513)

-   **[sql]**the label() method on ColumnElement will properly propagate
    the TypeEngine of the base element out to the label, including a
    label() created from a scalar=True select()
    statement.[¶](#change-6db4c8aa79f09bcab6c7161873c65f93)

-   **[sql]**
    MS-SQL 更好地检测到查询是子查询的时候，并且知道不会为那些[¶](#change-c987bd1aeea789b13f68c82c9c4a4ff7)生成 ORDER
    BY 短语

    参考文献：[＃513](http://www.sqlalchemy.org/trac/ticket/513)

-   **[sql]**fix for fetchmany() “size” argument being positional in
    most dbapis[¶](#change-6f431b2f1da5df6d8744478e753a48e3)

    参考文献：[＃505](http://www.sqlalchemy.org/trac/ticket/505)

-   **[sql]**将 None 作为参数发送到 func。将产生一个 NULL 参数[¶](#change-62f64e15e5caee27d5fdb304138a3d64)

-   **[sql]**query strings in unicode URLs get keys encoded to ascii for
    \*\*kwargs compat[¶](#change-8406340520cd47aabf06707f06d707e7)

-   **[sql]**原始的 execute()改变也稍微改变，以支持位置参数的元组，而不仅仅是列表[¶](#change-d6bccf2e2942ba9e7fc42b6359f5e1c5)

    参考文献：[＃523](http://www.sqlalchemy.org/trac/ticket/523)

-   **[sql]**fix to case() construct to propagate the type of the first
    WHEN condition as the return type of the case
    statement[¶](#change-e896659511f05a46c43f0bbb4a6ce393)

### MySQL 的[¶ T0\>](#change-0.3.7-mysql "Permalink to this headline")

-   **[mysql]**support for SSL arguments given as inline within URL
    query string, prefixed with “ssl\_”, courtesy
    [terjeros@gmail.com](mailto:terjeros%40gmail.com).[¶](#change-ea9d36d40ea288b0955dc117004baab9)

-   mysql 使用“DESCRIBE。”，在表不存在的情况下捕获异常，以确定表是否存在。**[mysql]
    [\<schemaname\>]**
    T2\>这支持 unicode 表名和模式名。使用 MySQL5 进行测试，但也应该使用 4.1 系列。（＃557）[¶
    T0\>](#change-a9940cb8e01661bf109d581f56990859)

### 源码[¶ T0\>](#change-0.3.7-sqlite "Permalink to this headline")

-   **[sqlite]**removed silly behavior where sqlite would reflect UNIQUE
    indexes as part of the primary key
    (?!)[¶](#change-cf170dcbc751945cb3050b2aba47a7fc)

### MSSQL [¶ T0\>](#change-0.3.7-mssql "Permalink to this headline")

-   **[mssql]**pyodbc is now the preferred DB-API for MSSQL, and if no
    module is specifically requested, will be loaded first on a module
    probe.[¶](#change-cd069bfe49e81ecb1723ce2f455629d9)

-   **[mssql]**现在使用@@ SCOPE\_IDENTITY 而不是@@
    IDENTITY。这种行为可能会被 engine\_connect“use\_scope\_identity”关键字参数覆盖，该参数也可能在 dburi 中指定。[¶](#change-98f166632883a1f0f0e9b5551435f1e4)

### 预言[¶ T0\>](#change-0.3.7-oracle "Permalink to this headline")

-   **[oracle]**小修复，允许连续编译具有 LIMIT /
    OFFSET 功能的相同 SELECT 对象。oracle 方言需要修改对象，使其具有 ROW\_NUMBER
    OVER，并且不会执行连续编译的全部步骤。[¶](#change-00f079e3efc304a332a86ad53163494c)

### 杂项[¶ T0\>](#change-0.3.7-misc "Permalink to this headline")

-   **[engines]**警告模块用于发出警告（而不是记录）[¶](#change-5769c29329bd92d3e0d54145d3c84967)

-   **[engines]**跨所有引擎清理 DBAPI 导入策略[¶](#change-7d24501b7c507a99a005fca1ced19d34)

    参考文献：[＃480](http://www.sqlalchemy.org/trac/ticket/480)

-   **[engines]**refactoring of engine internals which reduces
    complexity, number of codepaths; places more state inside of
    ExecutionContext to allow more dialect control of cursor handling,
    result sets.
    ResultProxy 完全重构，并且还有两个用于不同目的的“缓冲”结果集版本。[¶](#change-093f6563bc1d6302a6c65091f189c417)

-   **[engines]**服务器端游标支持在 postgres 中完全正常运行。[¶](#change-7563427af9a2dbabdc41b671f9119253)

    参考文献：[＃514](http://www.sqlalchemy.org/trac/ticket/514)

-   **[engines]**通过特定于方言的检测与数据库的断开连接相关的错误消息相对应的异常来自动失效已丢失其基础数据库的连接的改进框架。此外，当检测到“连接不再打开”条件时，整个连接池将被丢弃并替换为新实例。＃516
    [¶ T0\>](#change-de2734d32f9f75ca5bf6decc1c56eb11)

-   **[engines]**the dialects within sqlalchemy.databases become a
    setuptools entry points.
    加载内置数据库方言的工作方式与往常一样，但如果没有发现将回退到试图通过 pkg\_resources 加载外部模块[¶](#change-f7455a9f34d7db0039194c7cdeef8441)

    参考文献：[＃521](http://www.sqlalchemy.org/trac/ticket/521)

-   **[engines]**引擎包含引用 create\_engine()所使用的 url.URL 对象的“url”属性。[¶](#change-b231bc2f156428e9dc2d3013d285ace8)

-   **[informix]**加入 informix 支持！礼貌的詹姆斯张，他付出了很多努力。[¶](#change-ad45e2908330aaa751332d0c9d866f98)

-   **[extensions]**对 AssociationProxy 的一个很大的修复，以便多个 AssociationProxy 对象可以关联到一个关联集合。[¶](#change-a5ce4383d5826666ad4659e0d0d1b1f0)

-   **[extensions]**
    assign\_mapper 根据它们的键名称方法（即\_\_name\_\_）＃551
    [¶](#change-7d3dab36a8f8dd803d9be9c4c038dd9e)

0.3.6 [¶ T0\>](#change-0.3.6 "Permalink to this headline")
----------------------------------------------------------

发布时间：2007 年 3 月 23 日星期五

### ORM [¶ T0\>](#change-0.3.6-orm "Permalink to this headline")

-   **[orm]**the full featureset of the SelectResults extension has been
    merged into a new set of methods available off of Query.
    这些方法都提供了“生成”行为，查询被复制，并且新的查询添加了附加标准。新方法包括：

    > -   filter() - 将选择条件应用于查询
    > -   filter\_by() - 将“by”样式标准应用于查询
    > -   avg() - 返回给定列上的 avg()函数
    > -   join() - 加入属性（或属性列表）
    > -   outerjoin() - 像 join()，但使用 LEFT OUTER JOIN
    > -   limit()/ offset() - 应用 LIMIT /
    >     OFFSET 基于范围的访问，应用限制/偏移量：session.query（Foo）[3：5]
    > -   distinct() - 应用 DISTINCT
    > -   list() - 评估标准并返回结果

    Query 的 API 没有不兼容的变化，并且没有方法被弃用。像 select()，select\_by()，get()，get\_by()这样的现有方法一次执行查询并像往常一样返回结果。尽管生成的 join()/
    outerjoin()方法更容易使用，但 join\_to()/ join\_via()仍然存在。

    [¶](#change-7ab6dfcb95c397cb1aaadd385c779659)

-   **[orm]**the return value for multiple mappers used with instances()
    now returns a cartesian product of the requested list of mappers,
    represented as a list of tuples.
    这对应于记录的行为。为了使实例正确匹配，使用此功能时禁用“uniquing”。[¶](#change-346e841422c49f67aa893590d3f7a8e9)

-   **[orm]**查询具有 add\_entity()和 add\_column()生成方法。这些将在编译时将给定的 mapper
    /
    class 或 ColumnElement 添加到查询中，并将它们应用于 instances()方法。用户负责构建合理的连接条件（否则您可以获得完整的笛卡尔产品）。结果集是元组的列表，不是唯一的。[¶](#change-2795377646e93c3cb6cd134003d5dbe1)

-   **[orm]**字符串和列也可以发送到实例()的\*
    args，其中那些精确的结果列将成为结果元组的一部分。[¶](#change-9d692f0426fa9d69b169b9e1078dae86)

-   **[orm]**a full select() construct can be passed to query.select()
    (which worked anyway), but also query.selectfirst(),
    query.selectone() which will be used as is (i.e. no query is
    compiled).
    与将结果发送到 instances()类似。[¶](#change-1dc867b13e1759c636e371363f6ce297)

-   **[orm]**急于加载不会通过除了渴望加载器本身之外的东西放置在选择语句中的“排序”“排序”来修复死亡列的可能性，如图所示。然而，这意味着你必须更加小心 Query.select()的“order
    by”列中的列，你已经在你的标准中明确地命名了它们（即你不能依靠渴望的加载器为你添加它们）
    ）[¶ T0\>](#change-074438c0a67e60bc48e5420c5f490210)

    参考文献：[＃495](http://www.sqlalchemy.org/trac/ticket/495)

-   **[orm]**added a handy multi-use “identity\_key()” method to
    Session, allowing the generation of identity keys for primary key
    values, instances, and rows, courtesy Daniel
    Miller[¶](#change-8b4f380caf9d0a368e04cc060655abf0)

-   **[orm]**many-to-many table will be properly handled even for
    operations that occur on the “backref” side of the
    operation[¶](#change-87bb32d802de386360e5e46f791cdc52)

    参考文献：[＃249](http://www.sqlalchemy.org/trac/ticket/249)

-   **[orm]**添加了“刷新到期”级联。允许 refresh()和 expire()调用沿关系传播。[¶](#change-f1fbd06064c54bcac62f1348d7009f7a)

    参考文献：[＃492](http://www.sqlalchemy.org/trac/ticket/492)

-   **[orm]**more fixes to polymorphic relations, involving proper
    lazy-clause generation on many-to-one relationships to polymorphic
    mappers.
    还修复了检测“方向”的问题，更专门针对属于多态联合的列与不联合的列。[¶](#change-a975d6c5aa852fe9f1abe18ab4632941)

    参考文献：[＃493](http://www.sqlalchemy.org/trac/ticket/493)

-   **[orm]**当使用“viewonly =
    True”将其他表中的其他表拉入到关系的父/子映射的父关系中的连接条件时，修正了关系 calc
    [¶](#change-e60d7d1fb1e21d20e22cc7ee0a48e8cd)

-   **[orm]**flush fixes on cyclical-referential relationships that
    contain references to other instances outside of the cyclical chain,
    when some of the objects in the cycle are not actually part of the
    flush[¶](#change-0799b08072f174223f5a177a14fe3f19)

-   **[orm]**对“使用 B 的集合清除对象 A，但将 C 放入集合中”的错误条件 -
    **进行了积极的检查，即使 C 是 B 的子类\<
    t2\>，除非 B 的映射器多态地加载。**否则，集合稍后会加载一个“B”，它应该是一个“C”（因为它不是多形的），它在双向关系中断裂（即 C 有它的 A，但是 A 的 backref 将它作为一个不同类型的实例“B”）这个检查会咬一些没有问题的人，所以这个错误信息也会记录一个标志“enable\_typechecks
    =
    False”来禁止这个检查。但要注意，没有这种检查，双向关系尤其会变得脆弱。[¶](#change-2dd0c0ba2f51627186f0e3ca255e8679)

    参考文献：[＃500](http://www.sqlalchemy.org/trac/ticket/500)

### SQL [¶ T0\>](#change-0.3.6-sql "Permalink to this headline")

-   **[sql]**
    bindparam()名称现在可重复使用！在单个语句中指定两个具有相同名称的不同 bindparam()，并且该键将被共享。正确的位置/命名参数在编译时翻译。对于具有冲突名称的“别名”绑定参数的旧行为，请指定“unique
    = True” -
    此选项仍在内部用于所有自动生成的（基于值的）绑定参数。[¶](#change-44ab18885b5fa9a7f599390ae9397c22)

-   **[sql]**slightly better support for bind params as column clauses,
    either via bindparam() or via literal(), i.e.
    select([literal(‘foo’)])[¶](#change-32d223314680c88fa9ba080f5f3ce580)

-   **[sql]**MetaData can bind to an engine either via “url” or “engine”
    kwargs to constructor, or by using connect() method.
    BoundMetaData 与 MetaData 相同，但需要 engine\_or\_url 参数。DynamicMetaData 是相同的，并提供默认的线程本地连接。[¶](#change-cb1ef430a2696531f4258c7a228b6cd8)

-   **[sql]**exists() becomes useable as a standalone selectable, not
    just in a WHERE clause, i.e. exists([columns],
    criterion).select()[¶](#change-ff3d112668eb0765f0cea567cbea6a17)

-   **[sql]**correlated subqueries work inside of ORDER BY, GROUP
    BY[¶](#change-f69f079d1a2ab1a6dcbf3d7ad218bba7)

-   **[sql]**显式连接的固定函数执行，即 conn.execute（func.dosomething()）[¶](#change-2d6765ed8f52d6039f3ff327871651fe)

-   **[sql]**use\_labels flag on select() wont auto-create labels for
    literal text column elements, since we can make no assumptions about
    the text. 要为文字列创建标签，可以说“somecol AS
    somelabel”，或者使用 literal\_column（“somecol”）。label（“somelabel”）[¶](#change-a317e39c8ef05de7ec3007795cc6461d)

-   **[sql]**quoting wont occur for literal columns when they are
    “proxied” into the column collection for their selectable
    (is\_literal flag is propagated).
    文字列通过 literal\_column（“somestring”）指定。[¶](#change-e3edeb29a5666be8fcc4ca01511c4215)

-   **[sql]**added “fold\_equivalents” boolean argument to
    Join.select(), which removes ‘duplicate’ columns from the resulting
    column clause that are known to be equivalent based on the join
    condition.
    当构建 Postgres 抱怨有重复列名的连接子查询时，这是非常有用的。[¶](#change-f7c741c099c30418beeb3e590e129726)

-   **[sql]**在 ForeignKeyConstraint
    [上修复 use\_alter 标志¶](#change-1b52c0cfb8178249dbfa27198e657e37)

    参考文献：[＃503](http://www.sqlalchemy.org/trac/ticket/503)

-   **[sql]**在 topological.py
    [¶](#change-d6c64a3f6d7c0271de26273d1888c095)中仅固定使用 2.4“颠倒”

    参考文献：[＃506](http://www.sqlalchemy.org/trac/ticket/506)

-   **[sql]**for hackers, refactored the “visitor” system of
    ClauseElement and SchemaItem so that the traversal of items is
    controlled by the ClauseVisitor itself, using the method
    visitor.traverse(item).
    accept\_visitor()方法仍然可以直接调用，但不会执行任何子项的遍历。ClauseElement
    /
    SchemaItem 现在有一个可配置的 get\_children()方法来返回每个父对象的子元素集合。这使得遍历的项目清晰明确（以及可记录），并且使用简单的限制遍历的方法（只需传递适当的 get\_children()方法获取的标志）。[¶
    t0 \>](#change-11779379f1cac1ecc01fc15ac543b303)

    参考文献：[＃501](http://www.sqlalchemy.org/trac/ticket/501)

-   **[sql]**设置为 0 时，case 语句的“else\_”参数现在可以正常工作。[¶](#change-d3cf951f12ffc0a70ad1ada85b66a0a6)

### MySQL 的[¶ T0\>](#change-0.3.6-mysql "Permalink to this headline")

-   **[mysql]**为 MSString 添加了一个 catchall \*\*
    kwargs，以帮助反映不明显的类型（如 MS
    4.0 中的“varchar()binary”）[¶](#change-f0982bef56faed4137f772fe21cd4c31)

-   **[mysql]**添加了明确的 MSTimeStamp 类型，它在使用 types.TIMESTAMP 时生效。[¶](#change-1af85a8922781c43c7653e350c30801f)

### 预言[¶ T0\>](#change-0.3.6-oracle "Permalink to this headline")

-   **[oracle]**对于任何大小的输入都有二进制工作！cx\_oracle 工作正常，这是我的错，因为 BINARY 被传递，而不是 BLOPS
    setinputsizes（单元测试甚至没有设置输入大小）。[¶](#change-1de005425b678cd46ecc85ed5837c9c7)

-   **[oracle]**也修正了 CLOB 读/写在一个单独的变更集上。[¶](#change-12bd1d4f70a00eb5aa27999038a0d684)

-   **[oracle]**对于 Oracle 来说，auto\_setinputsizes 默认为 True，它会错误地传播错误类型。[¶](#change-22b00f0def3ec2ee49bb7d7a5b878466)

### 杂项[¶ T0\>](#change-0.3.6-misc "Permalink to this headline")

-   **[extensions]**options() method on SelectResults now implemented
    “generatively” like the rest of the SelectResults methods.
    但是你现在要使用 Query。[¶](#change-898f3d31d769657a997316a0a2a1b0ac)

    参考文献：[＃472](http://www.sqlalchemy.org/trac/ticket/472)

-   **[extensions]**
    query()方法由 assignmapper 添加。这有助于导航到 Query 上的所有新生成方法。[¶](#change-1eab2a69f89dd1f24faab811e0b58da3)

-   **[ms-sql]**

    在 DATE 列类型中删除秒输入（可能
    :   应该删除时间）

    [¶](#change-b87c523c857426c8d8b677b3058f15b5)

-   **[ms-sql]**浮点字段中的空值不再引发错误[¶](#change-77ff33ca3510c4330712ef7ecea18a8d)

-   **[ms-sql]**带 OFFSET 的 LIMIT 现在引发错误（MS-SQL 没有 OFFSET 支持）[¶](#change-542131c8c49c9372085c52a8c0cb56db)

-   **[ms-sql]**added an facility to use the MSSQL type VARCHAR(max)
    instead of TEXT for large unsized string fields.
    使用新的“text\_as\_varchar”将其打开。[¶](#change-92fb4300cf566200775defe777003a51)

    参考文献：[＃509](http://www.sqlalchemy.org/trac/ticket/509)

-   **[ms-sql]**现在在子查询中剥离了没有 LIMIT 的 ORDER
    BY 子句，因为 MS-SQL 禁止使用[¶](#change-91f921f0eaffcbb7dcbb4e655c3787de)

-   **[ms-sql]**cleanup of module importing code; specifiable DB-API
    module; more explicit ordering of module
    preferences.[¶](#change-4ac23e6c9087d3b35a82c00543826730)

    参考文献：[＃480](http://www.sqlalchemy.org/trac/ticket/480)

0.3.5 [¶ T0\>](#change-0.3.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2007 年 2 月 22 日

### ORM [¶ T0\>](#change-0.3.5-orm "Permalink to this headline")

-   **[orm]
    [bugs]**另一个重构关系计算。允许更准确的 ORM 行为与映射器之间的/到/之间的关系，特别是多态映射器，以及它们与 Query，SelectResults 的用法。门票包括,null,null,
    [¶](#change-8632b00faff5848753f92a330f517c03)

    References: [\#441](http://www.sqlalchemy.org/trac/ticket/441),
    [\#448](http://www.sqlalchemy.org/trac/ticket/448),
    [\#439](http://www.sqlalchemy.org/trac/ticket/439)

-   **[orm]
    [bugs]**删除了在类上指定自定义集合的弃用方法；你现在必须使用“collection\_class”选项。当人们使用 assign\_mapper()时，旧的方式开始产生冲突，现在它将“options”方法与名为“options”的关系相结合。（关系优先于 monkeypatched
    assign\_mapper 方法）。[¶](#change-420a8dde82328a1c84d68b07f0f008e2)

-   **[orm] [bugs]**extension() query option propagates to
    Mapper.\_instance() method so that all loading-related methods get
    called[¶](#change-b4ea85a697ce2e8a5476e0447b77ccf5)

    参考文献：[＃454](http://www.sqlalchemy.org/trac/ticket/454)

-   **[orm]
    [bugs]**如果没有为该关系返回的行，那么与继承映射器的渴望关系不会失败。[¶](#change-a75844e9e51b998af08e42d79b17d007)

-   **[orm]
    [bugs]**渴望的关系加载错误修复了对多个后代类的渴望关系[¶](#change-ac80398579a4fcbae21783cc62160e08)

    参考文献：[＃486](http://www.sqlalchemy.org/trac/ticket/486)

-   **[orm] [bugs]**修复非常大的拓扑排序，在 gmail
    [¶](#change-c165d9646437c3f933401899647483cb)处礼貌地使用 ants.aasma

    参考文献：[＃423](http://www.sqlalchemy.org/trac/ticket/423)

-   **[orm] [bugs]**eager loading is slightly more strict about
    detecting “self-referential” relationships, specifically between
    polymorphic mappers.
    这会导致延迟加载的“急切降级”。[¶](#change-39ce034d909d6179f0e57da79c888648)

-   **[orm]
    [bugs]**改进了对嵌入到 query.select()的“where”标准中的复杂查询的支持[¶](#change-77cfca11a557e706eafddf5289843a1a)

    参考文献：[＃449](http://www.sqlalchemy.org/trac/ticket/449)

-   **[orm]
    [bugs]**映​​射器选项（如 eagerload()，lazyload()，deferred()）可用于“synonym()”关系[¶](#change-a86a3aad19cf61adc26984764ce96a8b)

    参考文献：[＃485](http://www.sqlalchemy.org/trac/ticket/485)

-   **[orm]
    [bugs]**修正了级联操作错误地在级联中包含已删除集合项的错误[¶](#change-b8e4711961e2f380e6a7714230498042)

    参考文献：[＃445](http://www.sqlalchemy.org/trac/ticket/445)

-   **[orm]
    [bugs]**当一对多子项移动到单个工作单元中的新父项时，固定关系删除错误[¶](#change-22e5b7ae7b767a70ea7e0f53ad7e8248)

    参考文献：[＃478](http://www.sqlalchemy.org/trac/ticket/478)

-   **[orm] [bugs]**fixed relationship deletion error where parent/child
    with a single column as PK/FK on the child would raise a “blank out
    the primary key” error, if manually deleted or “delete” cascade
    without “delete-orphan” was
    used[¶](#change-226133d12414c7bceb0d870564d2db9e)

-   **[orm] [bugs]**修复延迟，以便只设置 PK
    col 属性时，不会错误地发生加载操作[¶](#change-559fd083469a062e02481918053495a7)

-   **[orm]
    [enhancements]**实现了映射器的 foreign\_keys 参数。与 primaryjoin /
    secondaryjoin 参数一起使用以指定/覆盖在 Table 实例上定义的外键。[¶](#change-6c4ac23619895aa1814ccc031d40da8a)

    参考文献：[＃385](http://www.sqlalchemy.org/trac/ticket/385)

-   **[orm] [enhancements]**
    contains\_eager（'foo'）自动暗示 eagerload（'foo'）[¶](#change-0755a972913cdf4f3d3ea28113aad132)

-   **[orm]
    [enhancements]**向 contains\_eager()添加了“别名”参数。用它来指定查询中用于急切加载的子项目的别名的字符串名称或 Alias 实例。比“装饰者”更容易使用[¶](#change-9559eca8c71abf14afd98ee3ccfd4f01)

-   **[orm]
    [enhancements]**添加了“contains\_alias()”选项，用于映射到映射表的别名的结果集[¶](#change-290a67bd31b7240bb829d5f3a1a8b913)

-   **[orm]
    [enhancements]**增加了对“py2.5”的支持，以及“带有 SessionTransaction
    [的语句](#change-4df85d62086609340f9ec07957b97137)

    参考文献：[＃468](http://www.sqlalchemy.org/trac/ticket/468)

### SQL [¶ T0\>](#change-0.3.5-sql "Permalink to this headline")

-   **[sql]**不管标识符的大小，“case\_sensitive”的值现在默认为 True，除非专门设置为 False。这是因为该对象可能被标记为包含混合大小写的其他内容，并且支持“case\_sensitive
    =
    False”会打破该情况。在使用标签和“假”列对象时引用的其他修正[¶](#change-0fe6675045936336cf076722fc9f4258)

-   **[sql]**added a “supports\_execution()” method to ClauseElement, so
    that individual kinds of clauses can express if they are appropriate
    for executing...such as, you can execute a “select”, but not a
    “Table” or a “Join”.[¶](#change-6c984550b02caf3742ce38d0ea98e80f)

-   **[sql]**固定参数传递给引擎上的直接文本 execute()，连接。可以处理\*
    args 或位置列表实例，\*\*
    kwargs 或 dict 实例，用于指定参数，或列表或调用 executemany()的列表或字典。[¶](#change-468f50da50e57a2dec8feb5e1ee1d75f)

-   **[sql]**小修复 BoundMetaData 以接受 unicode 或字符串 URL
    [¶](#change-799305b1c45d8b2c0b35daf24d651579)

-   **[sql]**在 gmail
    [¶](#change-098b0d8af7d1d8c4ac68ce0f0d1ab760)上修复了名为 PrimaryKeyConstraint 的代理礼让 andrija

    参考文献：[＃466](http://www.sqlalchemy.org/trac/ticket/466)

-   **[sql]**在列[¶](#change-70b974d0c4113b161566331bfc78053f)上固定生成 CHECK 约束

    参考文献：[＃464](http://www.sqlalchemy.org/trac/ticket/464)

-   **[sql]**修复 tometadata()操作以在列和表级别传播约束[¶](#change-d49ca559d4c734d1aaa61ba5a98e8a44)

### MySQL 的[¶ T0\>](#change-0.3.5-mysql "Permalink to this headline")

-   **[mysql]**修复可能返回 array()类型为“show variables
    like”语句的旧数据库的反射[¶](#change-23cbc502382175b57e3d21030a2373c2)

### MSSQL [¶ T0\>](#change-0.3.5-mssql "Permalink to this headline")

-   **[mssql]**初步支持 pyodbc（Yay！）[¶](#change-2c2ff52404aa9423f3b197ef8d064c57)

    参考文献：[＃419](http://www.sqlalchemy.org/trac/ticket/419)

-   **[mssql]**更好地支持添加的 NVARCHAR 类型[¶](#change-7e0d0b6aa2b56dd8a2643a2a996c1ce6)

    参考文献：[＃298](http://www.sqlalchemy.org/trac/ticket/298)

-   **[mssql]**修复 pymssql 上的提交逻辑[¶](#change-5456de0e05ace2611637223ef9c3b1a3)

-   **[mssql]**使用模式[修复 query.get()¶](#change-dd705f65a8f579d9f21e357b630ce0e1)

    参考文献：[＃456](http://www.sqlalchemy.org/trac/ticket/456)

-   **[mssql]**修复了非整数关系[¶](#change-911cdebc2d34a378435f400bf0cf630e)

    参考文献：[＃473](http://www.sqlalchemy.org/trac/ticket/473)

-   **[mssql]**现在可在运行时选择 DB-API 模块[¶](#change-539d4ad681f7456880dabe1620b68588)

    参考文献：[＃419](http://www.sqlalchemy.org/trac/ticket/419)

-   **[mssql] [415] [tickets:422]
    [481]**现在通过了更多的单元测试[¶](#change-59dc7293d796646a217909587ba56fb7)

-   **[mssql]**更好的与 ANSI 函数的单元测试兼容[¶](#change-9f0b045815840276afd66940cbba759c)

    参考文献：[＃479](http://www.sqlalchemy.org/trac/ticket/479)

-   **[mssql]**改进了对带有自动插入的隐式序列 PK 列的支持[¶](#change-381a1076dd1ae05a9d9d968cdf1c5bc9)

    参考文献：[＃415](http://www.sqlalchemy.org/trac/ticket/415)

-   **[mssql]**修复了 adodbapi
    [中的空密码¶](#change-dcdda808c45d24c958d8be769f83003f)

    参考文献：[＃371](http://www.sqlalchemy.org/trac/ticket/371)

-   **[mssql]**修复了使用 pyodbc
    [¶](#change-1075fe6db448bd584e19ab492e5f8c5c)的单元测试

    参考文献：[＃481](http://www.sqlalchemy.org/trac/ticket/481)

-   **[mssql]**修复 db-url 查询中的 auto\_identity\_insert
    [¶](#change-5bdb627a7d2ed7ec5bc84c7ebf111216)

-   **[mssql]**将 query\_timeout 添加到 db-url 查询参数中。目前仅适用于 pymssql
    [¶](#change-b8f7e80d560caa5ae3aec32c6e922ef6)

-   使用 pymssql 0.8.0（现在是 LGPL）测试**[mssql]**
    [¶](#change-2cea7ef341a84d5cc0ea53fd071ce1af)

### 预言[¶ T0\>](#change-0.3.5-oracle "Permalink to this headline")

-   **[oracle]**when returning “rowid” as the ORDER BY column or in use
    with ROW\_NUMBER OVER, oracle dialect checks the selectable its
    being applied to and will switch to table PK if not applicable, i.e.
    for a UNION. 检查 DISTINCT，GROUP
    BY（其他那些 rowid 无效的地方）仍然是 TODO。允许多态映射功能。[¶](#change-f2964e13050167fa913d5346579ed93a)

    参考文献：[＃436](http://www.sqlalchemy.org/trac/ticket/436)

-   **[oracle]**sequences on a non-pk column will properly fire off on
    INSERT[¶](#change-997cdb0c8e4db76469d84ce1e36ff870)

-   **[oracle]**增加了 PrefetchingResultProxy 支持，当它们被认为存在时预取 LOB 列，修复[¶](#change-41b33afb60cf82b8b6a4a0bb859562bf)

    参考文献：[＃435](http://www.sqlalchemy.org/trac/ticket/435)

-   **[oracle]**实现了基于同义词的表反映，包括跨越 dblinks
    [¶](#change-a87a4c61e30aa01276449a37779f7083)

    参考文献：[＃379](http://www.sqlalchemy.org/trac/ticket/379)

-   **[oracle]**当相关表由于某些权限错误而无法反映时，会发出日志警告[¶](#change-b8639b7a31e537e7f11dcd8f241550b6)

    参考文献：[＃363](http://www.sqlalchemy.org/trac/ticket/363)

### 杂项[¶ T0\>](#change-0.3.5-misc "Permalink to this headline")

-   **[postgres]**更好地反映替代模式表的序列[¶](#change-cc97a0bde59a0e25d2d0180cee1209a0)

    参考文献：[＃442](http://www.sqlalchemy.org/trac/ticket/442)

-   **[postgres]**sequences on a non-pk column will properly fire off on
    INSERT[¶](#change-997cdb0c8e4db76469d84ce1e36ff870)

-   **[postgres]**添加了 PGInterval 类型，PGInet 类型[¶](#change-848a61af4172ae1b5f0fc0247de36987)

    参考文献：[＃460](http://www.sqlalchemy.org/trac/ticket/460)，[＃444](http://www.sqlalchemy.org/trac/ticket/444)

-   **[extensions]**在 SelectResults 中添加了 distinct()方法。通常应该只在使用 count()时有所作为。[¶](#change-bd2bb531eaffdeab9654a4cd07ef2c2b)

-   **[extensions]**在 SelectResults 中添加了 options()方法，相当于 query.options()[¶](#change-e49cd2a7ca945f2421ae6902f52f8f37)

    参考文献：[＃472](http://www.sqlalchemy.org/trac/ticket/472)

-   **[extensions]**将可选的\_\_table\_opts\_\_字典添加到 ActiveMapper，将发送 kw 选项给表对象[¶](#change-cdde06072236d420f2b8e3603362354e)

    参考文献：[＃462](http://www.sqlalchemy.org/trac/ticket/462)

-   **[extensions]**将 selectfirst()，selectfirst\_by()添加到 assign\_mapper
    [¶](#change-a43a8ee036b96770b37d4e02ab37b4c0)

    参考文献：[＃467](http://www.sqlalchemy.org/trac/ticket/467)

0.3.4 [¶ T0\>](#change-0.3.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2007 年 1 月 23 日

### 一般[¶ T0\>](#change-0.3.4-general "Permalink to this headline")

-   **[general]**全球“保险” -
    \>“确保”更改。在美国英语中，“保险”实际上在很大程度上与“保证”（字典所说的）可以互换，所以我不是完全不识字的，但它确实是次优的，以确保它不含糊。[\<
    / T0\>](#change-ea7ee482db28ede59ac4bcfe7508bb68)

### ORM [¶ T0\>](#change-0.3.4-orm "Permalink to this headline")

-   **[orm]**poked the first hole in the can of worms: saying
    query.select\_by(somerelationname=someinstance) will create the join
    of the primary key columns represented by “somerelationname“‘s
    mapper to the actual primary key in
    “someinstance”.[¶](#change-3d028e23313c343b88f683148079f6d8)

-   **[orm]**reworked how relations interact with “polymorphic” mappers,
    i.e. mappers that have a select\_table as well as polymorphic flags.
    更好地确定正确的连接条件，与用户定义的连接条件进行交互以及支持自引用多态映射器。[¶](#change-5601e1cae87763b3397a1dff4dc3479c)

-   **[orm]**related to polymorphic mapping relations, some deeper error
    checking when compiling relations, to detect an ambiguous
    “primaryjoin” in the case that both sides of the relationship have
    foreign key references in the primary join condition.
    也收紧了用于定位“关系方向”的条件，将关系的“外键”与“主连接”相关联[¶](#change-77a27e5fc8a0403c05553cd6268b57ce)

-   **[orm]**a little bit of improvement to the concept of a “concrete”
    inheritance mapping, though that concept is not well fleshed out yet
    (added test case to support concrete mappers on top of a polymorphic
    base).[¶](#change-b68e439ba854a97afc57d071074809ec)

-   **[orm]**固定在 synonym()上的“proxy =
    True”行为[¶](#change-fc43ebe81ca938a541f0089c23bfb7a8)

-   **[orm]**修正了删除孤儿基本上无法与多对多关系一起工作的问题，backref 存在通常隐藏了症状[¶](#change-351dd3d3f2b53af4c434ce66c226cef5)

    参考文献：[＃427](http://www.sqlalchemy.org/trac/ticket/427)

-   **[orm]**在映射器编译步骤中添加了一个互斥体。虽然不愿意向 SA 添加任何线程化的任何东西，但是这是一个真正需要的地方，因为映射器通常是“全局的”，虽然它们的状态在正常操作期间不会改变，但初始编译步骤会显着修改内部状态，这一步通常不是在模块级的初始化时间（除非你调用 compile()），而是在第一次请求时[¶](#change-231c94f2c6414edd8ef94f7de383d349)

-   **[orm]**basic idea of “session.merge()” actually implemented.
    需要更多的测试。[¶](#change-40191965cf8a1fffbd5f3f7c476c442e)

-   **[orm]**添加了“compile\_mappers()”函数作为编译所有映射器的快捷方式[¶](#change-1fcc21636195b3b7a6c4751ded7aacc7)

-   **[orm]**修复 MapperExtension
    create\_instance，以便 entity\_name 与新实例正确关联[¶](#change-a564633ea1853007aeaac37573a81ee6)

-   **[orm]**speed enhancements to ORM object instantiation, eager
    loading of rows[¶](#change-9eccc99856ce597d36eae3266f7614b6)

-   **[orm]**invalid options sent to ‘cascade’ string will raise an
    exception[¶](#change-dd4031a82befed9119e377543328f8c0)

    参考文献：[＃406](http://www.sqlalchemy.org/trac/ticket/406)

-   **[orm]**修复了映射器刷新/过期中的错误，因此渴望的加载器没有正确地重新填充项目列表[¶](#change-32423083b9cdff2c1cfd63c406fe3d93)

    参考文献：[＃407](http://www.sqlalchemy.org/trac/ticket/407)

-   **[orm]**修复 post\_update 以确保即使对于非插入/删除方案也更新行[¶](#change-4c9bf70f421052228204cfd54e3196b0)

    参考文献：[＃413](http://www.sqlalchemy.org/trac/ticket/413)

-   **[orm]**如果实际尝试修改实体上的主键值然后将其刷新，则会添加错误消息[¶](#change-003b8a29b4cd8dc41607198658523317)

    参考文献：[＃412](http://www.sqlalchemy.org/trac/ticket/412)

### SQL [¶ T0\>](#change-0.3.4-sql "Permalink to this headline")

-   **[sql]**在 ResultProxy 中添加了“fetchmany()”支持[¶](#change-e485ef1aa25a4c1e54a8d7a9afa8749e)

-   **[sql]**增加了对列“key”属性的支持，以便在行[] /
    row 中使用。[¶](#change-594afe1f5a9a758e9428229d6e156f32)

-   **[sql]**将“BooleanExpression”从“BinaryExpression”改为子类，以便布尔表达式也可以遵循列子句行为（即 label()等）。[¶](#change-36de194453369736e2c6d36951589a57)

-   **[sql]**trailing underscores are trimmed from func. calls, such as
    func.if\_()[¶](#change-fd647f39d01615d6a2c872791f220b3d)

-   **[sql]**fix to correlation of subqueries when the column list of
    the select statement is constructed with individual calls to
    append\_column(); this fixes an ORM bug whereby nested select
    statements were not getting correlated with the main select
    generated by the Query
    object.[¶](#change-7c82a8fe27927597ae6beb2b46eaaa4e)

-   **[sql]**另一个解决子查询相关性的问题，以便只有一个 FROM 元素的子查询将*不*关联该单个元素，因为查询中至少需要一个 FROM 元素[¶
    T3\>](#change-9e9c62f87ee18fefb379e8a4754ae2f8)

-   **[sql]**默认的“时区”设置现在为 False。这对应于 Python 的日期时间行为以及 Postgres 的时间戳/时间类型（这是目前唯一的时区敏感方言）[¶](#change-5f52342a7f4ca2f210861d452dec505a)

    参考文献：[＃414](http://www.sqlalchemy.org/trac/ticket/414)

-   **[sql]**the “op()” function is now treated as an “operation”,
    rather than a “comparison”.
    不同之处在于，一个操作产生一个 BinaryExpression，从中可以进行进一步的操作，而比较产生更具限制性的 BooleanExpression
    [¶](#change-66229214f0f9e03fc7dee45d95c8e67c)

-   **[sql]**trying to redefine a reflected primary key column as
    non-primary key raises an
    error[¶](#change-d41715babcf6b70d6f88adf677313ea8)

-   **[sql]**类型的系统稍作修改以支持 TypeDecorator，可以被方言覆盖（好吧，这不是很清楚，它允许下面的 mssql 调整）[¶](#change-a8e520f2f077ca90381491c36493fe9d)

### MySQL 的[¶ T0\>](#change-0.3.4-mysql "Permalink to this headline")

-   **[mysql]**mysql is inconsistent with what kinds of quotes it uses
    in foreign keys during a SHOW CREATE TABLE, reflection updated to
    accommodate for all three
    styles[¶](#change-5398fcc75e1c898762a840d5476e9802)

    参考文献：[＃420](http://www.sqlalchemy.org/trac/ticket/420)

-   **[mysql]**mysql table create options work on a generic passthru
    now, i.e. Table(..., mysql\_engine=’InnoDB’,
    mysql\_collate=”latin1\_german2\_ci”, mysql\_auto\_increment=”5”,
    mysql\_...), helps[¶](#change-93636efc4d02d5b5e25f763da5f6dbb6)

    参考文献：[＃418](http://www.sqlalchemy.org/trac/ticket/418)

### MSSQL [¶ T0\>](#change-0.3.4-mssql "Permalink to this headline")

-   **[mssql]**添加了一个 NVarchar 类型（产生 NVARCHAR），也提供了 MSUnicode，它为 NVarchar 提供了 Unicode 转换，而不管方言 convert\_unicode 的设置。[¶](#change-71800340e8b8eaf7f5bbfeb1bb7fa8fa)

### 预言[¶ T0\>](#change-0.3.4-oracle "Permalink to this headline")

-   **[oracle]***slight* support for binary, but still need to figure
    out how to insert reasonably large values (over 4K).
    需要 auto\_setinputsizes =
    True 发送到 create\_engine()，行必须单独完全提取等。[¶](#change-7e37b511a75dea4c081f6e861d2577d9)

### 火鸟[¶ T0\>](#change-0.3.4-firebird "Permalink to this headline")

-   **[firebird]**创建约束的顺序首先在所有其他约束之前放置主键；
    firebird 需要，对其他人来说不是一个坏主意[¶](#change-f5553b26f95beaede1e3993d72351403)

    参考文献：[＃408](http://www.sqlalchemy.org/trac/ticket/408)

-   **[firebird]**
    Firebird 修复自动加载多字段外键[¶](#change-7d0941d7be1eff286a79a26140dbec40)

    参考文献：[＃409](http://www.sqlalchemy.org/trac/ticket/409)

-   **[firebird]** Firebird
    NUMERIC 类型正确处理一个没有精度的类型[¶](#change-1dd0655cdeb215bba70f97a6144d2d79)

    参考文献：[＃409](http://www.sqlalchemy.org/trac/ticket/409)

### 杂项[¶ T0\>](#change-0.3.4-misc "Permalink to this headline")

-   **[postgres]**修复表格的初始 checkfirst 以将当前模式考虑进去[¶](#change-fa53dae6bfd7b7e8b384d216ee8ba515)

    参考文献：[＃424](http://www.sqlalchemy.org/trac/ticket/424)

-   **[postgres]** postgres 有一个可选的“server\_side\_cursors =
    True”标志，它将使用服务器端游标。这些仅适用于获取部分结果，并且对于处理非常大的无限结果集是必需的。虽然我们希望这是默认行为，但不同的环境似乎有不同的结果，原因并未被隔离，所以我们现在默认关闭此功能。最近在 psycopg 邮件列表中发现了一个明显未公开的 psycopg2 行为。[¶](#change-1cd224ad7dc6c4a22f02a844273d939f)

-   **[postgres]**使用 PGBigInteger /
    autoincrement 添加了对 Postgres 表的“BIGSERIAL”支持[¶](#change-6f6b781d6e5399b6526088cc619cd843)

-   **[postgres]**修复了 postgres 反射，以便在模式名称存在时更好地处理；感谢 jason（at）ncsmags.com
    [¶](#change-61cfe585aaae9ecddaff0f20996405f7)

    参考文献：[＃402](http://www.sqlalchemy.org/trac/ticket/402)

-   **[extensions]**在 assign\_mapper 中添加了“validate =
    False”参数，如果 True 将确保只映射的属性被命名为[¶](#change-d06299a138c88ba57c7c327e826b3f81)

    参考文献：[＃426](http://www.sqlalchemy.org/trac/ticket/426)

-   **[extensions]**assign\_mapper gets “options”, “instances” functions
    added (i.e.
    MyClass.instances())[¶](#change-7e48f7fba0d3f1b5bad84893f66dc9f4)

0.3.3 [¶ T0\>](#change-0.3.3 "Permalink to this headline")
----------------------------------------------------------

发布：2006 年 12 月 15 日星期五

-   基于字符串的 FROM 子句 fixed，即 select（...，from\_obj =
    [“sometext”]）[¶](#change-5032f5e367ae143bbec87043ab8fcf11)

-   修复了 passive\_deletes 标志，lazy =
    None（noload）标志[¶](#change-a496d8fae942c14d4523057bd979019c)

-   添加了用于处理大型集合的示例/ docs
    [¶](#change-30a2c69a9decacc368b9a7b6779980ec)

-   added object\_session() method to sqlalchemy
    namespace[¶](#change-cc99c5f52ba79f63b5f7b50754788b0a)

-   fixed QueuePool bug whereby its better able to reconnect to a
    database that was not reachable (thanks to SÃ©bastien Lelong), also
    fixed dispose() method[¶](#change-80533f7c200e079d90597f6266ff66d5)

-   使 MySQL 行计数正常工作的修补程序！[¶](#change-d1570d0ab054957641111d7e277d03b4)

    参考文献：[＃396](http://www.sqlalchemy.org/trac/ticket/396)

-   修复 2006/2014 错误的 MySQL
    catch，以正确地重新引发 OperationalError 异常[¶](#change-2cadf5490827d447b1d4830a90b41caf)

0.3.2 [¶ T0\>](#change-0.3.2 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 12 月 10 日

-   修正了主要连接池错误。修复了 MySQL 不同步错误，还会阻止事务在所有 DB 中意外回滚[¶](#change-19098e0e6eed7c931125d7e25d812756)

    参考文献：[＃387](http://www.sqlalchemy.org/trac/ticket/387)

-   主要速度增强与 0.3.1 相比，使速度回到 0.2.8 级[¶](#change-278ff1b4865a34c36458359bdba8e20e)

-   有条件地执行了数十个调试日志调用，这些调用耗时耗力以生成日志消息[¶](#change-da5c4522ae9018928c5a69dbe99fa7f3)

-   fixed bug in cascade rules whereby the entire object graph could be
    unnecessarily cascaded on the save/update
    cascade[¶](#change-47d47dccb2480566207c5fe438fcf435)

-   属性模块[中的各种加速](#change-d1b12f9efbb4d033df0a742d87c94ec6)

-   Session 中的身份映射默认为*不再弱引用*。要使其引用较弱，请使用 create\_session（weak\_identity\_map
    = True）修复[¶](#change-3c38a41db88ddb08db4d6f9d55194829)

    参考文献：[＃388](http://www.sqlalchemy.org/trac/ticket/388)

-   MySQL detects errors 2006 (server has gone away) and 2014 (commands
    out of sync) and invalidates the connection on which it
    occurred.[¶](#change-79647e60f1175354aca8ce75bc921e74)

-   MySQL 布尔类型修正：[¶](#change-35fdc30fd93b0c3e1b37402908f76fd2)

    参考文献：[＃307](http://www.sqlalchemy.org/trac/ticket/307)

-   postgres 反射修复：[¶](#change-1ee7b209987629c6f339a0dcc1d703a0)

    参考文献：[＃382](http://www.sqlalchemy.org/trac/ticket/382)，[＃349](http://www.sqlalchemy.org/trac/ticket/349)

-   为 EXCEPT，INTERSECT，EXCEPT ALL，INTERSECT
    ALL 添加了关键字[¶](#change-fd7e2e948165b16a849ce49011d87d21)

    参考文献：[＃247](http://www.sqlalchemy.org/trac/ticket/247)

-   assignmapper 扩展中的 assign\_mapper 返回创建的映射器[¶](#change-c52f4bfa0a28896df33156b19ff3ca89)

    参考文献：[＃2110](http://www.sqlalchemy.org/trac/ticket/2110)

-   added label() function to Select class, when scalar=True is used to
    create a scalar subquery i.e. “select x, y, (select max(foo) from
    table) AS foomax from
    table”[¶](#change-f6551d6f54899ff8108cbbbd26e5018c)

-   将 onUpdate 和 ondelete 关键字参数添加到 ForeignKey；如果存在，则传播到底层的 ForeignKeyConstraint。（但不要向另一个方向传播）[¶](#change-9f53e9bcf5cece6ce6d03fb58eda20ad)

-   修复 session.update()以保留传入对象的“脏”状态[¶](#change-8372c4057499c22e46cf0bcc739b695d)

-   sending a selectable to an IN via the in\_() function no longer
    creates a “union” out of multiple selects; only one selectable to a
    the in\_() function is allowed now (make a union yourself if union
    is needed)[¶](#change-a1e2bb60c3cd464a48cdfbff5d33f9c2)

-   改进了对通过 cascade
    =“none”禁用保存更新级联的支持。[¶](#change-e009ef228c4e1a8a3e92bc728fbc438a)

-   在 relation()中添加了“remote\_side”参数，仅用于自引用映射器来强制父/子关系的方向。替换“切换”方向的“外键”参数的用法。“foreignkey”参数在所有用途上都被弃用，并最终被替换为专用于映射器上的 ForeignKey 规范的参数。[¶](#change-dcd5c21c1c376d26e9907a451ceb1ad7)

0.3.1 [¶ T0\>](#change-0.3.1 "Permalink to this headline")
----------------------------------------------------------

发布时间：2006 年 11 月 13 日

### ORM [¶ T0\>](#change-0.3.1-orm "Permalink to this headline")

-   **[orm]**the “delete” cascade will load in all child objects, if
    they were not loaded already.
    这可以通过在关系()上设置 passive\_deletes =
    True 来关闭（即旧行为）。[¶](#change-0af98bf52dddbf728106569a225ffa27)

-   **[orm]**调整重新生成的热切查询生成不会在循环加载关系中失败（如 backrefs）[¶](#change-a23f03ece2ae82e1264ecacd54d01e12)

-   **[orm]**修正了在生成 LIMIT 查询时 eagerload()（也不是 lazyload()）选项没有正确指示查询是否使用“嵌套”的问题。[T2\>](#change-201da868406f1523d1d4d0051049fbb3)

-   **[orm]**fixed bug in circular dependency sorting at flush time; if
    object A contained a cyclical many-to-one relationship to object B,
    and object B was just attached to object A, *but* object B itself
    wasn’t changed, the many-to-one synchronize of B’s primary key
    attribute to A’s foreign key attribute wouldn’t
    occur.[¶](#change-ed4601755ccc028c0cda37fd8bc2343f)

    参考文献：[＃360](http://www.sqlalchemy.org/trac/ticket/360)

-   **[orm]**对 query.count 实现 from\_obj 参数，改进了 selectresults 的 count 函数[¶](#change-443db0da68194af1c486a31424626acc)

    参考文献：[＃325](http://www.sqlalchemy.org/trac/ticket/325)

-   **[orm]**added an assertion within the “cascade” step of ORM
    relationships to check that the class of object attached to a parent
    object is appropriate (i.e. if A.items stores B objects, raise an
    error if a C is appended to
    A.items)[¶](#change-6c3fe5348af079926eefaa5fe198132a)

-   **[orm]**新的扩展 sqlalchemy.ext.associationproxy 提供了透明的“关联对象”映射。新的示例 examples
    / association /
    proxied\_association.py 说明。[¶](#change-3c54016dd3eb6240c61bdf6630fb6ba2)

-   **[orm]**改进单个表继承以加载目标类下的完整层次结构[¶](#change-2352347ba67e763e63b5ab5fee615fd0)

-   **[orm]**修复了拓扑排序中的细微情况，其中节点可能出现两次，[¶](#change-7c2c83368bc653695d50bf41a32ba122)

    参考文献：[＃362](http://www.sqlalchemy.org/trac/ticket/362)

-   **[orm]**针对[¶](#change-21099b0b4cfd087d7544c0d5b29f20ad)的拓扑排序，重构的额外返工

    参考文献：[＃365](http://www.sqlalchemy.org/trac/ticket/365)

-   **[orm]**可以在多个父类上设置特定类型的“delete-orphan”；只有当它没有附加到*那些父母的*
    [¶](#change-c31972da5ddfab970d95b975b0de0f13)时，该实例才是“孤儿”

### 杂项[¶ T0\>](#change-0.3.1-misc "Permalink to this headline")

-   **[engine/pool]**一些新的池实用程序类，更新的文档[¶](#change-ae1c652969370d12b5391b3c25bc311b)

-   **[engine/pool]**“use\_threadlocal” on Pool defaults to False (same
    as create\_engine)[¶](#change-40bd8ced1a542293a3bee2e4e993b319)

-   **[engine/pool]**固定直接执行编译对象[¶](#change-d05d5b0d7cbdb72d11dda30dba80e253)

-   **[engine/pool]** create\_engine()返工严格限制传入的\*\*
    kwargs。所有关键字参数都必须由方言，连接池和引擎构造函数之一使用，否则将抛出一个 TypeError，它描述与所选 dialect
    / pool /
    engine 配置有关的全套无效 kwargs。[T0\>](#change-c6dec82e7a9a007a628f587642c8adc7)

-   **[databases/types]**
    MySQL 在“describe”上捕获异常并报告为 NoSuchTableError
    [¶](#change-95a6b3fd67d1f8a92d5fc7d3c4a72cd3)

-   **[databases/types]**进一步修复了 sqlite 布尔错误，并未作为默认工作[¶](#change-01a55d6e648e86ae237b8c9014765637)

-   当使用模式时，**[databases/types]**修复 postgres 序列引用[¶](#change-4990b03a3ffa7973be6eaf89b54a64c2)

0.3.0 [¶ T0\>](#change-0.3.0 "Permalink to this headline")
----------------------------------------------------------

发布于：2006 年 10 月 22 日

### 一般[¶ T0\>](#change-0.3.0-general "Permalink to this headline")

-   **[general]**logging is now implemented via standard python
    “logging” module.
    “回声”关键字参数仍然有效，但为其各自的类/实例设置/取消设置日志级别。通过在“sqlalchemy”名称空间中为记录器设置 INFO 和 DEBUG 级别，可以通过 Python
    API 直接控制所有日志记录。类级别日志记录在“sqlalchemy。。”下，在“sqlalchemy。。.0x
    ..＆lt； 00-FF\>”下面的实例级日志记录下。 T3\> T2\> T1\>
    T0\>测试套件包括独立于-verbose /
    -quiet 工作的“-log-info”和“-log-debug”参数。将记录添加到 orm 以允许跟踪映射器配置，行迭代。[¶](#change-af1703046aac222edc8054620ba72d5b)

-   **[general]**the documentation-generation system has been overhauled
    to be much simpler in design and more integrated with
    Markdown[¶](#change-5becb5a90dce00b288e48c42b5b11c91)

### ORM [¶ T0\>](#change-0.3.0-orm "Permalink to this headline")

-   **[orm]**attribute tracking modified to be more intelligent about
    detecting changes, particularly with mutable types.
    现在，TypeEngine 对象在定义如何比较两个标量实例方面扮演了更重要的角色，其中包括添加由 PickleType 实现的 MutableType 混合。工作单元现在将“脏”列表作为属性管理器检测到所有持久对象的表达式进行跟踪。固定的基本问题是检测 PickleType 对象上的更改，但也推广了类型处理和“修改”对象检查，使其更加完整和可扩展。[¶](#change-4d0f18a84af312791a640dd1de2ac5aa)

-   **[orm]**对“属性加载器”和“选项”体系结构进行了广泛的重构。ColumnProperty 和 PropertyLoader 通过可切换的“策略”定义它们的加载行为，MapperOptions 不再使用映射器/属性复制功能；它们在查询/实例时间通过 QueryContext 和 SelectionContext 对象传播。所有用于处理继承的映射器和属性的内部复制以及 options()都已被删除；映射器和属性的结构比以前简单得多，并且清楚地在新的“接口”模块中进行了布置。[¶](#change-b455e30f2020397a52b52dee6104b5c3)

-   **[orm]**related to the mapper/property overhaul, internal
    refactoring to mapper instances() method to use a SelectionContext
    object to track state during the operation. SLIGHT API
    BREAKAGE：由于更改，MapperExtension 上的 append\_result()和 populate\_instances()方法现在具有稍微不同的方法签名；希望这些方法还没有被广泛使用。[¶](#change-1119b49161e5498c6ab5268241c9bc68)

-   **[orm]**
    instances()方法现在移至 Query，向后兼容版本保留在 Mapper 上。[¶](#change-b9edae4ebe585fc03a2663daead0be3c)

-   **[orm]**added contains\_eager() MapperOption, used in conjunction
    with instances() to specify properties that should be eagerly loaded
    from the result set, using their plain column names by default, or
    translated given an custom row-translation
    function.[¶](#change-35f311fe6deb6c511ce9e34f3aba4864)

-   **[orm]**more rearrangements of unit-of-work commit scheme to better
    allow dependencies within circular flushes to work
    properly...updated task traversal/logging
    implementation[¶](#change-50bbbc3588a69af8445ccb96ccd2e5ce)

-   **[orm]**polymorphic mappers (i.e. using inheritance) now produces
    INSERT statements in order of tables across all inherited
    classes[¶](#change-cc6b22ffd1c978ed11157bf9e14e6394)

    参考文献：[＃321](http://www.sqlalchemy.org/trac/ticket/321)

-   **[orm]**added an automatic “row switch” feature to mapping, which
    will detect a pending instance/deleted instance pair with the same
    identity key and convert the INSERT/DELETE to a single
    UPDATE[¶](#change-69a48fb25de0e1cd620693a836968e3d)

-   **[orm]**“关联”映射简化为利用自动“行开关”功能[¶](#change-9741ba8323c434593dbd85ae32233bba)

-   **[orm]**“custom list classes” is now implemented via the
    “collection\_class” keyword argument to relation().
    旧的方式仍然有效，但不推荐使用[¶](#change-f970db37c47df342ea626e5d34c33557)

    参考文献：[＃212](http://www.sqlalchemy.org/trac/ticket/212)

-   **[orm]**将“viewonly”标志添加到 relation()，允许构造对 flush()过程没有影响的关系。[¶](#change-0b4f7934178b19d2f4198f972fa48af0)

-   **[orm]**在基本查询 select /
    get 函数中添加了“lockmode”参数，包括“with\_lockmode”函数以获取具有默认锁定模式的 Query 副本。将“read”/“update”参数转换为选择端的 for\_update 参数。[¶](#change-89e8bd4b5f78c821a2184eda9d0b4596)

    参考文献：[＃292](http://www.sqlalchemy.org/trac/ticket/292)

-   **[orm]**implemented “version check” logic in Query/Mapper, used
    when version\_id\_col is in effect and query.with\_lockmode() is
    used to get() an instance that’s already
    loaded[¶](#change-0e58e5ab6f48202b49a15d78dac03244)

-   **[orm]**
    post\_update 行为得到改善；在不更新太多行方面做得更好，只更新需要的列[¶](#change-db567762bd8f003f9bf446dc80e93356)

    参考文献：[＃208](http://www.sqlalchemy.org/trac/ticket/208)

-   **[orm]**adjustments to eager loading so that its “eager chain” is
    kept separate from the normal mapper setup, thereby preventing
    conflicts with lazy loader operation,
    fixes[¶](#change-ed17766eeb0f7e0ffae4b5a8d65e19ba)

    参考文献：[＃308](http://www.sqlalchemy.org/trac/ticket/308)

-   **[orm]**修复延迟群组加载[¶](#change-49870ec4b2e0423340358dea26b3babf)

-   **[orm]**
    session.flush()不会关闭它打开的连接[¶](#change-9b6964ae2926bcd79206eacf3b9f3cfd)

    参考文献：[＃346](http://www.sqlalchemy.org/trac/ticket/346)

-   **[orm]**向映射器添加了“batch =
    True”标志；如果为 False，则 save\_obj 将一次完全保存一个对象，包括调用 before\_XXXX 和 after\_XXXX
    [¶](#change-805e0f356e88803a0f83d386731283b0)

-   **[orm]**向 mapper 添加了“column\_prefix =
    None”参数；将给定的字符串（通常是'\_'）预加到从映射程序的表中自动设置的基于列的属性[¶](#change-f2876d14278453a3a9e07c35b3fc23d6)

-   **[orm]**specifying joins in the from\_obj argument of
    query.select() will replace the main table of the query, if the
    table is somewhere within the given from\_obj.
    这使得在查询中生成自定义连接和外连接成为可能，而不需要两次添加主表。[¶](#change-84a0aa83db4fbe7fa685c9586be1c4ec)

    参考文献：[＃315](http://www.sqlalchemy.org/trac/ticket/315)

-   **[orm]**调整 eagerloading 以更贴心地将其 LEFT OUTER
    JOIN 附加到给定的查询中，寻找可能已经设置好的自定义“FROM”子句。[¶](#change-ccb145193bd44d06f18079179309f197)

-   **[orm]**added join\_to and outerjoin\_to transformative methods to
    SelectResults, to build up join/outerjoin conditions based on
    property names.
    还添加了 select\_from 来显式设置 from\_obj 参数。[¶](#change-63a7d34aabebf51b4547b9939aee9ea7)

-   **[orm]**从映射器中移除了“is\_primary”标志。[¶](#change-c1c88b8cfd3e533c3299e6380b4c2363)

### SQL [¶ T0\>](#change-0.3.0-sql "Permalink to this headline")

-   **[sql] [construction]**改变了“for\_update”参数以接受 False / True
    /“nowait”和“read”，后两者仅由 Oracle 和 Mysql 解释[T2\>](#change-e5f40f680103943b465258a215ef6f9e)

    参考文献：[＃292](http://www.sqlalchemy.org/trac/ticket/292)

-   **[sql] [construction]**added extract() function to sql dialect
    (SELECT extract(field FROM
    expr))[¶](#change-3abbda64974ee3c2264a57b840bd8421)

-   **[sql] [construction]**
    BooleanExpression 包含新的“negate”参数，用于指定适当的否定运算符（如果有）。[¶](#change-121c9f650291edb4ca7b8ffa8139c66b)

-   **[sql] [construction]**calling a negation on an “IN” or “IS” clause
    will result in “NOT IN”, “IS NOT” (as opposed to NOT (x IN
    y)).[¶](#change-9350ceaebf6175edafc4765a8f79bd9b)

-   **[sql]
    [construction]**函数对象现在知道在 FROM 子句中要做什么。他们的行为应该是相同的，除了现在你还可以执行 select（['\*']，from\_obj
    =
    [func.my\_function()]）来从结果中获取多个列，甚至使用 sql.column()构造命名返回列[¶](#change-22c4e15de46bb1d96abbdf555f8dc4a7)

    参考文献：[＃172](http://www.sqlalchemy.org/trac/ticket/172)

### 架构[¶ T0\>](#change-0.3.0-schema "Permalink to this headline")

-   **[schema]**a fair amount of cleanup to the schema package, removal
    of ambiguous methods, methods that are no longer needed.
    限制使用略多，更强调明确性[¶](#change-4df510b9c3361af772c20d1ad5825ea4)

-   **[schema]**the “primary\_key” attribute of Table and other
    selectables becomes a setlike ColumnCollection object; is ordered
    but not numerically indexed. 可以通过 table1.primary\_key ==
    table2.primary\_key
    [¶](#change-7e3d79a0f25e4a5cfff24316d2cf0887)生成从相同基础表派生的两个 pks 之间的比较子句（即，例如两个 Alias 对象）

-   **[schema]**ForeignKey(Constraint) supports “use\_alter=True”, to
    create/drop a foreign key via ALTER.
    这允许建立循环外键关系。[¶](#change-1f5f61d9a455f45e8e7957b4a802259c)

-   **[schema]**append\_item() methods removed from Table and Column;
    preferably construct Table/Column/related objects inline, but if
    needed use append\_column(), append\_foreign\_key(),
    append\_constraint(),
    etc.[¶](#change-07dabb3b17789490c2f1f3c1325d7f94)

-   **[schema]**table.create() no longer returns the Table object,
    instead has no return value.
    通常的情况是表格是通过元数据创建的，这是可取的，因为它将处理表格依赖关系。[¶](#change-9297cc5781aef837ddcf8a66d489adac)

-   **[schema]**增加了 UniqueConstraint（进入表级），CheckConstraint（进入表级或列级）[¶](#change-96cef28bc60b163b11d7748202f7927d)

-   **[schema]**index=False/unique=True on Column now creates a
    UniqueConstraint, index=True/unique=False creates a plain Index,
    index=True/unique=True on Column creates a unique Index.
    'index'和'unique'关键字参数列现在只是布尔值；对于 explcit 名称和索引分组或者唯一约束，请明确使用 UniqueConstraint
    / Index 结构。[¶](#change-f11c7c40de054e42f985d34823335728)

-   **[schema]**在列中添加了 autoincrement = True；如果显式设置为 False
    [¶](#change-504cbc530860d0c4286f50b29cc1df63)，将禁止为 postgres /
    mysql / mssql 生成 SERIAL / AUTO\_INCREMENT / identity seq 的模式

-   **[schema]**现在，TypeEngine 对象具有处理复制和比较其特定类型值的方法。目前由 ORM 使用，见下文。[¶](#change-c835aa697ef27bc1779955d5c07a05f1)

-   **[schema]**固定条件是在主键列被重载时反射时发生的，其中 PrimaryKeyConstraint 会使反射列和编程列两者都加倍[¶](#change-935239bc03f9354863c60df9010bef03)

-   **[schema]**the “foreign\_key” attribute on Column and ColumnElement
    in general is deprecated, in favor of the “foreign\_keys”
    list/set-based attribute, which takes into account multiple foreign
    keys on one column.
    “foreign\_key”将返回“foreign\_keys”列表中的第一个元素，如果列表为空，则返回 None。[¶](#change-fed9bf9740d5a682cebb46515151e5c0)

### 源码[¶ T0\>](#change-0.3.0-sqlite "Permalink to this headline")

-   **[sqlite]**默认情况下，sqlite 布尔数据类型将 False / True 转换为 0/1
    [¶](#change-73aea24b040bca4e9965ccbb6e349046)

-   **[sqlite]**修复了日期/时间（SLDate /
    SLTime）类型；现在和 postgres 一样好[¶](#change-2f2f6303c04b763ae32a23ad61552cf4)

    参考文献：[＃335](http://www.sqlalchemy.org/trac/ticket/335)

### 预言[¶ T0\>](#change-0.3.0-oracle "Permalink to this headline")

-   **[oracle]**Oracle has experimental support for
    cx\_Oracle.TIMESTAMP, which requires a setinputsizes() call on the
    cursor that is now enabled via the ‘auto\_setinputsizes’ flag to the
    oracle dialect.[¶](#change-2a9e63a93ef8e8feadccbfb766be4727)

### 火鸟[¶ T0\>](#change-0.3.0-firebird "Permalink to this headline")

-   **[firebird]**别名不使用“AS”[¶](#change-a1b63a91c9fe5f9b5cae296b49617e99)

-   **[firebird]**在反映不存在的表[¶](#change-d6929c3d1968bd8c70fc395ea5abac4e)时正确地引发 NoSuchTableError

### 杂项[¶ T0\>](#change-0.3.0-misc "Permalink to this headline")

-   **[ms-sql]**fixes bug 261 (table reflection broken for MS-SQL
    case-sensitive
    databases)[¶](#change-fce7c38172fd247996365a12bbad8a3c)

-   **[ms-sql]**can now specify port for
    pymssql[¶](#change-5c03c1b73b7683cc5c95d8f6dcbff900)

-   **[ms-sql]**introduces new “auto\_identity\_insert” option for
    auto-switching between “SET IDENTITY\_INSERT” mode when values
    specified for IDENTITY
    columns[¶](#change-d61a87077e1d1c9fa96868d8e8805a87)

-   **[ms-sql]**现在支持多列外键[¶](#change-b7bc176c6d0fced17db9766f866ca8d9)

-   **[ms-sql]**固定为反映日期/日期时间列[¶](#change-f2463d5087105bc305f2098f3a932ea4)

-   **[ms-sql]**添加了 NCHAR 和 NVARCHAR 类型支持[¶](#change-b0212da21088f78c1fb2b5c69f08802a)

-   **[connections/pooling/execution]**connection pool tracks open
    cursors and automatically closes them if connection is returned to
    pool with cursors still opened.
    可能会受到导致它引发错误的选项的影响，或者什么也不做。修复了 MySQL 和其他问题[¶](#change-784d08fb847e35d6d1df60cc5b77a74c)的问题

-   **[connections/pooling/execution]**固定错误，其中 Connection 在 commit
    /
    rollback 后不会丢失事务[¶](#change-f6cf03213eb3b88352eb7887cc9cfe0e)

-   **[connections/pooling/execution]**将 scalar()方法添加到 ComposedSQLEngine，ResultProxy
    [¶](#change-f646180e65ac4eacb62bc3ff6b69286e)

-   **[connections/pooling/execution]**ResultProxy will close() the
    underlying cursor when the ResultProxy itself is closed.
    这将自动关闭已取出所有行的 ResultProxy 对象的游标（或已调用 scalar()）。[¶](#change-1753263c929a352b09f567f6469bcbe3)

-   **[connections/pooling/execution]**ResultProxy.fetchall() internally
    uses DBAPI fetchall() for better efficiency, added to mapper
    iteration as well (courtesy Michael
    Twomey)[¶](#change-8b8beaee4be0988cd69dfbdb5a8603e0)


