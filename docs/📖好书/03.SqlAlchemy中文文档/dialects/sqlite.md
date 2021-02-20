---
title: sqlite
date: 2021-02-20 22:41:38
permalink: /pages/243733/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - dialects
tags:
  - 
---
SQLite的[¶ T0\>](#module-sqlalchemy.dialects.sqlite.base "Permalink to this headline")
======================================================================================

支持SQLite数据库。

DBAPI支持[¶](#dialect-sqlite "Permalink to this headline")
----------------------------------------------------------

以下dialect / DBAPI选项可用。请参阅各个DBAPI部分的连接信息。

-   [pysqlite T0\>](#module-sqlalchemy.dialects.sqlite.pysqlite)
-   [pysqlcipher T0\>](#module-sqlalchemy.dialects.sqlite.pysqlcipher)

日期和时间类型[¶](#date-and-time-types "Permalink to this headline")
--------------------------------------------------------------------

SQLite没有内置的DATE，TIME或DATETIME类型，并且pysqlite不提供用于在Python
datetime对象和SQLite支持的格式之间转换值的开箱即用功能。SQLAlchemy自己的[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")和相关类型在使用SQlite时提供日期格式和分析功能。实现类是[`DATETIME`](#sqlalchemy.dialects.sqlite.DATETIME "sqlalchemy.dialects.sqlite.DATETIME")，[`DATE`](#sqlalchemy.dialects.sqlite.DATE "sqlalchemy.dialects.sqlite.DATE")和[`TIME`](#sqlalchemy.dialects.sqlite.TIME "sqlalchemy.dialects.sqlite.TIME")。这些类型将日期和时间表示为ISO格式的字符串，这也很好地支持排序。这些函数不依赖于典型的“libc”内部函数，因此完全支持历史日期。

### 确保文字亲和力[¶](#ensuring-text-affinity "Permalink to this headline")

为这些类型提供的DDL是标准的`DATE`，`TIME`和`DATETIME`指标。但是，自定义存储格式也可以应用于这些类型。当检测到存储格式不包含字母字符时，这些类型的DDL将呈现为`DATE_CHAR`，`TIME_CHAR`和`DATETIME_CHAR`，以便该列继续具有文本亲和力。

也可以看看

[Type Affinity](http://www.sqlite.org/datatype3.html#affinity) -
在SQLite文档中

SQLite自动递增行为[¶](#sqlite-auto-incrementing-behavior "Permalink to this headline")
--------------------------------------------------------------------------------------

SQLite自动增量的背景是：[http://sqlite.org/autoinc.html](http://sqlite.org/autoinc.html)

关键概念：

-   SQLite有一个隐含的“自动增量”功能，对于任何使用“INTEGER PRIMARY
    KEY”专门为+主键创建的非复合主键列进行。
-   SQLite也有一个明确的“AUTOINCREMENT”关键字，即**not**等价于隐式自动增量特性；此关键字不推荐用于一般用途。除非使用特殊的SQLite特定指令，否则SQLAlchemy不会呈现此关键字（请参见下文）。但是，它仍然要求列的类型被命名为“INTEGER”。

### 使用AUTOINCREMENT关键字[¶](#using-the-autoincrement-keyword "Permalink to this headline")

要在呈现DDL时在主键列上专门呈现AUTOINCREMENT关键字，请将以下标记`sqlite_autoincrement=True`添加到Table结构中：

    Table('sometable', metadata,
            Column('id', Integer, primary_key=True),
            sqlite_autoincrement=True)

### 允许自动增量行为SQLAlchemy类型不是Integer / INTEGER [¶](#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer "Permalink to this headline")

SQLite的键入模型基于命名约定。除此之外，这意味着包含子字符串`"INT"`的任何类型名称将被确定为“整数相似性”。一个名为`"BIGINT"`，`"SPECIAL_INT"`甚至`"XYZINTQPR"`的类型将被SQLite视为“整数”关联。However, **the SQLite
autoincrement feature, whether implicitly or explicitly enabled,
requires that the name of the column’s type is exactly the string
“INTEGER”**. Therefore, if an application uses a type like
[`BigInteger`](core_type_basics.html#sqlalchemy.types.BigInteger "sqlalchemy.types.BigInteger")
for a primary key, on SQLite this type will need to be rendered as the
name `"INTEGER"` when emitting the initial
`CREATE TABLE` statement in order for the
autoincrement behavior to be available.

实现这一目标的一种方法是在SQLite上仅使用[`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")使用[`Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")：

    table = Table(
        "my_table", metadata,
        Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    )

另一种方法是在针对SQLite编译时使用[`BigInteger`](core_type_basics.html#sqlalchemy.types.BigInteger "sqlalchemy.types.BigInteger")的子类来覆盖其DDL名称为`INTEGER`：

    from sqlalchemy import BigInteger
    from sqlalchemy.ext.compiler import compiles

    class SLBigInteger(BigInteger):
        pass

    @compiles(SLBigInteger, 'sqlite')
    def bi_c(element, compiler, **kw):
        return "INTEGER"

    @compiles(SLBigInteger)
    def bi_c(element, compiler, **kw):
        return compiler.visit_BIGINT(element, **kw)


    table = Table(
        "my_table", metadata,
        Column("id", SLBigInteger(), primary_key=True)
    )

也可以看看

[`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")

[Custom SQL Constructs and Compilation Extension](core_compiler.html)

[数据类型在SQLite版本3中](http://sqlite.org/datatype3.html)

数据库锁定行为/并发[¶](#database-locking-behavior-concurrency "Permalink to this headline")
-------------------------------------------------------------------------------------------

SQLite不是专为高级别的写入并发而设计的。作为文件的数据库本身在事务内的写操作期间被完全锁定，这意味着在此期间恰好有一个“连接”（实际上是文件句柄）对数据库有独占访问权限
- 在此期间所有其他“连接”将被阻止时间。

Python
DBAPI规范还要求一个始终在事务中的连接模型；没有`connection.begin()`方法，只有`connection.commit()`和`connection.rollback()`立即开始。这似乎意味着SQLite驱动程序理论上在任何时候都只允许在一个特定的数据库文件上使用一个文件句柄；然而，SQlite本身以及pysqlite驱动程序中都有几个因素，这些因素显着地放宽了这一限制。

然而，无论使用什么锁定模式，一旦事务启动并且DML（例如INSERT，UPDATE，DELETE）至少被发射出去，SQLite仍然会始终锁定数据库文件，并且这至少会在该点处阻止其他事务他们也试图发射DML。默认情况下，该块的时间长度非常短，并且在发生错误时超时。

与SQLAlchemy
ORM一起使用时，此行为变得更加重要。默认情况下，SQLAlchemy的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象在事务中运行，并且使用其自动刷新模型，可以在任何SELECT语句之前发出DML。这可能会导致SQLite数据库的锁定速度超出预期。SQLite的锁定模式和pysqlite驱动程序可以在一定程度上被操纵，但是应该注意的是，使用SQLite实现高度的写入并发是一场失败的战斗。

有关SQLite缺乏设计写入并发性的更多信息，请参阅[另一个RDBMS可能更好地工作的情况
- 高并发性](http://www.sqlite.org/whentouse.html)接近页面底部。

以下小节介绍了受SQLite的基于文件的体系结构影响的区域，并且通常还需要解决方法才能在使用pysqlite驱动程序时工作。

事务隔离级别[¶](#transaction-isolation-level "Permalink to this headline")
--------------------------------------------------------------------------

SQLite支持以非标准方式沿两个轴进行“事务隔离”。One is that of the [PRAGMA
read\_uncommitted](http://www.sqlite.org/pragma.html#pragma_read_uncommitted)
instruction. This setting can essentially switch SQLite between its
default mode of `SERIALIZABLE` isolation, and a
“dirty read” isolation mode normally referred to as
`READ UNCOMMITTED`.

SQLAlchemy使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的[`create_engine.isolation_level`{.xref
.py .py-paramref .docutils
.literal}](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")参数连接到此PRAGMA语句中。与SQLite一起使用时，此参数的有效值分别为`"SERIALIZABLE"`和`“READ UNCOMMITTED”`分别为0和1。SQLite默认为`SERIALIZABLE`，但其行为受到pysqlite驱动程序默认行为的影响。

SQLite的事务锁定所受影响的另一个轴是通过使用的`BEGIN`语句的性质。如[BEGIN
TRANSACTION](http://sqlite.org/lang_transaction.html)所述，这三个品种是“延期”，“即时”和“排他”。A
straight `BEGIN` statement uses the “deferred” mode,
where the the database file is not locked until the first read or write
operation, and read access remains open to other transactions until the
first write operation.
但同样重要的是要注意，在第一次写操作之前，pysqlite驱动程序会通过*干扰此行为，甚至不会发出BEGIN*。

警告

SQLite的事务范围受到pysqlite驱动程序中未解决的问题的影响，该驱动程序将BEGIN语句推迟到比通常可行的程度更大的程度。有关解决此问题的技术，请参阅[Serializable
isolation / Savepoints / Transactional
DDL](#pysqlite-serializable)一节。

SAVEPOINT支持[¶](#savepoint-support "Permalink to this headline")
-----------------------------------------------------------------

SQLite支持SAVEPOINT，它只在事务开始时才起作用。SQLAlchemy的SAVEPOINT支持可以在核心级别使用[`Connection.begin_nested()`](core_connections.html#sqlalchemy.engine.Connection.begin_nested "sqlalchemy.engine.Connection.begin_nested")方法，在ORM级别使用[`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")。但是，除非采取了解决方法，否则SAVEPOINTs根本无法使用pysqlite。

警告

SQLite的SAVEPOINT功能受到pysqlite驱动程序中未解决的问题的影响，该驱动程序将BEGIN语句的推迟程度比往往可行。有关解决此问题的技术，请参阅[Serializable
isolation / Savepoints / Transactional
DDL](#pysqlite-serializable)一节。

事务性DDL [¶](#transactional-ddl "Permalink to this headline")
--------------------------------------------------------------

SQLite数据库也支持事务性[DDL](glossary.html#term-ddl)。在这种情况下，pysqlite驱动程序不仅无法启动事务，还会在检测到DDL时结束任何现有的转换，因此再次需要解决方法。

警告

SQLite的事务性DDL受到pysqlite驱动程序中未解决的问题的影响，该问题无法发出BEGIN，并且在遇到DDL时强制COMMIT取消任何事务。有关解决此问题的技术，请参阅[Serializable
isolation / Savepoints / Transactional
DDL](#pysqlite-serializable)一节。

外键支持[¶](#foreign-key-support "Permalink to this headline")
--------------------------------------------------------------

SQLite在为表发出CREATE语句时支持FOREIGN
KEY语法，但默认情况下，这些约束对表的操作没有影响。

SQLite上的约束检查有三个先决条件：

-   至少必须使用SQLite版本3.6.19
-   SQLite库必须在没有启用SQLITE\_OMIT\_FOREIGN\_KEY或SQLITE\_OMIT\_TRIGGER符号的情况下编译*。*
-   在使用前必须在所有连接上发送`PRAGMA foreign_keys = ON`

SQLAlchemy允许通过使用事件自动为新连接发布`PRAGMA`语句：

    from sqlalchemy.engine import Engine
    from sqlalchemy import event

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

警告

当启用SQLite外键时，**不可能**为包含相互依赖的外键约束的表发出CREATE或DROP语句；为这些表发出DDL需要使用ALTER
TABLE单独创建或删除这些约束，SQLite不支持这些约束。

也可以看看

[SQLite外键支持](http://www.sqlite.org/foreignkeys.html) -
在SQLite网站上。

[Events](core_event.html) - SQLAlchemy事件API。

[Creating/Dropping Foreign Key Constraints via ALTER](core_constraints.html#use-alter) - 关于SQLAlchemy处理设施的更多信息
:   相互依赖的外键约束。

类型反射[¶](#type-reflection "Permalink to this headline")
----------------------------------------------------------

SQLite类型与大多数其他数据库后端的类型不同，因为类型的字符串名称通常不以一对一的方式与“类型”相对应。相反，SQLite根据类型的字符串匹配模式将每列的输入行为链接到五个所谓的“类型亲和性”之一。

SQLAlchemy的反射过程在检查类型时使用简单的查找表来链接返回给提供的SQLAlchemy类型的关键字。这个查询表在SQLite方言中，与所有其他方言一样。但是，当特定类型名称不在查找映射中时，SQLite方言具有不同的“后退”例程；它实现了位于[http://www.sqlite.org/datatype3.html](http://www.sqlite.org/datatype3.html)
2.1节的SQLite“type affinity”方案。

所提供的typemap将直接关联以下类型的完全字符串名称匹配：

[`BIGINT`](core_type_basics.html#sqlalchemy.types.BIGINT "sqlalchemy.types.BIGINT"),
[`BLOB`](core_type_basics.html#sqlalchemy.types.BLOB "sqlalchemy.types.BLOB"),
[`BOOLEAN`](core_type_basics.html#sqlalchemy.types.BOOLEAN "sqlalchemy.types.BOOLEAN"),
[`BOOLEAN`](core_type_basics.html#sqlalchemy.types.BOOLEAN "sqlalchemy.types.BOOLEAN"),
[`CHAR`](core_type_basics.html#sqlalchemy.types.CHAR "sqlalchemy.types.CHAR"),
[`DATE`](core_type_basics.html#sqlalchemy.types.DATE "sqlalchemy.types.DATE"),
[`DATETIME`](core_type_basics.html#sqlalchemy.types.DATETIME "sqlalchemy.types.DATETIME"),
[`FLOAT`](core_type_basics.html#sqlalchemy.types.FLOAT "sqlalchemy.types.FLOAT"),
[`DECIMAL`](core_type_basics.html#sqlalchemy.types.DECIMAL "sqlalchemy.types.DECIMAL"),
[`FLOAT`](core_type_basics.html#sqlalchemy.types.FLOAT "sqlalchemy.types.FLOAT"),
[`INTEGER`](core_type_basics.html#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER"),
[`INTEGER`](core_type_basics.html#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER"),
[`NUMERIC`](core_type_basics.html#sqlalchemy.types.NUMERIC "sqlalchemy.types.NUMERIC"),
[`REAL`](core_type_basics.html#sqlalchemy.types.REAL "sqlalchemy.types.REAL"),
[`SMALLINT`](core_type_basics.html#sqlalchemy.types.SMALLINT "sqlalchemy.types.SMALLINT"),
[`TEXT`](core_type_basics.html#sqlalchemy.types.TEXT "sqlalchemy.types.TEXT"),
[`TIME`](core_type_basics.html#sqlalchemy.types.TIME "sqlalchemy.types.TIME"),
[`TIMESTAMP`](core_type_basics.html#sqlalchemy.types.TIMESTAMP "sqlalchemy.types.TIMESTAMP"),
[`VARCHAR`](core_type_basics.html#sqlalchemy.types.VARCHAR "sqlalchemy.types.VARCHAR"),
[`NVARCHAR`](core_type_basics.html#sqlalchemy.types.NVARCHAR "sqlalchemy.types.NVARCHAR"),
[`NCHAR`](core_type_basics.html#sqlalchemy.types.NCHAR "sqlalchemy.types.NCHAR")

当类型名称与以上类型之一不匹配时，将使用“类型关联”查找：

-   如果类型名称包含字符串`INT`，则返回[`INTEGER`](core_type_basics.html#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER")
-   [`TEXT`](core_type_basics.html#sqlalchemy.types.TEXT "sqlalchemy.types.TEXT")
    is returned if the type name includes the string `CHAR`, `CLOB` or `TEXT`
-   [`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")
    is returned if the type name includes the string `BLOB`
-   如果类型名称包含字符串`REAL`，`FLOA`或`DOUB`，则返回[`REAL`](core_type_basics.html#sqlalchemy.types.REAL "sqlalchemy.types.REAL")。
-   否则，使用[`NUMERIC`](core_type_basics.html#sqlalchemy.types.NUMERIC "sqlalchemy.types.NUMERIC")类型。

New in version 0.9.3: Support for SQLite type affinity rules when
reflecting columns.

部分索引[¶](#partial-indexes "Permalink to this headline")
----------------------------------------------------------

部分索引，例如其中一个使用WHERE子句，可以使用参数`sqlite_where`在DDL系统中指定：

    tbl = Table('testtbl', m, Column('data', Integer))
    idx = Index('test_idx1', tbl.c.data,
                sqlite_where=and_(tbl.c.data > 5, tbl.c.data < 10))

索引将在创建时呈现为：

    CREATE INDEX test_idx1 ON testtbl (data)
    WHERE data > 5 AND data < 10

版本0.9.9中的新功能

虚线列名称[¶](#dotted-column-names "Permalink to this headline")
----------------------------------------------------------------

使用明确具有句点的表名或列名是**不推荐**。虽然这对于关系数据库来说通常是一个坏主意，但由于点是一个语法上重要的特征，SQLite驱动程序直到版本**3.10.0**
SQLite有一个错误，它要求SQLAlchemy过滤掉这些结果集中的点。

在版本1.1中更改：从SQLite版本3.10.0开始，下列SQLite问题已得到解决。SQLAlchemy自**1.1**自动禁用基于检测此版本的内部变通方法。

这个错误完全在SQLAlchemy之外，可以这样说明：

    import sqlite3

    assert sqlite3.sqlite_version_info < (3, 10, 0), "bug is fixed in this version"

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("create table x (a integer, b integer)")
    cursor.execute("insert into x (a, b) values (1, 1)")
    cursor.execute("insert into x (a, b) values (2, 2)")

    cursor.execute("select x.a, x.b from x")
    assert [c[0] for c in cursor.description] == ['a', 'b']

    cursor.execute('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert [c[0] for c in cursor.description] == ['a', 'b'], \
        [c[0] for c in cursor.description]

第二个断言失败：

    Traceback (most recent call last):
      File "test.py", line 19, in <module>
        [c[0] for c in cursor.description]
    AssertionError: ['x.a', 'x.b']

在上面的情况中，驱动程序错误地报告了列的名称，包括表的名称，这与UNION不存在时完全不一致。

SQLAlchemy依赖于列名与原始语句匹配的可预测性，因此SQLAlchemy方言别无选择，只能将其过滤掉：

    from sqlalchemy import create_engine

    eng = create_engine("sqlite://")
    conn = eng.connect()

    conn.execute("create table x (a integer, b integer)")
    conn.execute("insert into x (a, b) values (1, 1)")
    conn.execute("insert into x (a, b) values (2, 2)")

    result = conn.execute("select x.a, x.b from x")
    assert result.keys() == ["a", "b"]

    result = conn.execute('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert result.keys() == ["a", "b"]

注意上面，即使SQLAlchemy过滤掉了这些点，*这两个名字仍然是可寻址的*：

    >>> row = result.first()
    >>> row["a"]
    1
    >>> row["x.a"]
    1
    >>> row["b"]
    1
    >>> row["x.b"]
    1

Therefore, the workaround applied by SQLAlchemy only impacts
[`ResultProxy.keys()`](core_connections.html#sqlalchemy.engine.ResultProxy.keys "sqlalchemy.engine.ResultProxy.keys")
and [`RowProxy.keys()`](core_connections.html#sqlalchemy.engine.RowProxy.keys "sqlalchemy.engine.RowProxy.keys")
in the public API. In the very specific case where an application is
forced to use column names that contain dots, and the functionality of
[`ResultProxy.keys()`](core_connections.html#sqlalchemy.engine.ResultProxy.keys "sqlalchemy.engine.ResultProxy.keys")
and [`RowProxy.keys()`](core_connections.html#sqlalchemy.engine.RowProxy.keys "sqlalchemy.engine.RowProxy.keys")
is required to return these dotted names unmodified, the
`sqlite_raw_colnames` execution option may be
provided, either on a per-[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
basis:

    result = conn.execution_options(sqlite_raw_colnames=True).execute('''
        select x.a, x.b from x where a=1
        union
        select x.a, x.b from x where a=2
    ''')
    assert result.keys() == ["x.a", "x.b"]

或基于每个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")：

    engine = create_engine("sqlite://", execution_options={"sqlite_raw_colnames": True})

在使用per- [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")执行选项时，请注意**使用UNION的核心和ORM查询可能无法正常工作**。

SQLite数据类型[¶](#sqlite-data-types "Permalink to this headline")
------------------------------------------------------------------

与所有SQLAlchemy方言一样，所有已知可用于SQLite的UPPERCASE类型都可以从顶级方言导入，无论它们源自[`sqlalchemy.types`](core_type_basics.html#module-sqlalchemy.types "sqlalchemy.types")还是来自本地方言：

    from sqlalchemy.dialects.sqlite import \
                BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
                INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
                VARCHAR

 *class*`sqlalchemy.dialects.sqlite.`{.descclassname}`DATETIME`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.dialects.sqlite.DATETIME "Permalink to this definition")
:   基础：`sqlalchemy.dialects.sqlite.base._DateTimeMixin`，[`sqlalchemy.types.DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

    使用字符串在SQLite中表示Python日期时间对象。

    默认的字符串存储格式是：

        "%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(min)02d:%(second)02d.%(microsecond)06d"

    例如。：

        2011-03-15 12:05:57.10558

    存储格式可以使用`storage_format`和`regexp`参数进行一定程度的自定义，例如：

        import re
        from sqlalchemy.dialects.sqlite import DATETIME

        dt = DATETIME(
            storage_format="%(year)04d/%(month)02d/%(day)02d %(hour)02d:%(min)02d:%(second)02d",
            regexp=r"(\d+)/(\d+)/(\d+) (\d+)-(\d+)-(\d+)"
        )

    参数：

    -   **storage\_format**[¶](#sqlalchemy.dialects.sqlite.DATETIME.params.storage_format)
        – format string which will be applied to the dict with keys
        year, month, day, hour, minute, second, and microsecond.
    -   **regexp**[¶](#sqlalchemy.dialects.sqlite.DATETIME.params.regexp)
        – regular expression which will be applied to incoming result
        rows.
        如果正则表达式包含命名组，则所得匹配字典作为关键字参数应用于Python
        datetime()构造函数。否则，如果使用位置组，则使用位置参数通过`* map（int， match_obj.groups（0））调用datetime T0>。`{.docutils
        .literal}

*class* `sqlalchemy.dialects.sqlite。`{.descclassname} `DATE`{.descname} （ *storage\_format =无*，*regexp = None*，*\*\* kw* ） [¶](#sqlalchemy.dialects.sqlite.DATE "Permalink to this definition")
:   基础：`sqlalchemy.dialects.sqlite.base._DateTimeMixin`，[`sqlalchemy.types.Date`](core_type_basics.html#sqlalchemy.types.Date "sqlalchemy.types.Date")

    使用字符串在SQLite中表示Python日期对象。

    默认的字符串存储格式是：

        "%(year)04d-%(month)02d-%(day)02d"

    例如。：

        2011-03-15

    存储格式可以使用`storage_format`和`regexp`参数进行一定程度的自定义，例如：

        import re
        from sqlalchemy.dialects.sqlite import DATE

        d = DATE(
                storage_format="%(month)02d/%(day)02d/%(year)04d",
                regexp=re.compile("(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)")
            )

    参数：

    -   **storage\_format**[¶](#sqlalchemy.dialects.sqlite.DATE.params.storage_format)
        – format string which will be applied to the dict with keys
        year, month, and day.
    -   **regexp**[¶](#sqlalchemy.dialects.sqlite.DATE.params.regexp) –
        regular expression which will be applied to incoming result
        rows.
        如果正则表达式包含命名组，则所得到的匹配字典作为关键字参数应用于Python
        date()构造函数。否则，如果使用位置组，则使用位置参数通过`* map（int， match_obj.groups（0））调用date T0>。`{.docutils
        .literal}

 *class*`sqlalchemy.dialects.sqlite.`{.descclassname}`TIME`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.dialects.sqlite.TIME "Permalink to this definition")
:   基础：`sqlalchemy.dialects.sqlite.base._DateTimeMixin`，[`sqlalchemy.types.Time`](core_type_basics.html#sqlalchemy.types.Time "sqlalchemy.types.Time")

    使用字符串在SQLite中表示一个Python时间对象。

    默认的字符串存储格式是：

        "%(hour)02d:%(minute)02d:%(second)02d.%(microsecond)06d"

    例如。：

        12:05:57.10558

    存储格式可以使用`storage_format`和`regexp`参数进行一定程度的自定义，例如：

        import re
        from sqlalchemy.dialects.sqlite import TIME

        t = TIME(
            storage_format="%(hour)02d-%(minute)02d-%(second)02d-%(microsecond)06d",
            regexp=re.compile("(\d+)-(\d+)-(\d+)-(?:-(\d+))?")
        )

    参数：

    -   T0\> **storage\_format T1\> [¶ T2\> -
        将被施加到字典连键时，分，秒和微秒格式字符串。](#sqlalchemy.dialects.sqlite.TIME.params.storage_format)**
    -   **regexp**[¶](#sqlalchemy.dialects.sqlite.TIME.params.regexp) –
        regular expression which will be applied to incoming result
        rows.
        如果正则表达式包含命名组，则所得匹配字典作为关键字参数应用于Python
        time()构造函数。否则，如果使用位置组，time()构造函数将通过位置参数通过`* map（int， match_obj.groups（0）） T0>。`{.docutils
        .literal}

Pysqlite [¶ T0\>](#module-sqlalchemy.dialects.sqlite.pysqlite "Permalink to this headline")
-------------------------------------------------------------------------------------------

通过pysqlite驱动程序支持SQLite数据库。

请注意，`pysqlite`与Python发行版中包含的`sqlite3`模块是相同的驱动程序。

### DBAPI [¶ T0\>](#dialect-sqlite-pysqlite-url "Permalink to this headline")

pysqlite的文档和下载信息（如果适用）可在以下网址获得：[http://docs.python.org/library/sqlite3.html](http://docs.python.org/library/sqlite3.html)

### 连接[¶ T0\>](#dialect-sqlite-pysqlite-connect "Permalink to this headline")

连接字符串：

    sqlite+pysqlite:///file_path

### 驱动程序[¶ T0\>](#driver "Permalink to this headline")

当使用Python 2.5或更高版本时，内置的`sqlite3`驱动程序已经安装，不需要额外的安装。否则，需要存在`pysqlite2`驱动程序。这与`sqlite3`是相同的驱动程序，只是名称不同而已。

`pysqlite2`驱动程序将首先加载，如果未找到，则加载`sqlite3`。这允许明确安装的pysqlite驱动程序优先于内置驱动程序。As with
all dialects, a specific DBAPI module may be provided to
[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
to control this explicitly:

    from sqlite3 import dbapi2 as sqlite
    e = create_engine('sqlite+pysqlite:///file.db', module=sqlite)

### 连接字符串[¶](#connect-strings "Permalink to this headline")

SQLite数据库的文件规范被认为是URL的“数据库”部分。请注意，SQLAlchemy网址的格式是：

    driver://user:pass@host/database

这意味着要使用的实际文件名以第三个斜杠的**右侧**中的字符开头。因此连接到相对的文件路径如下所示：

    # relative path
    e = create_engine('sqlite:///path/to/database.db')

绝对路径，以斜杠开始，表示您需要**四个**斜线：

    # absolute path
    e = create_engine('sqlite:////path/to/database.db')

要使用Windows路径，可以使用常规的驱动器规格和反斜杠。可能需要双反斜杠：

    # absolute path on Windows
    e = create_engine('sqlite:///C:\\path\\to\\database.db')

如果没有文件路径存在，sqlite `:memory:`标识符是默认值。指定`sqlite://`，而不是别的：

    # in-memory database
    e = create_engine('sqlite://')

### 与sqlite3“native”日期和日期时间类型兼容[¶](#compatibility-with-sqlite3-native-date-and-datetime-types "Permalink to this headline")

pysqlite驱动程序包括sqlite3.PARSE\_DECLTYPES和sqlite3.PARSE\_COLNAMES选项，这些选项会将显式转换为“date”或“timestamp”的任何列或表达式转换为Python日期或日期时间对象。pysqlite方言提供的日期和日期时间类型目前与这些选项不兼容，因为它们呈现ISO日期/日期时间（包括微秒），而pysqlite的驱动程序却没有。此外，SQLAlchemy目前不会自动呈现独立函数“current\_timestamp”和“current\_date”所需的“强制转换”语法，以便本机返回datetime
/ date类型。不幸的是，pysqlite没有在`cursor.description`中提供标准DBAPI类型，使得SQLAlchemy无法在没有昂贵的每行类型检查的情况下即时检测这些类型。

请记住，建议不要使用pysqlite的解析选项，也不需要使用SQLAlchemy，如果在create\_engine()上配置了“native\_datetime
= True”，则可以强制使用PARSE\_DECLTYPES：

    engine = create_engine('sqlite://',
        connect_args={'detect_types':
            sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES},
        native_datetime=True
    )

启用此标志时，DATE和TIMESTAMP类型（但注意 -
不是DATETIME或TIME类型......困惑了吗？）将不执行任何绑定参数或结果处理。执行“func.current\_date()”将返回一个字符串。“func.current\_timestamp()”被注册为在SQLAlchemy中返回DATETIME类型，所以该函数仍然接收SQLAlchemy级别的结果处理。

### 线程/池化行为[¶](#threading-pooling-behavior "Permalink to this headline")

Pysqlite的默认行为是禁止在多个线程中使用单个连接。这本来是为了适应不同环境下不支持多线程操作的旧版SQLite。特别是，在任何情况下，较旧的SQLite版本都不允许在多线程中使用`:memory:`数据库。

Pysqlite确实包含一个名为`check_same_thread`的now-undocumented标志，它将禁用此检查，但请注意，pysqlite连接在多个线程中并发使用仍然不安全。特别是，任何语句执行调用都需要外部互斥，因为Pysqlite不会提供错误消息的线程安全传播等。因此，尽管即使`:memory:`数据库可以在现代SQLite的线程之间共享，Pysqlite也不能提供足够的线程安全性来使此用法值得。

SQLAlchemy设置池以使用Pysqlite的默认行为：

-   当指定`:memory:`
    SQLite数据库时，缺省方言将使用[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")。该池为每个线程维护一个连接，以便当前线程中对引擎的所有访问使用相同的`:memory:`数据库 - 其他线程将访问不同的`:memory:`

-   当指定基于文件的数据库时，方言将使用[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")作为连接的来源。此池关闭并丢弃立即返回到池的连接。基于SQLite文件的连接开销非常低，因此并不是必需的。该方案还可以防止在另一个线程中再次使用连接，并且最适合SQLite的粗粒度文件锁定。

    版本0.7中的更改：针对基于SQLite文件的数据库的[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")的默认选择。以前的版本默认为所有SQLite数据库选择[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")。

#### 在多个线程中使用内存数据库[¶](#using-a-memory-database-in-multiple-threads "Permalink to this headline")

要在多线程场景中使用`:memory:`数据库，必须在线程间共享相同的连接对象，因为数据库仅存在于该连接的范围内。[`StaticPool`](core_pooling.html#sqlalchemy.pool.StaticPool "sqlalchemy.pool.StaticPool")实现将全局维护一个连接，并且`check_same_thread`标志可以作为`False`传递给Pysqlite：

    from sqlalchemy.pool import StaticPool
    engine = create_engine('sqlite://',
                        connect_args={'check_same_thread':False},
                        poolclass=StaticPool)

请注意，在多个线程中使用`:memory:`数据库需要最新版本的SQLite。

#### 在SQLite中使用临时表[¶](#using-temporary-tables-with-sqlite "Permalink to this headline")

由于SQLite处理临时表的方式，如果您希望在跨连接池的多个签出的基于文件的SQLite数据库中使用临时表，例如在使用临时表的ORM
[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时临时表表应该在[`Session.commit()`](orm_session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")或[`Session.rollback()`](orm_session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")之后继续保持，必须使用维护单个连接的池。如果仅在当前线程中需要作用域，则使用[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")，或者在这种情况下多个线程内需要[`StaticPool`](core_pooling.html#sqlalchemy.pool.StaticPool "sqlalchemy.pool.StaticPool")作用域：

    # maintain the same connection per thread
    from sqlalchemy.pool import SingletonThreadPool
    engine = create_engine('sqlite:///mydb.db',
                        poolclass=SingletonThreadPool)


    # maintain the same connection across all threads
    from sqlalchemy.pool import StaticPool
    engine = create_engine('sqlite:///mydb.db',
                        poolclass=StaticPool)

请注意，应该为要使用的线程数配置[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")；超过这个数字，连接将以非确定性的方式被关闭。

### Unicode的[¶ T0\>](#unicode "Permalink to this headline")

pysqlite驱动程序只返回结果集中的Python `unicode`对象，从不使用普通字符串，并且在所有情况下都可以在绑定参数值中容纳`unicode`对象。无论使用哪种SQLAlchemy字符串类型，Python 2中的Python
`unicode`都将基于字符串的结果值。但仍然应该使用[`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")类型来指示那些需要unicode的列，以便非故意传递的非`unicode`值会发出警告。如果传递包含非ASCII字符的非`unicode`字符串，则Pysqlite将发出错误。

### 可串行化隔离/保存点/事务性DDL [¶](#serializable-isolation-savepoints-transactional-ddl "Permalink to this headline")

在[Database Locking Behavior /
Concurrency](#sqlite-concurrency)部分中，我们引用了pysqlite驱动程序的各种问题，这些问题阻止SQLite的几个功能正常工作。pysqlite
DBAPI驱动程序有几个长期存在的错误会影响其交易行为的正确性。在默认操作模式下，SQLite功能（如SERIALIZABLE隔离，事务性DDL和SAVEPOINT支持）不起作用，为了使用这些功能，必须采取解决方法。

这个问题基本上是驱动程序尝试第二次猜测用户的意图，无法启动事务并且有时会过早结束它们，以尽量减少SQLite数据库的文件锁定行为，尽管SQLite本身使用“共享”锁来进行只读操作，只有活动。

SQLAlchemy默认选择不改变这种行为，因为它是pysqlite驱动程序的长期预期行为；如果当pysqlite驱动程序尝试修复这些问题时，这将成为更多SQLAlchemy默认驱动程序的驱动程序。

好消息是，通过一些事件，我们可以完全实现事务性支持，完全禁用pysqlite的功能并自行发布BEGIN。这是通过使用两个事件监听器来实现的：

    from sqlalchemy import create_engine, event

    engine = create_engine("sqlite:///myfile.db")

    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, "begin")
    def do_begin(conn):
        # emit our own BEGIN
        conn.execute("BEGIN")

上面，我们拦截一个新的pysqlite连接并禁用任何事务集成。Then, at the point
at which SQLAlchemy knows that transaction scope is to begin, we emit
`"BEGIN"` ourselves.

当我们控制`"BEGIN"`时，我们还可以直接控制[BEGIN
TRANSACTION](http://sqlite.org/lang_transaction.html)中引入的SQLite锁定模式，方法是将所需的锁定模式添加到我们的`"BEGIN"`

    @event.listens_for(engine, "begin")
    def do_begin(conn):
        conn.execute("BEGIN EXCLUSIVE")

也可以看看

[BEGIN TRANSACTION](http://sqlite.org/lang_transaction.html) -
在SQLite网站上

[sqlite3 SELECT does not BEGIN a
transaction](http://bugs.python.org/issue9924) - on the Python bug
tracker

[sqlite3 module breaks transactions and potentially corrupts
data](http://bugs.python.org/issue10740) - on the Python bug tracker

Pysqlcipher [¶ T0\>](#module-sqlalchemy.dialects.sqlite.pysqlcipher "Permalink to this headline")
-------------------------------------------------------------------------------------------------

通过pysqlcipher驱动程序支持SQLite数据库。

`pysqlcipher`是使用[SQLCipher](https://www.zetetic.net/sqlcipher)后端的标准`pysqlite`驱动程序的一个分支。

版本0.9.9中的新功能

### DBAPI [¶ T0\>](#dialect-sqlite-pysqlcipher-url "Permalink to this headline")

pysqlcipher的文档和下载信息（如果适用）可在以下网址获得：[https://pypi.python.org/pypi/pysqlcipher](https://pypi.python.org/pypi/pysqlcipher)

### 连接[¶ T0\>](#dialect-sqlite-pysqlcipher-connect "Permalink to this headline")

连接字符串：

    sqlite+pysqlcipher://:passphrase/file_path[?kdf_iter=<iter>]

### 驱动程序[¶ T0\>](#id3 "Permalink to this headline")

这里的驱动程序是使用SQLCipher引擎的[pysqlcipher](https://pypi.python.org/pypi/pysqlcipher)驱动程序。该系统基本上向SQLite引入了新的PRAGMA命令，允许设置密码和其他加密参数，从而允许对数据库文件进行加密。

### 连接字符串[¶](#id5 "Permalink to this headline")

连接字符串的格式与[`pysqlite`](#module-sqlalchemy.dialects.sqlite.pysqlite "sqlalchemy.dialects.sqlite.pysqlite")驱动程序的格式相同，只是现在接受了“密码”字段，其中应包含密码短语：

    e = create_engine('sqlite+pysqlcipher://:testing@/foo.db')

对于绝对文件路径，应该为数据库名称使用两个斜杠：

    e = create_engine('sqlite+pysqlcipher://:testing@//path/to/foo.db')

在[https://www.zetetic.net/sqlcipher/sqlcipher-api/](https://www.zetetic.net/sqlcipher/sqlcipher-api/)中记录的SQLCipher支持的其他与加密相关的编译指示的选择可以在查询字符串中传递，并且会导致PRAGMA被称为每个新的连接。目前，支持`cipher`，`kdf_iter` `cipher_page_size`和`cipher_use_hmac`

    e = create_engine('sqlite+pysqlcipher://:testing@/foo.db?cipher=aes-256-cfb&kdf_iter=64000')

### 合并行为[¶](#pooling-behavior "Permalink to this headline")

驱动程序根据[Threading/Pooling
Behavior](#pysqlite-threading-pooling)中的描述更改pysqlite的默认池行为。pysqlcipher驱动程序的连接速度比pysqlite驱动程序慢得多，很可能是由于加密开销，所以这里的方言默认使用[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")实现，而不是[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")由pysqlite使用的池。As
always, the pool implementation is entirely configurable using the
[`create_engine.poolclass`](core_engines.html#sqlalchemy.create_engine.params.poolclass "sqlalchemy.create_engine")
parameter; the [`StaticPool`](core_pooling.html#sqlalchemy.pool.StaticPool "sqlalchemy.pool.StaticPool")
may be more feasible for single-threaded use, or [`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")
may be used to prevent unencrypted connections from being held open for
long periods of time, at the expense of slower startup time for new
connections.
