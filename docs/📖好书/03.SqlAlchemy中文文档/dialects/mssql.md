---
title: Microsoft SQL Server
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/dialects/mssql/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - dialects
tags:
  - 
---
Microsoft SQL Server [¶](#module-sqlalchemy.dialects.mssql.base "Permalink to this headline")
=============================================================================================

支持 Microsoft SQL Server 数据库。

DBAPI支持[¶](#dialect-mssql "Permalink to this headline")
---------------------------------------------------------

以下 dialect / DBAPI 选项可用。请参阅各个 DBAPI 部分的连接信息。

-   [PyODBC T0\>](#module-sqlalchemy.dialects.mssql.pyodbc)
-   [mxODBC T0\>](#module-sqlalchemy.dialects.mssql.mxodbc)
-   [pymssql T0\>](#module-sqlalchemy.dialects.mssql.pymssql)
-   Jython 的[zxJDBC](#module-sqlalchemy.dialects.mssql.zxjdbc)
-   [adodbapi T0\>](#module-sqlalchemy.dialects.mssql.adodbapi)

自动增量行为[¶](#auto-increment-behavior "Permalink to this headline")
----------------------------------------------------------------------

SQL Server 使用`IDENTITY`结构提供所谓的“自动递增”行为，该结构可放置在整数主键上。SQLAlchemy 在[`Column.autoincrement`](core_metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")中描述的默认“autoincrement”行为内考虑`IDENTITY`；这意味着默认情况下，[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的第一个整数主键列将被视为标识列，并将生成 DDL：

    from sqlalchemy import Table, MetaData, Column, Integerplain

    m = MetaData()
    t = Table('t', m,
            Column('id', Integer, primary_key=True),
            Column('x', Integer))
    m.create_all(engine)

上面的例子将生成DDL：

    CREATE TABLE t (
        id INTEGER NOT NULL IDENTITY(1,1),
        x INTEGER NULL,
        PRIMARY KEY (id)
    )

对于不需要此默认的`IDENTITY`生成的情况，请在所有整数主键列上指定`autoincrement=False`：

    m = MetaData()plainplain
    t = Table('t', m,
            Column('id', Integer, primary_key=True, autoincrement=False),
            Column('x', Integer))
    m.create_all(engine)

注意

SQL
Server 禁止引用此类列的显式值的 INSERT 语句，但 SQLAlchemy 将在语句执行时检测到此操作并相应地修改`IDENTITY_INSERT`标志。由于这不是一个高性能的进程，因此应该小心为实际上不需要 IDENTITY 行为的列设置`autoincrement`标志。

### 控制“开始”和“增量”[¶](#controlling-start-and-increment "Permalink to this headline")

使用[`schema.Sequence`](core_defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象支持对`IDENTITY`值参数的特定控制。虽然此对象通常表示支持后端的显式“序列”，但在 SQL
Server 上，它重新用于指定有关标识列的行为，包括对“开始”和“增量”值的支持：

    from sqlalchemy import Table, Integer, Sequence, Column

    Table('test', metadata,
           Column('id', Integer,
                  Sequence('blah', start=100, increment=10),
                  primary_key=True),
           Column('name', String(20))
         ).create(some_engine)

会产生：

    CREATE TABLE test (plainplain
      id INTEGER NOT NULL IDENTITY(100,10) PRIMARY KEY,
      name VARCHAR(20) NULL,
      )

请注意，序列的`start`和`increment`值是可选的，默认值为 1,1。

### INSERT 行为[¶](#insert-behavior "Permalink to this headline")

在 INSERT 时间处理`IDENTITY`列涉及两个关键技术。最常见的是能够为给定的`IDENTITY`列获取“最后插入的值”，这是 SQLAlchemy 在很多情况下隐式执行的过程，最重要的是在 ORM 中执行。

获取此值的过程有几个变体：

-   在绝大多数情况下，RETURNING 与 SQL
    Server 上的 INSERT 语句一起使用以获取新生成的主键值：

        INSERT INTO t (x) OUTPUT inserted.id VALUES (?)plain

-   当 RETURNING 不可用或已通过`implicit_returning=False`禁用时，使用`scope_identity()`函数或`@@identity`变量；行为因后端而异：

    -   when using PyODBC, the phrase
        `; select scope_identity()` will be appended
        to the end of the INSERT statement; a second result set will be
        fetched in order to receive the value. 给定一个表格为：

            t = Table('t', m, Column('id', Integer, primary_key=True),plainplain
                    Column('x', Integer),
                    implicit_returning=False)

        INSERT将如下所示：

            INSERT INTO t (x) VALUES (?); select scope_identity()plain

    -   Other dialects such as pymssql will call upon
        `SELECT scope_identity() AS lastrowid`
        subsequent to an INSERT statement. If the flag
        `use_scope_identity=False` is passed to
        [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine"),
        the statement `SELECT @@identity AS lastrowid` is used instead.

包含`IDENTITY`列的表将禁止显式引用标识列的 INSERT 语句。The SQLAlchemy dialect
will detect when an INSERT construct, created using a core
[`insert()`](postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")
construct (not a plain string SQL), refers to the identity column, and
in this case will emit `SET IDENTITY_INSERT ON`
prior to the insert statement proceeding, and
`SET IDENTITY_INSERT OFF` subsequent to the
execution. 给出这个例子：

    m = MetaData()
    t = Table('t', m, Column('id', Integer, primary_key=True),
                    Column('x', Integer))
    m.create_all(engine)

    engine.execute(t.insert(), {'id': 1, 'x':1}, {'id':2, 'x':2})

上面的列将使用 IDENTITY 创建，但是我们发出的 INSERT 语句指定了明确的值。在 echo 输出中，我们可以看到 SQLAlchemy 如何处理这个问题：

    CREATE TABLE t (
        id INTEGER NOT NULL IDENTITY(1,1),
        x INTEGER NULL,
        PRIMARY KEY (id)
    )

    COMMIT
    SET IDENTITY_INSERT t ON
    INSERT INTO t (id, x) VALUES (?, ?)
    ((1, 1), (2, 2))
    SET IDENTITY_INSERT t OFF
    COMMIT

这是适用于测试和批量插入场景的辅助用例。

整理支持[¶](#collation-support "Permalink to this headline")
------------------------------------------------------------

字符排序规则由基本字符串类型支持，由字符串参数“排序规则”指定：

    from sqlalchemy import VARCHARplain
    Column('login', VARCHAR(32, collation='Latin1_General_CI_AS'))

当这样的列与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联时，此列的 CREATE
TABLE 语句将产生：

    login VARCHAR(32) COLLATE Latin1_General_CI_AS NULLplain

版本 0.8 中的新功能：字符归类现在是基本字符串类型的一部分。

LIMIT / OFFSET 支持[¶](#limit-offset-support "Permalink to this headline")
-------------------------------------------------------------------------

MSSQL 不支持 LIMIT 或 OFFSET 关键字。LIMIT 通过`TOP`
Transact SQL 关键字直接支持：

    select.limitplainplain

会产生：

    SELECT TOP nplain

如果使用 SQL Server 2005 或更高版本，可通过`ROW_NUMBER OVER`结构使用支持 OFFSET 的 LIMIT。对于 2005 以下的版本，使用 OFFSET 的 LIMIT 将失败。

事务隔离级别[¶](#transaction-isolation-level "Permalink to this headline")
--------------------------------------------------------------------------

All SQL Server dialects support setting of transaction isolation level
both via a dialect-specific parameter
[`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")
accepted by [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine"),
as well as the [`Connection.execution_options.isolation_level`(core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")
argument as passed to [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options").
该功能通过发出命令`SET TRANSACTION ISOLATION LEVEL  tt> ＆lt； level＆gt； / t5>`为每个新的连接。

使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")设置隔离级别：

    engine = create_engine(plainplain
        "mssql+pyodbc://scott:tiger@ms_2008",
        isolation_level="REPEATABLE READ"
    )

要设置使用每个连接执行选项：

    connection = engine.connect()plain
    connection = connection.execution_options(
        isolation_level="READ COMMITTED"
    )

`isolation_level`的有效值包括：

-   `READ COMMITTED`
-   `READ UNCOMMITTED`
-   `REPEATABLE READ`
-   `SERIALIZABLE`
-   `SNAPSHOT` - 特定于 SQL Server

版本 1.1 中的新功能：支持 Microsoft SQL Server 上的隔离级别设置。

为空[¶ T0\>](#nullability "Permalink to this headline")
-------------------------------------------------------

MSSQL 支持三级列可空性。默认的可空性允许空值，并且在 CREATE
TABLE 结构中是显式的：

    name VARCHAR(20) NULLplain

如果`nullable=None`被指定，那么没有指定。换句话说，使用数据库的配置默认值。这将呈现：

    name VARCHAR(20)plainplainplain

如果`nullable`是`True`或`False`那么该列将是`NULL`或`t9> NULL`。

日期/时间处理[¶](#date-time-handling "Permalink to this headline")
------------------------------------------------------------------

DATE 和 TIME 均受支持。绑定参数按照大多数 MSSQL 驱动程序的要求转换为 datetime.datetime()对象，并根据需要从字符串处理结果。DATE 和 TIME 类型不适用于 MSSQL
2005 和以前 -
如果检测到 2008 以下的服务器版本，则这些类型的 DDL 将作为 DATETIME 发布。

大文本/二进制类型不赞成[¶](#large-text-binary-type-deprecation "Permalink to this headline")
--------------------------------------------------------------------------------------------

根据[SQL Server 2012/2014
Documentation](http://technet.microsoft.com/en-us/library/ms187993.aspx)，`NTEXT`，`TEXT`和`IMAGE`数据类型将从 SQL
Server 在未来的版本中。SQLAlchemy 通常将这些类型与[`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")，[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")和[`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")数据类型相关联。

为了适应这种变化，一个新的标志`deprecate_large_types`被添加到方言中，如果没有用户设置，它将根据检测到的服务器版本自动设置。此标志的行为如下所示：

-   当此标志为`True`时，[`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")，[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")和[`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")数据类型在用于呈现 DDL 时，分别是`NVARCHAR(max)`，`VARCHAR(max)`和`VARBINARY(max)`类型。这是添加此标志后的新行为。

-   当此标志为`False`时，[`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")，[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")和[`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")数据类型在渲染 DDL 时将渲染类型分别为`NTEXT`，`TEXT`和`IMAGE`。这是这些类型的长期行为。

-   在数据库连接建立之前，该标志以`None`值开始。如果方言用于在未设置标志的情况下呈现 DDL，则它被解释为与`False`相同。

-   在第一次连接时，方言检测 SQL
    Server 版本 2012 或更高版本是否正在使用；如果标志仍然在`None`，则根据是否检测到 2012 或更高，将其设置为`True`或`False`。

-   创建方言时，通常可以通过[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")将标志设置为`True`或`False`：

        eng = create_engine("mssql+pymssql://user:pass@host/db",
                        deprecate_large_types=True)

-   通过使用大写类型对象来完全控制所有 SQLAlchemy 版本是否呈现“旧”或“新”类型：[`NVARCHAR`](core_type_basics.html#sqlalchemy.types.NVARCHAR "sqlalchemy.types.NVARCHAR")，[`VARCHAR`](mysql.html#sqlalchemy.dialects.mysql.VARCHAR "sqlalchemy.dialects.mysql.VARCHAR")，[`types.VARBINARY`](core_type_basics.html#sqlalchemy.types.VARBINARY "sqlalchemy.types.VARBINARY")，[`TEXT`](core_type_basics.html#sqlalchemy.types.TEXT "sqlalchemy.types.TEXT")，[`mssql.NTEXT`](#sqlalchemy.dialects.mssql.NTEXT "sqlalchemy.dialects.mssql.NTEXT")，[`mssql.IMAGE`](#sqlalchemy.dialects.mssql.IMAGE "sqlalchemy.dialects.mssql.IMAGE")将始终保持固定并始终输出该类型。

版本 1.0.0 中的新功能

传统架构模式[¶](#legacy-schema-mode "Permalink to this headline")
-----------------------------------------------------------------

非常旧的 MSSQL 方言版本引入了这样的行为：在 SELECT 语句中使用时，限定模式的表将被自动替换；给出一张表格：

    account_table = Table(plain
        'account', metadata,
        Column('id', Integer, primary_key=True),
        Column('info', String(100)),
        schema="customer_schema"
    )

这种传统的渲染模式会假设“customer\_schema.account”不会被 SQL 语句的所有部分所接受，如下所示：

    >>> eng = create_engine("mssql+pymssql://mydsn", legacy_schema_aliasing=True)plain
    >>> print(account_table.select().compile(eng))
    SELECT account_1.id, account_1.info
    FROM customer_schema.account AS account_1

这种行为模式现在是默认关闭的，因为它似乎没有任何用处；但是在传统应用程序依赖它的情况下，如上所述，它可以使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的`legacy_schema_aliasing`参数。

在版本 1.1 中更改：版本 1.0.5 中引入的`legacy_schema_aliasing`标志允许禁用模式的传统模式现在默认为False。

聚簇索引支持[¶](#clustered-index-support "Permalink to this headline")
----------------------------------------------------------------------

MSSQL 方言通过`mssql_clustered`选项支持聚簇索引（和主键）。此选项可用于[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")，[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")。和[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")。

要生成聚簇索引：

    Index("my_index", table.c.x, mssql_clustered=True)

它将索引呈现为`CREATE CLUSTERED INDEX my_index ON  table （x）`。

要生成群集主键，请使用：

    Table('my_table', metadata,plain
          Column('x', ...),
          Column('y', ...),
          PrimaryKeyConstraint("x", "y", mssql_clustered=True))

例如，它将呈现该表格，如下所示：

    CREATE TABLE my_table (x INTEGER NOT NULL, y INTEGER NOT NULL,
                           PRIMARY KEY CLUSTERED (x, y))

同样，我们可以使用以下命令生成聚集的唯一约束：

    Table('my_table', metadata,
          Column('x', ...),
          Column('y', ...),
          PrimaryKeyConstraint("x"),
          UniqueConstraint("y", mssql_clustered=True),
          )

要显式请求非集群主键（例如，当需要单独的集群索引时），请使用：

    Table('my_table', metadata,plain
          Column('x', ...),
          Column('y', ...),
          PrimaryKeyConstraint("x", "y", mssql_clustered=False))

例如，它将呈现该表格，如下所示：

    CREATE TABLE my_table (x INTEGER NOT NULL, y INTEGER NOT NULL,plain
                           PRIMARY KEY NONCLUSTERED (x, y))

在版本 1.1 中更改： `mssql_clustered`选项现在默认为 None，而不是 False。`mssql_clustered=False`现在显式呈现 NONCLUSTERED 子句，而 None 完全忽略 CLUSTERED 子句，从而允许 SQL
Server 默认设置生效。

MSSQL 特定的索引选项[¶](#mssql-specific-index-options "Permalink to this headline")
----------------------------------------------------------------------------------

除集群之外，MSSQL 方言支持[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的其他特殊选项。

### INCLUDE [¶ T0\>](#include "Permalink to this headline")

`mssql_include`选项为给定的字符串名称呈现INCLUDE（colname）：

    Index("my_index", table.c.x, mssql_include=['y'])plain

将使该指数为`创建 T1>  INDEX  T2>  my_index  T3>  ON  T4> 表 T5> （x） INCLUDE （y）`

0.8 版本中的新功能

### 索引排序[¶](#index-ordering "Permalink to this headline")

索引排序可通过函数表达式获得，例如：

    Index("my_index", table.c.x.desc())plain

would render the index as
`CREATE INDEX my_index ON table (x DESC)`

0.8 版本中的新功能

也可以看看

[Functional Indexes](core_constraints.html#schema-indexes-functional)

兼容级别[¶](#compatibility-levels "Permalink to this headline")
---------------------------------------------------------------

MSSQL 支持在数据库级别设置兼容级别的概念。例如，这允许在 SQL2005 数据库服务器上运行时运行与 SQL2000 兼容的数据库。`server_version_info` will always return the database server version information (in
this case SQL2005) and not the compatibility level information.
因此，如果在向后兼容模式下运行，SQAlchemy 可能会尝试使用无法由数据库服务器分析的 T-SQL 语句。

触发器[¶ T0\>](#triggers "Permalink to this headline")
------------------------------------------------------

SQLAlchemy 默认使用 OUTPUT
INSERTED 通过 IDENTITY 列或其他服务器端默认值获取新生成的主键值。MS-SQL 不允许在具有触发器的表上使用 OUTPUT
INSERTED。要禁用每个表的 OUTPUT INSERTED 用法，请为每个[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")指定`implicit_returning=False`

    Table('mytable', metadata,plain
        Column('id', Integer, primary_key=True),
        # ...,
        implicit_returning=False
    )

声明形式：

    class MyClass(Base):
        # ...
        __table_args__ = {'implicit_returning':False}

此选项也可以在[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")中使用`implicit_returning=False`参数在整个引擎范围内指定。

Rowcount 支持/ ORM 版本控制[¶](#rowcount-support-orm-versioning "Permalink to this headline")
-------------------------------------------------------------------------------------------

SQL
Server 驱动程序具有非常有限的能力来返回从 UPDATE 或 DELETE 语句更新的行数。特别是，pymssql 驱动程序不支持，而 pyodbc 驱动程序只能在特定条件下返回此值。

特别是，当使用 OUTPUT
INSERTED 时，更新的 rowcount 不可用。这会在使用服务器端版本控制方案时影响 SQLAlchemy
ORM 的版本控制功能。在使用 pyodbc 时，对于使用 version\_id 列与服务器端版本生成器结合使用的任何 ORM 映射类，需要将“implicit\_returning”标志设置为 false：

    class MyTable(Base):plain
        __tablename__ = 'mytable'
        id = Column(Integer, primary_key=True)
        stuff = Column(String(10))
        timestamp = Column(TIMESTAMP(), default=text('DEFAULT'))
        __mapper_args__ = {
            'version_id_col': timestamp,
            'version_id_generator': False,
        }
        __table_args__ = {
            'implicit_returning': False
        }

如果没有上面的 implicit\_returning 标志，那么 UPDATE 语句将使用`OUTPUT inserted.timestamp`，并且 rowcount 将返回-1，导致版本控制逻辑失败。

启用快照隔离[¶](#enabling-snapshot-isolation "Permalink to this headline")
--------------------------------------------------------------------------

不一定特定于 SQLAlchemy，SQL
Server 具有默认的事务隔离模式，可以锁定整个表，甚至可以使并发轻微并发的应用程序长期持有锁和频繁死锁。对于现代级别的并发支持，建议为整个数据库启用快照隔离。这是通过在 SQL 提示符下执行的以下 ALTER
DATABASE 命令完成的：

    ALTER DATABASE MyDatabase SET ALLOW_SNAPSHOT_ISOLATION ON

    ALTER DATABASE MyDatabase SET READ_COMMITTED_SNAPSHOT ON

有关 SQL
Server 快照隔离的背景信息，请访问[http://msdn.microsoft.com/en-us/library/ms175095.aspx](http://msdn.microsoft.com/en-us/library/ms175095.aspx)。

已知问题[¶](#known-issues "Permalink to this headline")
-------------------------------------------------------

-   每个表不支持多个`IDENTITY`列
-   索引的反映不适用于早于 SQL Server 2005 的版本

SQL Server数据类型[¶](#sql-server-data-types "Permalink to this headline")
--------------------------------------------------------------------------

与所有 SQLAlchemy 方言一样，所有已知可用于 SQL
Server 的 UPPERCASE 类型都可以从顶级方言导入，无论它们来源于[`sqlalchemy.types`](core_type_basics.html#module-sqlalchemy.types "sqlalchemy.types")还是来自本地方言：

    from sqlalchemy.dialects.mssql import \plainplain
        BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
        DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
        NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
        SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
        TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR

特定于 SQL Server 的类型或 SQL Server 特定的构造参数如下所示：

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `BIT`{.descname} [¶](#sqlalchemy.dialects.mssql.BIT "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}plain
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

 *class*`sqlalchemy.dialects.mssql.`{.descclassname}`CHAR`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.CHAR "Permalink to this definition")
:   基础：[`sqlalchemy.types.String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

    SQL CHAR类型。

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.CHAR.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.String.__init__ "sqlalchemy.types.String.__init__")
        *method of* [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

        创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.mssql.CHAR.params.length)
            – optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理**
            [¶](#sqlalchemy.dialects.mssql.CHAR.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.dialects.mssql.CHAR.params.convert_unicode)
            -

            当设置为`True`时，[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")类型将假定输入将作为Python
            `unicode`对象传递，结果以Python
            `unicode`对象。If the DBAPI in use does
            not support Python unicode (which is fewer and fewer these
            days), SQLAlchemy will encode/decode the value, using the
            value of the `encoding` parameter passed
            to [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
            as the encoding.

            当使用本地支持Python
            unicode对象的DBAPI时，通常不需要设置此标志。For columns that
            are explicitly intended to store non-ASCII data, the
            [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            or [`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")
            types should be used regardless, which feature the same
            behavior of `convert_unicode` but also
            indicate an underlying column type that directly supports
            unicode, such as `NVARCHAR`.

            对于非常罕见的情况，Python `unicode`将由本地支持Python `unicode`的后端由SQLAlchemy编码/解码，值`force`可以在这里传递，这将导致无条件地使用SQLAlchemy的编码/解码服务。

        -   **unicode\_error**
            [¶](#sqlalchemy.dialects.mssql.CHAR.params.unicode_error) -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `DATETIME2`{.descname} （ *precision = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.DATETIME2 "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mssql.base._DateTimeBase`，[`sqlalchemy.types.DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `DATETIMEOFFSET`{.descname} （ *precision = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.DATETIMEOFFSET "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

 *class*`sqlalchemy.dialects.mssql.`{.descclassname}`IMAGE`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.mssql.IMAGE "Permalink to this definition")
:   基础：[`sqlalchemy.types.LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.LargeBinary.__init__ "sqlalchemy.types.LargeBinary.__init__")
        *method of* [`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

        构建一个LargeBinary类型。

        参数：

        **length**[¶](#sqlalchemy.dialects.mssql.IMAGE.params.length) –
        optional, a length for the column for use in DDL statements, for
        those binary types that accept a length, such as the MySQL BLOB
        type.

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `MONEY`{.descname} [¶](#sqlalchemy.dialects.mssql.MONEY "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}plainplain
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `NCHAR`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.NCHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

    SQL NCHAR类型。plain

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mssql.NCHAR.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.Unicode.__init__ "sqlalchemy.types.Unicode.__init__")
        *method of* [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

        创建一个[`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")对象。

        参数与[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")的参数相同，不同的是`convert_unicode`默认为`True`。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `NTEXT`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.NTEXT "Permalink to this definition")*
:   基础：[`sqlalchemy.types.UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")

    MSSQL NTEXT类型，用于最多2 \^ 30个字符的可变长度unicode文本。plainplain

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mssql.NTEXT.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.UnicodeText.__init__ "sqlalchemy.types.UnicodeText.__init__")
        *method of* [`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")

        创建一个Unicode转换文本类型。

        参数与[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")相同，但`convert_unicode`默认为`True`。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `NVARCHAR`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.NVARCHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

    SQL NVARCHAR类型。plain

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mssql.NVARCHAR.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.Unicode.__init__ "sqlalchemy.types.Unicode.__init__")
        *method of* [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

        创建一个[`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")对象。

        参数与[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")的参数相同，不同的是`convert_unicode`默认为`True`。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `REAL`{.descname} （ *\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mssql.REAL "Permalink to this definition")
:   基础：[`sqlalchemy.types.REAL`](core_type_basics.html#sqlalchemy.types.REAL "sqlalchemy.types.REAL")

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `SMALLDATETIME`{.descname} （ *timezone = False* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mssql.SMALLDATETIME "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mssql.base._DateTimeBase`，[`sqlalchemy.types.DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

    ` __初始化__  T0> （ T1> 时区=假 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的
        [`__init__()`](core_type_basics.html#sqlalchemy.types.DateTime.__init__ "sqlalchemy.types.DateTime.__init__")
        **

        构建一个新的[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")。

        参数：

        **时区**
        [¶](#sqlalchemy.dialects.mssql.SMALLDATETIME.params.timezone) -
        布尔值。如果为True，并由后端支持，则会产生'TIMESTAMP WITH
        TIMEZONE'。对于不支持时区感知时间戳的后端，不起作用。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `SMALLMONEY`{.descname} [¶](#sqlalchemy.dialects.mssql.SMALLMONEY "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}plain
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `SQL_VARIANT`{.descname} [¶](#sqlalchemy.dialects.mssql.SQL_VARIANT "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}plain
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

 *class*`sqlalchemy.dialects.mssql.`{.descclassname}`TEXT`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.TEXT "Permalink to this definition")
:   基础：[`sqlalchemy.types.Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")

    SQL TEXT类型。plain

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.TEXT.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.String.__init__ "sqlalchemy.types.String.__init__")
        *method of* [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

        创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.mssql.TEXT.params.length)
            – optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理**
            [¶](#sqlalchemy.dialects.mssql.TEXT.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.dialects.mssql.TEXT.params.convert_unicode)
            -

            当设置为`True`时，[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")类型将假定输入将作为Python
            `unicode`对象传递，结果以Python
            `unicode`对象。If the DBAPI in use does
            not support Python unicode (which is fewer and fewer these
            days), SQLAlchemy will encode/decode the value, using the
            value of the `encoding` parameter passed
            to [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
            as the encoding.

            当使用本地支持Python
            unicode对象的DBAPI时，通常不需要设置此标志。For columns that
            are explicitly intended to store non-ASCII data, the
            [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            or [`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")
            types should be used regardless, which feature the same
            behavior of `convert_unicode` but also
            indicate an underlying column type that directly supports
            unicode, such as `NVARCHAR`.

            对于非常罕见的情况，Python `unicode`将由本地支持Python `unicode`的后端由SQLAlchemy编码/解码，值`force`可以在这里传递，这将导致无条件地使用SQLAlchemy的编码/解码服务。

        -   **unicode\_error**
            [¶](#sqlalchemy.dialects.mssql.TEXT.params.unicode_error) -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `TIME`{.descname} （ *precision = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mssql.TIME "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TIME`](core_type_basics.html#sqlalchemy.types.TIME "sqlalchemy.types.TIME")

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `TINYINT`{.descname} [¶](#sqlalchemy.dialects.mssql.TINYINT "Permalink to this definition")
:   基础：[`sqlalchemy.types.Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.mssql。`{.descclassname} `UNIQUEIDENTIFIER`{.descname} [¶](#sqlalchemy.dialects.mssql.UNIQUEIDENTIFIER "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}plainplain
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

 *class*`sqlalchemy.dialects.mssql.`{.descclassname}`VARCHAR`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.VARCHAR "Permalink to this definition")
:   基础：[`sqlalchemy.types.String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

    SQL VARCHAR类型。plain

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.mssql.VARCHAR.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.String.__init__ "sqlalchemy.types.String.__init__")
        *method of* [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

        创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.mssql.VARCHAR.params.length)
            – optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理**
            [¶](#sqlalchemy.dialects.mssql.VARCHAR.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.dialects.mssql.VARCHAR.params.convert_unicode)
            -

            当设置为`True`时，[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")类型将假定输入将作为Python
            `unicode`对象传递，结果以Python
            `unicode`对象。If the DBAPI in use does
            not support Python unicode (which is fewer and fewer these
            days), SQLAlchemy will encode/decode the value, using the
            value of the `encoding` parameter passed
            to [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
            as the encoding.

            当使用本地支持Python
            unicode对象的DBAPI时，通常不需要设置此标志。For columns that
            are explicitly intended to store non-ASCII data, the
            [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            or [`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")
            types should be used regardless, which feature the same
            behavior of `convert_unicode` but also
            indicate an underlying column type that directly supports
            unicode, such as `NVARCHAR`.

            对于非常罕见的情况，Python `unicode`将由本地支持Python `unicode`的后端由SQLAlchemy编码/解码，值`force`可以在这里传递，这将导致无条件地使用SQLAlchemy的编码/解码服务。

        -   **unicode\_error**
            [¶](#sqlalchemy.dialects.mssql.VARCHAR.params.unicode_error)
            -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

PyODBC [¶ T0\>](#module-sqlalchemy.dialects.mssql.pyodbc "Permalink to this headline")
--------------------------------------------------------------------------------------

通过 PyODBC 驱动程序支持 Microsoft SQL Server 数据库。

### DBAPI [¶ T0\>](#dialect-mssql-pyodbc-url "Permalink to this headline")

PyODBC 的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/pyodbc/](http://pypi.python.org/pypi/pyodbc/)

### 连接[¶ T0\>](#dialect-mssql-pyodbc-connect "Permalink to this headline")

连接字符串：

    mssql+pyodbc://<username>:<password>@<dsnname>plainplain

### 连接到PyODBC [¶](#connecting-to-pyodbc "Permalink to this headline")

此处的 URL 将被转换为 PyODBC 连接字符串，详见[ConnectionStrings](https://code.google.com/p/pyodbc/wiki/ConnectionStrings)。

#### DSN连接[¶](#dsn-connections "Permalink to this headline")

A DSN-based connection is **preferred** overall when using ODBC.
基本的基于DSN的连接如下所示：

    engine = create_engine("mssql+pyodbc://scott:tiger@some_dsn")

上面哪个，将下面的连接字符串传递给 PyODBC：

    dsn=mydsn;UID=user;PWD=passplain

如果省略用户名和密码，则 DSN 表格还会将`Trusted_Connection=yes`指令添加到 ODBC 字符串中。

#### 主机名连接[¶](#hostname-connections "Permalink to this headline")

基于主机名的连接**不是首选**，但是受支持。ODBC 驱动程序名称必须明确指定：

    engine = create_engine("mssql+pyodbc://scott:tiger@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0")plain

版本 1.0.0 中已更改：现在，基于主机名的 PyODBC 连接需要明确指定的 SQL
Server 驱动程序名称。由于 SQLAlchemy 根据平台和安装的驱动程序而有所不同，SQLAlchemy 无法选择最佳默认值。

由 Pyodbc 方言解释的其他关键字在 DSN 和主机名情况下都被传递给`pyodbc.connect()`包括：`odbc_autotranslate`，`ansi`， `unicode_results`，`autocommit`。

#### 通过精确的 Pyodbc 字符串[¶](#pass-through-exact-pyodbc-string "Permalink to this headline")

PyODBC 连接字符串也可以使用参数`odbc_connect`完全按照[ConnectionStrings](https://code.google.com/p/pyodbc/wiki/ConnectionStrings)中的规定发送到驱动程序中。但是，使用`urllib.quote_plus`时，定界符必须是 URL 转义的：

    import urllibplainplain
    params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=dagger;DATABASE=test;UID=user;PWD=password")

    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

### Unicode绑定[¶](#unicode-binds "Permalink to this headline")

关于 unicode，PyTBC 在 FreeTDS 和/或 EasySoft 后端的当前状态很差；不同操作系统平台和版本的 UnixODBC 与 IODBC 与 FreeTDS
/
EasySoft 相比，PyODBC 本身会显着改变字符串的接收方式。PyODBC 方言尝试使用它所知道的所有信息来确定是否可以将 Python
unicode 文字直接传递给 PyODBC 驱动程序；虽然 SQLAlchemy 可以首先将它们编码为字节串，但有些用户报告说 PyODBC 对某些编码的字节串错误处理，并且需要一个 Python
unicode 对象，而作者观察到 python
unicode 完全被 PyODBC 误解的普遍情况，特别是在处理表反射中使用的信息模式表，并且必须首先将该值编码为字符串。

正是由于这个原因，可以使用`supports_unicode_binds`参数控制`create_engine()`来控制是否将绑定参数的 unicode 文字发送到 PyODBC。当默认值为`None`时，PyODBC 方言将使用最佳猜测来判断驱动程序是否处理 unicode 字面值。当`False`时，unicode文字将首先被编码，并且`True`
unicode 文字将被直接传递。这是一个临时标志，当 unix +
PyODBC 的 unicode 情况稳定时，希望不需要该标志。

New in version 0.7.7: `supports_unicode_binds`
parameter to `create_engine()`.

### Rowcount 支持[¶](#rowcount-support "Permalink to this headline")

Pyodbc 只支持 rowcount。在使用 ORM 版本控制时，请参阅[Rowcount Support / ORM
Versioning](#mssql-rowcount-versioning)中的说明以了解重要说明。

mxODBC [¶ T0\>](#module-sqlalchemy.dialects.mssql.mxodbc "Permalink to this headline")
--------------------------------------------------------------------------------------

通过 mxODBC 驱动程序支持 Microsoft SQL Server 数据库。

### DBAPI [¶ T0\>](#dialect-mssql-mxodbc-url "Permalink to this headline")

mxODBC 的文档和下载信息（如果适用）可在以下网址获得：[http://www.egenix.com/](http://www.egenix.com/)

### 连接[¶ T0\>](#dialect-mssql-mxodbc-connect "Permalink to this headline")

连接字符串：

    mssql+mxodbc://<username>:<password>@<dsnname>

### 执行模式[¶](#execution-modes "Permalink to this headline")

mxODBC使用`cursor.execute()`和`cursor.executedirect()`方法（第二种是 DBAPI 规范的扩展）提供了两种语句执行风格。前者使用特定于 SQL
Server Native Client
ODBC 驱动程序的特定 API 调用（已知 SQLDescribeParam），而后者则不使用。

当使用 SQLDescribeParam 时，mxODBC 显然只会重复使用单个预准备语句。准备语句重用的好处是性能。缺点是 SQLDescribeParam 的绑定参数被理解为有限的一组场景，包括它们不能放在函数调用的参数列表中，在 FROM 之外的任何地方，或者甚至在 FROM 子句内的子查询中
- 使得在 SELECT 语句中绑定参数是不可能的，除了最简单的陈述之外。

因此，默认情况下，mxODBC 方言默认只使用 INSERT，UPDATE 和 DELETE 语句的“本机”模式，对所有其他语句使用转义字符串模式。

This behavior can be controlled via [`execution_options()`](core_selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
using the `native_odbc_execute` flag with a value of
`True` or `False`, where a value
of `True` will unconditionally use native bind
parameters and a value of `False` will
unconditionally use string-escaped parameters.

pymssql [¶ T0\>](#module-sqlalchemy.dialects.mssql.pymssql "Permalink to this headline")
----------------------------------------------------------------------------------------

通过 pymssql 驱动程序支持 Microsoft SQL Server 数据库。

### DBAPI [¶ T0\>](#dialect-mssql-pymssql-url "Permalink to this headline")

pymssql 的文档和下载信息（如果适用）可在以下网址获得：[http://pymssql.org/](http://pymssql.org/)

### 连接[¶ T0\>](#dialect-mssql-pymssql-connect "Permalink to this headline")

连接字符串：

    mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8

pymssql 是一个 Python 模块，它提供围绕[FreeTDS](http://www.freetds.org/)的 Python
DBAPI 接口。兼容版本适用于 Linux，MacOSX 和 Windows 平台。

zxjdbc [¶ T0\>](#module-sqlalchemy.dialects.mssql.zxjdbc "Permalink to this headline")
--------------------------------------------------------------------------------------

通过 zxJDBC 为 Jython 驱动程序支持 Microsoft SQL Server 数据库。

注意

当前版本的 SQLAlchemy 不支持 Jython。zxjdbc 方言应该被认为是实验性的。

### DBAPI [¶ T0\>](#dialect-mssql-zxjdbc-url "Permalink to this headline")

此数据库的驱动程序可在以下网站获得：[http://jtds.sourceforge.net/](http://jtds.sourceforge.net/)

### 连接[¶ T0\>](#dialect-mssql-zxjdbc-connect "Permalink to this headline")

连接字符串：

    mssql+zxjdbc://user:pass@host:port/dbname[?key=value&key=value...]

AdoDBAPI [¶ T0\>](#module-sqlalchemy.dialects.mssql.adodbapi "Permalink to this headline")
------------------------------------------------------------------------------------------

通过 adodbapi 驱动程序支持 Microsoft SQL Server 数据库。

### DBAPI [¶ T0\>](#dialect-mssql-adodbapi-url "Permalink to this headline")

有关 adodbapi 的文档和下载信息（如果适用），请访问：[http://adodbapi.sourceforge.net/](http://adodbapi.sourceforge.net/)

### 连接[¶ T0\>](#dialect-mssql-adodbapi-connect "Permalink to this headline")

连接字符串：

    mssql+adodbapi://<username>:<password>@<dsnname>plain

注意

adodbapi 方言目前尚未实现 SQLAlchemy 0.6 及更高版本。
