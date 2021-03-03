---
title: 火鸟
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/dialects/firebird/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - dialects
tags:
---
火鸟[¶ T0\>](#module-sqlalchemy.dialects.firebird.base "Permalink to this headline")
====================================================================================

支持 Firebird 数据库。

DBAPI 支持[¶](#dialect-firebird "Permalink to this headline")
------------------------------------------------------------

以下 dialect / DBAPI 选项可用。请参阅各个 DBAPI 部分的连接信息。

-   [FDB T0\>](#module-sqlalchemy.dialects.firebird.fdb)
-   [kinterbasdb T0\>](#module-sqlalchemy.dialects.firebird.kinterbasdb)

火鸟方言[¶](#firebird-dialects "Permalink to this headline")
------------------------------------------------------------

Firebird 提供两种不同的[方言](http://mc-computing.com/Databases/Firebird/SQL_Dialect.html)（不要与 SQLAlchemy
`Dialect`）：

方言 1
:   这是从 Interbase 6.0 之前继承而来的旧语法和行为。
方言 3
:   这是 Interbase 6.0 中引入的更新和支持的语法。

SQLAlchemy
Firebird 方言检测这些版本并相应地调整其 SQL 表示。然而，对方言 1 的支持没有得到很好的测试，可能有不相容的地方。

锁定行为[¶](#locking-behavior "Permalink to this headline")
-----------------------------------------------------------

Firebird 积极锁定表格。出于这个原因，DROP
TABLE 可能会挂起，直到其他事务被释放。SQLAlchemy 尽可能快地释放事务。挂起交易的最常见原因是未完全消费的结果集，即：

    result = engine.execute("select * from table")
    row = result.fetchone()
    return

如上所述，`ResultProxy`尚未完全消耗。连接将返回到池中，并且一旦 Python 垃圾回收器回收持有连接的对象（通常异步发生），事务状态就会回滚。可以通过在`ResultProxy`上调用`first()`来缓解上述用例，该操作将获取第一行并立即关闭所有剩余的游标/连接资源。

返回支持[¶](#returning-support "Permalink to this headline")
------------------------------------------------------------

Firebird
2.0 支持从插入返回结果集，并且 2.1 扩展了它以删除和更新。这通常由 SQLAlchemy
`returning()`方法公开，例如：

    # INSERT..RETURNINGplain
    result = table.insert().returning(table.c.col1, table.c.col2).\
                   values(name='foo')
    print result.fetchall()

    # UPDATE..RETURNING
    raises = empl.update().returning(empl.c.id, empl.c.salary).\
                  where(empl.c.sales>100).\
                  values(dict(salary=empl.c.salary * 1.1))
    print raises.fetchall()

FDB [¶ T0\>](#module-sqlalchemy.dialects.firebird.fdb "Permalink to this headline")
-----------------------------------------------------------------------------------

通过 fdb 驱动程序支持 Firebird 数据库。

fdb 是 Firebird 的兼容 kinterbasdb 的 DBAPI。

0.8 版新增功能： - 支持 fdb Firebird 驱动程序。

在版本 0.9 中更改： - fdb 方言现在是`firebird://`
URL 空间下的默认方言，因为`fdb`现在是官方 Firebird 的 Python 驱动程序。

### DBAPI [¶ T0\>](#dialect-firebird-fdb-url "Permalink to this headline")

fdb 的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/fdb/](http://pypi.python.org/pypi/fdb/)

### 连接[¶ T0\>](#dialect-firebird-fdb-connect "Permalink to this headline")

连接字符串：

    firebird+fdb://user:password@host:port/path/to/db[?key=value&key=value...]plain

### 参数[¶ T0\>](#arguments "Permalink to this headline")

`fdb`方言基于[`sqlalchemy.dialects.firebird.kinterbasdb`](#module-sqlalchemy.dialects.firebird.kinterbasdb "sqlalchemy.dialects.firebird.kinterbasdb")方言，但不接受 Kinterbasdb 所做的每个参数。

-   `enable_rowcount` -
    默认情况下，将其设置为 False 时，将禁用使用 Kinterbasdb 方言的“cursor.rowcount”，SQLAlchemy 通常在任何 UPDATE 或 DELETE 语句后自动调用。禁用时，SQLAlchemy 的 ResultProxy 将为 result.rowcount 返回-1。这里的基本原理是，当调用.rowcount 时，Kinterbasdb 需要第二次往返数据库
    -
    因为 SQLA 的 resultproxy 在非结果返回语句后自动关闭游标，因此必须调用 rowcount（如果有的话），在结果对象之前回。此外，cursor.rowcount 可能不会在旧版 Firebird 中返回正确结果，并将此标志设置为 False 也会导致 SQLAlchemy
    ORM 忽略其使用情况。该行为还可以通过[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")使用`enable_rowcount`选项以每个执行为基础进行控制：

        conn = engine.connect().execution_options(enable_rowcount=True)
        r = conn.execute(stmt)
        print r.rowcount

-   `retaining` -
    默认为 False。将此设置为 True 会将`retaining=True`关键字参数传递给 DBAPI 连接的`.commit()`和`.rollback()`这可以在某些情况下提高性能，但显然有重大警告。请阅读 fdb 和/或 kinterbasdb
    DBAPI 文档以了解此标志的含义。

    0.8.2 版新增： - `retaining`关键字参数 -
    在 0.8 中，为了向后兼容，默认为`True`。

    版本 0.9.0 更改： - `retaining`标志默认为`False`。在 0.8 中，默认为`True`。

    也可以看看

    [http://pythonhosted.org/fdb/usage-guide.html\#retaining-transactions](http://pythonhosted.org/fdb/usage-guide.html#retaining-transactions)
    - 有关“保留”标志的信息。

kinterbasdb [¶ T0\>](#module-sqlalchemy.dialects.firebird.kinterbasdb "Permalink to this headline")
---------------------------------------------------------------------------------------------------

通过 kinterbasdb 驱动程序支持 Firebird 数据库。

### DBAPI [¶ T0\>](#dialect-firebird-kinterbasdb-url "Permalink to this headline")

文档和下载信息（如果适用）kinterbasdb 可在以下网址获得：[http://firebirdsql.org/index.php?op=devel&amp；sub=python](http://firebirdsql.org/index.php?op=devel&sub=python)

### 连接[¶ T0\>](#dialect-firebird-kinterbasdb-connect "Permalink to this headline")

连接字符串：

    firebird+kinterbasdb://user:password@host:port/path/to/db[?key=value&key=value...]plain

### 参数[¶ T0\>](#id1 "Permalink to this headline")

Kinterbasdb 后端接受[`sqlalchemy.dialects.firebird.fdb`](#module-sqlalchemy.dialects.firebird.fdb "sqlalchemy.dialects.firebird.fdb")方言接受的`enable_rowcount`和`retaining`参数。另外，它还接受以下内容：

-   `type_conv` -
    选择在类型上完成的映射种类：默认情况下，SQLAlchemy 使用 200，Unicode，datetime 和 decimal 支持。请参阅下面的链接文件以获取更多信息。
-   `concurrency_level` -
    根据线程问题设置后端策略：默认情况下，SQLAlchemy 使用策略 1。请参阅下面的链接文件以获取更多信息。

也可以看看

[http://sourceforge.net/projects/kinterbasdb
T0\>](http://sourceforge.net/projects/kinterbasdb)

[http://kinterbasdb.sourceforge.net/dist\_docs/usage.html\#adv\_param\_conv\_dynamic\_type\_translation
T0\>](http://kinterbasdb.sourceforge.net/dist_docs/usage.html#adv_param_conv_dynamic_type_translation)

[http://kinterbasdb.sourceforge.net/dist\_docs/usage.html\#special\_issue\_concurrency
T0\>](http://kinterbasdb.sourceforge.net/dist_docs/usage.html#special_issue_concurrency)
