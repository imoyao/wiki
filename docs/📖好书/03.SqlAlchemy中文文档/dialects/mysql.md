---
title: mysql
date: 2021-02-20 22:41:37
permalink: /pages/6326fd/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - dialects
tags:
  - 
---
MySQL的[¶ T0\>](#module-sqlalchemy.dialects.mysql.base "Permalink to this headline")
====================================================================================

支持MySQL数据库。

DBAPI支持[¶](#dialect-mysql "Permalink to this headline")
---------------------------------------------------------

以下dialect / DBAPI选项可用。请参阅各个DBAPI部分的连接信息。

-   [的MySQL的Python T0\>](#module-sqlalchemy.dialects.mysql.mysqldb)
-   [PyMySQL T0\>](#module-sqlalchemy.dialects.mysql.pymysql)
-   [MySQL连接器/
    Python](#module-sqlalchemy.dialects.mysql.mysqlconnector)
-   [CyMySQL T0\>](#module-sqlalchemy.dialects.mysql.cymysql)
-   [OurSQL T0\>](#module-sqlalchemy.dialects.mysql.oursql)
-   [Google Cloud SQL](#module-sqlalchemy.dialects.mysql.gaerdbms)
-   [PyODBC T0\>](#module-sqlalchemy.dialects.mysql.pyodbc)
-   Jython的[zxjdbc](#module-sqlalchemy.dialects.mysql.zxjdbc)

支持的版本和功能[¶](#supported-versions-and-features "Permalink to this headline")
----------------------------------------------------------------------------------

SQLAlchemy通过现代版本支持从4.1版本开始的MySQL。但是，如果您的服务器版本不支持子选择，则不会采取英雄措施解决主要缺失的SQL功能，例如，它们也不会在SQLAlchemy中工作。

有关任何给定服务器版本中支持的功能的详细信息，请参阅官方的MySQL文档。

连接超时[¶](#connection-timeouts "Permalink to this headline")
--------------------------------------------------------------

MySQL具有自动连接关闭行为，适用于闲置八小时或更长时间的连接。为了避免发生此问题，请使用控制任何连接的最大使用期限的`pool_recycle`选项：

    engine = create_engine('mysql+mysqldb://...', pool_recycle=3600)

也可以看看

[Setting Pool Recycle](core_pooling.html#pool-setting-recycle) -
池回收功能的完整说明。

包含存储引擎的CREATE TABLE参数[¶](#create-table-arguments-including-storage-engines "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------

MySQL’s CREATE TABLE syntax includes a wide array of special options,
including `ENGINE`, `CHARSET`,
`MAX_ROWS`, `ROW_FORMAT`,
`INSERT_METHOD`, and many more.
要适应这些参数的呈现，请指定`mysql_argument_name="value"`形式。For example, to specify a table with `ENGINE` of `InnoDB`, `CHARSET`
of `utf8`, and `KEY_BLOCK_SIZE`
of `1024`:

    Table('mytable', metadata,
          Column('data', String(32)),
          mysql_engine='InnoDB',
          mysql_charset='utf8',
          mysql_key_block_size="1024"
         )

MySQL方言通常会将指定为`mysql_keyword_name`的任何关键字转换成`CREATE TABLE中的KEYWORD_NAME` \>语句。A handful of these names will render with a space
instead of an underscore; to support this, the MySQL dialect has
awareness of these particular names, which include
`DATA DIRECTORY` (e.g.
`mysql_data_directory`), `CHARACTER SET` (e.g. `mysql_character_set`) and
`INDEX DIRECTORY` (e.g.
`mysql_index_directory`).

最常见的参数是`mysql_engine`，它引用表的存储引擎。从历史上看，MySQL服务器安装默认为`MyISAM`，尽管新版本可能默认为`InnoDB`。The
`InnoDB` engine is typically preferred for its
support of transactions and foreign keys.

在具有`MyISAM`存储引擎的MySQL数据库中创建的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")将基本上是非事务性的，这意味着引用此表的任何INSERT
/ UPDATE /
DELETE语句将是被调用为自动提交。它也不会支持外键约束；而当使用`MyISAM`存储引擎时，`CREATE TABLE`语句接受外键选项，这些参数将被丢弃。反映这样的表格也不会产生外键约束信息。

For fully atomic transactions as well as support for foreign key
constraints, all participating `CREATE TABLE`
statements must specify a transactional engine, which in the vast
majority of cases is `InnoDB`.

也可以看看

[InnoDB存储引擎](http://dev.mysql.com/doc/refman/5.0/en/innodb-storage-engine.html)
- 在MySQL网站上。

区分大小写和表反射[¶](#case-sensitivity-and-table-reflection "Permalink to this headline")
------------------------------------------------------------------------------------------

MySQL对区分大小写的标识符名称提供了不一致的支持，基于对底层操作系统特定细节的支持。然而，据观察，无论出现什么样的大小写敏感性行为，外键声明中的表名都始终是*总是*从数据库接收为全小写，因此无法准确反映架构中相互关联的表使用混合大小写标识符名称。

因此，强烈建议在SQLAlchemy以及MySQL数据库本身中声明表名全部小写，尤其是在要使用数据库反射功能的情况下。

事务隔离级别[¶](#transaction-isolation-level "Permalink to this headline")
--------------------------------------------------------------------------

All MySQL dialects support setting of transaction isolation level both
via a dialect-specific parameter [`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")
accepted by [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine"),
as well as the [`Connection.execution_options.isolation_level`(core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")
argument as passed to [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options").
This feature works by issuing the command
`SET SESSION TRANSACTION ISOLATION LEVEL <level>`
for each new connection.
对于特殊的AUTOCOMMIT隔离级别，使用了特定于DBAPI的技术。

使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")设置隔离级别：

    engine = create_engine(
                    "mysql://scott:tiger@localhost/test",
                    isolation_level="READ UNCOMMITTED"
                )

要设置使用每个连接执行选项：

    connection = engine.connect()
    connection = connection.execution_options(
        isolation_level="READ COMMITTED"
    )

`isolation_level`的有效值包括：

-   `READ COMMITTED`
-   `READ UNCOMMITTED`
-   `REPEATABLE READ`
-   `SERIALIZABLE`
-   `AUTOCOMMIT`

特殊的`AUTOCOMMIT`值使用特定DBAPI提供的各种“autocommit”属性，目前支持MySQLdb，MySQL-Client，MySQL-Connector
Python和PyMySQL。使用它，MySQL连接将对`SELECT @@ autocommit；`的值返回true。

1.1版新增功能： - 增加了对AUTOCOMMIT隔离级别的支持。

AUTO\_INCREMENT行为[¶](#auto-increment-behavior "Permalink to this headline")
-----------------------------------------------------------------------------

创建表时，SQLAlchemy将在未标记为外键的第一个[`Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")主键列上自动设置`AUTO_INCREMENT`：

    >>> t = Table('mytable', metadata,
    ...   Column('mytable_id', Integer, primary_key=True)
    ... )
    >>> t.create()
    CREATE TABLE mytable (
            id INTEGER NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (id)
    )

您可以通过将`False`传递给[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的[`autoincrement`](core_metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")参数来禁用此行为。此标志还可用于启用某些存储引擎的多列键中辅助列的自动递增：

    Table('mytable', metadata,
          Column('gid', Integer, primary_key=True, autoincrement=False),
          Column('id', Integer, primary_key=True)
         )

Unicode的[¶ T0\>](#unicode "Permalink to this headline")
--------------------------------------------------------

### 字符集选择[¶](#charset-selection "Permalink to this headline")

大多数MySQL
DBAPI提供了为连接设置客户端字符集的选项。这通常通过URL中的`charset`参数提供，例如：

    e = create_engine("mysql+pymysql://scott:tiger@localhost/test?charset=utf8")

这个字符集是连接的**客户端字符集**。Some MySQL DBAPIs will default this
to a value such as `latin1`, and some will make use
of the `default-character-set` setting in the
`my.cnf` file as well.
应该查阅正在使用的DBAPI的文档以了解具体行为。

用于Unicode的编码传统上是`'utf8'`。但是，对于正向版本的MySQL
5.5.3，引入了一个新的特定于MySQL的编码`'utf8mb4'`。这种新编码的基本原理是由于MySQL的utf-8编码仅支持最多三个字节而不是四个的码位。因此，当与包含三个字节以上的代码点的MySQL数据库进行通信时，如果数据库和客户端DBAPI都支持，则这个新的字符集是首选的，如下所示：

    e = create_engine("mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4")

目前，MySQLdb和PyMySQL的最新版本支持`utf8mb4`字符集。其他DBAPI如MySQL-Connector和OurSQL可能**不能**支持它。

为了使用`utf8mb4`编码，可能需要更改MySQL架构和/或服务器配置。

也可以看看

[utf8mb4字符集](http://dev.mysql.com/doc/refman/5.5/en/charset-unicode-utf8mb4.html)
- 在MySQL文档中

### Unicode编码/解码[¶](#unicode-encoding-decoding "Permalink to this headline")

所有现代的MySQL
DBAPI都提供了在Python应用程序空间和数据库之间处理unicode数据编码和解码的服务。由于情况并非总是如此，SQLAlchemy还包含一个执行编码/解码任务的综合系统。由于这些系统中只有一个应该在使用，SQLAlchemy长期以来包含了在第一次连接时自动检测DBAPI是否自动处理unicode的功能。

MySQL DBAPI是否处理编码通常可以使用DBAPI标志`use_unicode`进行配置，该标志至少已被MySQLdb，PyMySQL和MySQL-Connector支持。在“connect
args”或查询字符串中将此值设置为`0`将导致禁用DBAPI处理unicode的效果，例如，它将返回`str`类型或`bytes`类型，数据在配置的字符集中：

    # connect while disabling the DBAPI's unicode encoding/decoding
    e = create_engine("mysql+mysqldb://scott:tiger@localhost/test?charset=utf8&use_unicode=0")

目前对现代DBAPI的建议如下：

-   将`use_unicode`标志设置为其默认值通常总是安全的；也就是说，根本不要使用它。
-   在Python 3下，`use_unicode=0`标志应该**永远不会被使用**。Python
    3下的SQLAlchemy通常假定DBAPI接收并返回字符串值，如Python
    3字符串，它本质上是unicode对象。
-   在使用MySQLdb的Python 2下，`use_unicode=0`标志将**提供卓越的性能**，因为与SQLAlchemy的快速性相比，MySQLdb的Python
    2下的unicode转换器仅被观察到异常缓慢的性能基于C的编码器/解码器。

简而言之：不要在所有的中指定`use_unicode`
*，并且Python 2 **的MySQLdb上的`use_unicode=0` /
t5\>以获得潜在的性能增益。***

Ansi Quoting Style [¶](#ansi-quoting-style "Permalink to this headline")
------------------------------------------------------------------------

MySQL features two varieties of identifier “quoting style”, one using
backticks and the other using quotes, e.g.
`` `some_identifier` `` vs.
`"some_identifier"`. 当首次建立与特定[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的连接时，所有MySQL方言通过检查`sql_mode`的值来检测正在使用哪个版本。这种引用风格在呈现表名和列名以及反映现有数据库结构时起作用。检测是完全自动的，不需要使用任何引用样式的特殊配置。

在版本0.6中更改：检测ANSI引用样式是完全自动的，在这方面不再有任何最终用户`create_engine()`选项。

MySQL SQL扩展[¶](#mysql-sql-extensions "Permalink to this headline")
--------------------------------------------------------------------

许多MySQL SQL扩展都是通过SQLAlchemy的通用函数和运算符支持来处理的：

    table.select(table.c.password==func.md5('plaintext'))
    table.select(table.c.username.op('regexp')('^[a-d]'))

当然，任何有效的MySQL语句也可以作为字符串执行。

目前有一些对SQL扩展的有限直接支持。

-   SELECT杂注：

        select(..., prefixes=['HIGH_PRIORITY', 'SQL_SMALL_RESULT'])

-   更新与限制：

        update(..., mysql_limit=10)

Rowcount支持[¶](#rowcount-support "Permalink to this headline")
---------------------------------------------------------------

SQLAlchemy将DBAPI `cursor.rowcount`属性标准化为“UPDATE或DELETE匹配的行数”的通常定义。这与大多数MySQL
DBAPI驱动程序的默认设置相矛盾，即“实际修改/删除的行数”。因此，SQLAlchemy
MySQL方言总是在连接时添加`constants.CLIENT.FOUND_ROWS`标志或任何等同于目标方言的标志。此设置目前是硬编码的。

也可以看看

[`ResultProxy.rowcount`](core_connections.html#sqlalchemy.engine.ResultProxy.rowcount "sqlalchemy.engine.ResultProxy.rowcount")

CAST支持[¶](#cast-support "Permalink to this headline")
-------------------------------------------------------

MySQL将文档CAST操作符记录在版本4.0.2中。当使用SQLAlchemy [`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数时，基于服务器版本检测，SQLAlchemy将不会在此版本之前在MySQL上呈现CAST标记，而是直接渲染内部表达式。

在早期的MySQL版本4.0.2之后，CAST可能仍然不可取，因为在4.1.1之前它没有添加所有的数据类型支持。如果您的应用程序属于这个狭窄区域，则可以使用[Custom
SQL Constructs and Compilation
Extension](core_compiler.html)系统按照以下配方来控制CAST的行为：

    from sqlalchemy.sql.expression import Cast
    from sqlalchemy.ext.compiler import compiles

    @compiles(Cast, 'mysql')
    def _check_mysql_version(element, compiler, **kw):
        if compiler.dialect.server_version_info < (4, 1, 0):
            return compiler.process(element.clause, **kw)
        else:
            return compiler.visit_cast(element, **kw)

上述函数只需要在应用程序中声明一次，就会覆盖编译[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")结构以在完全呈现CAST之前检查版本4.1.0；否则直接渲染构造的内部元素。

MySQL特定索引选项[¶](#mysql-specific-index-options "Permalink to this headline")
--------------------------------------------------------------------------------

针对[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构的特定于MySQL的扩展可用。

### 索引长度[¶](#index-length "Permalink to this headline")

MySQL提供了创建具有一定长度的索引条目的选项，其中“length”是指每个值中将成为索引一部分的字符或字节数。SQLAlchemy通过`mysql_length`参数提供此功能：

    Index('my_index', my_table.c.data, mysql_length=10)

    Index('a_b_idx', my_table.c.a, my_table.c.b, mysql_length={'a': 4,
                                                               'b': 9})

对于非二进制字符串类型，前缀长度以字符给出，二进制字符串类型以字节给出。传递给关键字参数*的值必须是*或者是一个整数（因此，为索引的所有列指定相同的前缀长度值）或者一个字典中的列名称和值是前缀相应列的长度值。如果是CHAR，VARCHAR，TEXT，BINARY，VARBINARY和BLOB，MySQL只允许索引列的长度。

0.8.2版中的新功能 `mysql_length`现在可以被指定为与组合索引一起使用的字典。

### 索引类型[¶](#index-types "Permalink to this headline")

某些MySQL存储引擎允许您在创建索引或主键约束时指定索引类型。SQLAlchemy通过[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")上的`mysql_using`参数提供此功能：

    Index('my_index', my_table.c.data, mysql_using='hash')

以及[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")上的`mysql_using`参数：

    PrimaryKeyConstraint("data", mysql_using='hash')

The value passed to the keyword argument will be simply passed through
to the underlying CREATE INDEX or PRIMARY KEY clause, so it *must* be a
valid index type for your MySQL storage engine.

有关更多信息，请访问：

[http://dev.mysql.com/doc/refman/5.0/en/create-index.html
T0\>](http://dev.mysql.com/doc/refman/5.0/en/create-index.html)

[http://dev.mysql.com/doc/refman/5.0/en/create-table.html
T0\>](http://dev.mysql.com/doc/refman/5.0/en/create-table.html)

MySQL外键[¶](#mysql-foreign-keys "Permalink to this headline")
--------------------------------------------------------------

MySQL关于外键的行为有一些重要的注意事项。

### 避免使用外键参数[¶](#foreign-key-arguments-to-avoid "Permalink to this headline")

MySQL不支持外键参数“DEFERRABLE”，“INITIALLY”或“MATCH”。对[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")或[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")使用`deferrable`或`initially`关键字参数将会产生这些关键字在DDL表达式，这会在MySQL上引发错误。为了在外键上使用这些关键字，同时让它们在MySQL后端上被忽略，请使用自定义编译规则：

    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.schema import ForeignKeyConstraint

    @compiles(ForeignKeyConstraint, "mysql")
    def process(element, compiler, **kw):
        element.deferrable = element.initially = None
        return compiler.visit_foreign_key_constraint(element, **kw)

Changed in version 0.9.0: - the MySQL backend no longer silently ignores
the `deferrable` or `initially`
keyword arguments of [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
and [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey").

“MATCH”关键字实际上更加隐蔽，并且被SQLAlchemy与MySQL后端结合在一起明确地禁止。这个参数被MySQL默默地忽略，但是另外有ON
UPDATE和ON
DELETE选项也被后端忽略。因此MATCH不应该与MySQL后端一起使用；与DEFERRABLE和INITIALLY一样，自定义编译规则可用于在DDL定义时更正MySQL
ForeignKeyConstraint。

New in version 0.9.0: - the MySQL backend will raise a
[`CompileError`](core_exceptions.html#sqlalchemy.exc.CompileError "sqlalchemy.exc.CompileError")
when the `match` keyword is used with
[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
or [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey").

### 外键约束的反映[¶](#reflection-of-foreign-key-constraints "Permalink to this headline")

并非所有的MySQL存储引擎都支持外键。When using the very common
`MyISAM` MySQL storage engine, the information
loaded by table reflection will not include foreign keys.
对于这些表，您可以在反射时提供`ForeignKeyConstraint`{.xref .py .py-class
.docutils .literal}：

    Table('mytable', metadata,
          ForeignKeyConstraint(['other_id'], ['othertable.other_id']),
          autoload=True
         )

也可以看看

[CREATE TABLE arguments including Storage
Engines](#mysql-storage-engines)

MySQL唯一约束和反射[¶](#mysql-unique-constraints-and-reflection "Permalink to this headline")
---------------------------------------------------------------------------------------------

SQLAlchemy支持带有标志`unique=True`的[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构，表示一个UNIQUE索引以及[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")结构，表示一个UNIQUE约束。当发出DDL来创建这些约束时，MySQL支持这两种对象/语法。但是，MySQL没有独特的约束结构，它与独特的索引是分开的；也就是说，MySQL上的“UNIQUE”约束等同于创建“UNIQUE
INDEX”。

当反映这些结构时，[`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")和[`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")方法**都会返回一个UNIQUE索引的条目MySQL的。**However,
when performing full table reflection using
`Table(..., autoload=True)`, the
[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
construct is **not** part of the fully reflected [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
construct under any circumstances; this construct is always represented
by a [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
with the `unique=True` setting present in the
`Table.indexes` collection.

TIMESTAMP列和NULL [¶](#timestamp-columns-and-null "Permalink to this headline")
-------------------------------------------------------------------------------

MySQL在历史上强制指定TIMESTAMP数据类型的列隐式地包含缺省值CURRENT\_TIMESTAMP，尽管没有说明，并且另外将列设置为NOT
NULL，与所有其他数据类型相反：

    mysql> CREATE TABLE ts_test (
        -> a INTEGER,
        -> b INTEGER NOT NULL,
        -> c TIMESTAMP,
        -> d TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        -> e TIMESTAMP NULL);
    Query OK, 0 rows affected (0.03 sec)

    mysql> SHOW CREATE TABLE ts_test;
    +---------+-----------------------------------------------------
    | Table   | Create Table
    +---------+-----------------------------------------------------
    | ts_test | CREATE TABLE `ts_test` (
      `a` int(11) DEFAULT NULL,
      `b` int(11) NOT NULL,
      `c` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `d` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `e` timestamp NULL DEFAULT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1

在上面，我们看到INTEGER列默认为NULL，除非它用NOT
NULL指定。但是，当列的类型为TIMESTAMP时，会生成CURRENT\_TIMESTAMP的隐式缺省值，这也会强制该列成为NOT
NULL，即使我们没有这样指定它。

MySQL的这种行为可以使用MySQL
5.6中引入的[explicit\_defaults\_for\_timestamp](http://dev.mysql.com/doc/refman/5.6/en/server-system-variables.html#sysvar_explicit_defaults_for_timestamp)配置标志在MySQL端进行更改。在启用此服务器设置的情况下，TIMESTAMP列的行为与MySQL侧的任何其他数据类型相对于默认和可空性相同。

但是，为了适应绝大多数不指定此新标志的MySQL数据库，SQLAlchemy会使用任何未指定`nullable=False`的TIMESTAMP列显式地发出“NULL”说明符。为了适应更新的指定`explicit_defaults_for_timestamp`的数据库，SQLAlchemy还为指定`nullable=False`的TIMESTAMP列发出NOT NULL。以下示例说明：

    from sqlalchemy import MetaData, Integer, Table, Column, text
    from sqlalchemy.dialects.mysql import TIMESTAMP

    m = MetaData()
    t = Table('ts_test', m,
            Column('a', Integer),
            Column('b', Integer, nullable=False),
            Column('c', TIMESTAMP),
            Column('d', TIMESTAMP, nullable=False)
        )


    from sqlalchemy import create_engine
    e = create_engine("mysql://scott:tiger@localhost/test", echo=True)
    m.create_all(e)

输出：

    CREATE TABLE ts_test (
        a INTEGER,
        b INTEGER NOT NULL,
        c TIMESTAMP NULL,
        d TIMESTAMP NOT NULL
    )

版本1.0.0更改： - SQLAlchemy现在在所有情况下为TIMESTAMP列呈现NULL或NOT
NULL，以适应`explicit_defaults_for_timestamp`。在此版本之前，它不会为`nullable=False`的TIMESTAMP列呈现“NOT NULL”。

MySQL数据类型[¶](#mysql-data-types "Permalink to this headline")
----------------------------------------------------------------

与所有SQLAlchemy方言一样，所有已知可用于MySQL的UPPERCASE类型都可从顶级方言导入：

    from sqlalchemy.dialects.mysql import \
            BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
            DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
            LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
            NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
            TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

特定于MySQL的类型或具有特定于MySQL的构造参数的类型如下所示：

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `BIGINT`{.descname} （ *display\_width = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.BIGINT "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._IntegerType`，[`sqlalchemy.types.BIGINT`](core_type_basics.html#sqlalchemy.types.BIGINT "sqlalchemy.types.BIGINT")

    MySQL BIGINTEGER类型。

    `__ init __`{.descname} （ *display\_width = None*，*\*\* kw* ） [/ T5\>](#sqlalchemy.dialects.mysql.BIGINT.__init__ "Permalink to this definition")
    :   构建一个BIGINTEGER。

        参数：

        -   **display\_width**
            [¶](#sqlalchemy.dialects.mysql.BIGINT.params.display_width)
            - 可选，此数字的最大显示宽度。
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.BIGINT.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.BIGINT.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`BINARY`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.mysql.BINARY "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    SQL BINARY类型。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`BIT`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.mysql.BIT "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    MySQL BIT类型。

    这种类型适用于MyISAM的MySQL
    5.0.3或更高版本，以及MyISAM，MEMORY，InnoDB和BDB的5.0.5或更高版本。对于旧版本，请使用MSTinyInteger()类型。

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   构建一个BIT。

        参数：

        **长度** [¶](#sqlalchemy.dialects.mysql.BIT.params.length) -
        可选，位数。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`BLOB`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.mysql.BLOB "Permalink to this definition")
:   基础：[`sqlalchemy.types.LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

    SQL BLOB类型。

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.LargeBinary.__init__ "sqlalchemy.types.LargeBinary.__init__")
        *method of* [`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

        构建一个LargeBinary类型。

        参数：

        **length**[¶](#sqlalchemy.dialects.mysql.BLOB.params.length) –
        optional, a length for the column for use in DDL statements, for
        those binary types that accept a length, such as the MySQL BLOB
        type.

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `BOOLEAN`{.descname} （ *create\_constraint = True*，*name = None*，*\_create\_events = True tt\> ） [¶](#sqlalchemy.dialects.mysql.BOOLEAN "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

    SQL BOOLEAN类型。

    `__ init __`{.descname} （ *create\_constraint = True*，*name =无*，*\_create\_events = True* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.BOOLEAN.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.Boolean.__init__ "sqlalchemy.types.Boolean.__init__")
        *method of* [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

        构造一个布尔值。

        参数：

        -   **create\_constraint**
            [¶](#sqlalchemy.dialects.mysql.BOOLEAN.params.create_constraint)
            - 默认为True。如果布尔值是作为int /
            smallint生成的，那么还要在表上创建CHECK约束，以确保1或0作为值。
        -   **name**[¶](#sqlalchemy.dialects.mysql.BOOLEAN.params.name)
            – if a CHECK constraint is generated, specify the name of
            the constraint.

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`CHAR`{.descname}(*length=None*, *\*\*kwargs*)[¶](#sqlalchemy.dialects.mysql.CHAR "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._StringType`，[`sqlalchemy.types.CHAR`](core_type_basics.html#sqlalchemy.types.CHAR "sqlalchemy.types.CHAR")

    MySQL CHAR类型，用于固定长度的字符数据。

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mysql.CHAR.__init__ "Permalink to this definition")
    :   构建一个CHAR。

        参数：

        -   **长度** [¶](#sqlalchemy.dialects.mysql.CHAR.params.length)
            - 最大数据长度，以字符为单位。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.CHAR.params.binary)
            – Optional, use the default binary collation for the
            national character set.
            这不影响存储的数据类型，对二进制数据使用BINARY类型。
        -   **整理**
            [¶](#sqlalchemy.dialects.mysql.CHAR.params.collation) -
            可选，请求特定的排序规则。必须与国家字符集兼容。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `DATE`{.descname} [¶](#sqlalchemy.dialects.mysql.DATE "Permalink to this definition")
:   基础：[`sqlalchemy.types.Date`](core_type_basics.html#sqlalchemy.types.Date "sqlalchemy.types.Date")

    SQL DATE类型。

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `DATETIME`{.descname} （ *timezone = False*，*FSP =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.DATETIME "Permalink to this definition")*
:   基础：[`sqlalchemy.types.DATETIME`](core_type_basics.html#sqlalchemy.types.DATETIME "sqlalchemy.types.DATETIME")

    MySQL DATETIME类型。

     `__init__`{.descname}(*timezone=False*, *fsp=None*)[¶](#sqlalchemy.dialects.mysql.DATETIME.__init__ "Permalink to this definition")
    :   构建一个MySQL DATETIME类型。

        参数：

        -   **时区**
            [¶](#sqlalchemy.dialects.mysql.DATETIME.params.timezone) -
            MySQL方言没有使用。
        -   **fsp** [¶](#sqlalchemy.dialects.mysql.DATETIME.params.fsp)
            -

            小数秒精度值。MySQL
            5.6.4支持小数秒的存储；此参数将在DATETIME类型发出DDL时使用。

            注意

            DBAPI驱动程序对小数秒的支持可能有限；目前的支持包括MySQL连接器/
            Python。

        0.8.5版新增：增加了支持小数秒的特定于MySQL的[`mysql.DATETIME`{.xref
        .py .py-class .docutils
        .literal}](#sqlalchemy.dialects.mysql.DATETIME "sqlalchemy.dialects.mysql.DATETIME")。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `DECIMAL`{.descname} （ *precision = None*，*scale = None*，*asdecimal = True*，*\*\* kw* ） [](#sqlalchemy.dialects.mysql.DECIMAL "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._NumericType`，[`sqlalchemy.types.DECIMAL`](core_type_basics.html#sqlalchemy.types.DECIMAL "sqlalchemy.types.DECIMAL")

    MySQL DECIMAL类型。

     `__init__`{.descname}(*precision=None*, *scale=None*, *asdecimal=True*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.DECIMAL.__init__ "Permalink to this definition")
    :   构建一个DECIMAL。

        参数：

        -   **精确度**
            [¶](#sqlalchemy.dialects.mysql.DECIMAL.params.precision) -
            此数字中的总数字。如果比例和精度均为无，则将值存储为服务器允许的限制。
        -   **scale**[¶](#sqlalchemy.dialects.mysql.DECIMAL.params.scale)
            – The number of digits after the decimal point.
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.DECIMAL.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.DECIMAL.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `DOUBLE`{.descname} （ *precision = None*，*scale = None*，*asdecimal = True*，*\*\* kw* ） [](#sqlalchemy.dialects.mysql.DOUBLE "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._FloatType`

    MySQL DOUBLE类型。

     `__init__`{.descname}(*precision=None*, *scale=None*, *asdecimal=True*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.DOUBLE.__init__ "Permalink to this definition")
    :   构建一个DOUBLE。

        注意

        默认情况下，[`DOUBLE`](#sqlalchemy.dialects.mysql.DOUBLE "sqlalchemy.dialects.mysql.DOUBLE")类型将从float转换为Decimal，并使用默认为10位的截断。指定`scale=n`或`decimal_return_scale=n`以更改此比例，或`asdecimal=False`直接以Python浮点形式返回值。

        参数：

        -   **精确度**
            [¶](#sqlalchemy.dialects.mysql.DOUBLE.params.precision) -
            此数字中的总数字。如果比例和精度均为无，则将值存储为服务器允许的限制。
        -   **scale**[¶](#sqlalchemy.dialects.mysql.DOUBLE.params.scale)
            – The number of digits after the decimal point.
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.DOUBLE.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.DOUBLE.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `ENUM`{.descname} （ *\* enums*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.ENUM "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")，`sqlalchemy.dialects.mysql.enumerated._EnumeratedValues`

    MySQL ENUM类型。

    `__ init __`{.descname} （ *\* enums*，*\*\* kw* ） [T5\>](#sqlalchemy.dialects.mysql.ENUM.__init__ "Permalink to this definition")
    :   构造一个枚举。

        例如。：

            Column('myenum', ENUM("foo", "bar", "baz"))

        参数：

        -   **枚举** [¶](#sqlalchemy.dialects.mysql.ENUM.params.enums) -

            此ENUM的有效值范围。根据引用标志生成模式时，将引用值（请参见下文）。该对象也可以是符合PEP-435的枚举类型。

        -   **严格** [¶](#sqlalchemy.dialects.mysql.ENUM.params.strict)
            -

            这个标志没有效果。

            版本更改： MySQL
            ENUM类型以及基本枚举类型现在验证所有Python数据值。

        -   **charset**[¶](#sqlalchemy.dialects.mysql.ENUM.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.ENUM.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.ENUM.params.ascii) –
            Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.ENUM.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **binary**[¶](#sqlalchemy.dialects.mysql.ENUM.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。
        -   **引用** [¶](#sqlalchemy.dialects.mysql.ENUM.params.quoting)
            -

            默认为'auto'：自动确定枚举值引用。如果所有枚举值被相同的引号字符包围，则使用“引用”模式。否则，请使用“未加引号”模式。

            '引用'：枚举中的值已被引用，它们将在生成模式时直接使用 -
            此用法已弃用。

            'unquoted'：枚举中的值不被引用，它们将在生成模式时被转义并被单引号包围。

            此类型的以前版本始终要求提供手动引用的值；未来版本将始终为您引用字符串文字。这是一个过渡选项。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `FLOAT`{.descname} （ *precision = None*，*scale = None*，*asdecimal = False*，*\*\* kw* ） [](#sqlalchemy.dialects.mysql.FLOAT "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._FloatType`，[`sqlalchemy.types.FLOAT`](core_type_basics.html#sqlalchemy.types.FLOAT "sqlalchemy.types.FLOAT")

    MySQL FLOAT类型。

     `__init__`{.descname}(*precision=None*, *scale=None*, *asdecimal=False*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.FLOAT.__init__ "Permalink to this definition")
    :   构建一个浮动。

        参数：

        -   **精确度**
            [¶](#sqlalchemy.dialects.mysql.FLOAT.params.precision) -
            此数字中的总数字。如果比例和精度均为无，则将值存储为服务器允许的限制。
        -   **scale**[¶](#sqlalchemy.dialects.mysql.FLOAT.params.scale)
            – The number of digits after the decimal point.
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.FLOAT.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.FLOAT.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `INTEGER`{.descname} （ *display\_width = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.INTEGER "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._IntegerType`，[`sqlalchemy.types.INTEGER`](core_type_basics.html#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER")

    MySQL INTEGER类型。

    `__ init __`{.descname} （ *display\_width = None*，*\*\* kw* ） [/ T5\>](#sqlalchemy.dialects.mysql.INTEGER.__init__ "Permalink to this definition")
    :   构建一个INTEGER。

        参数：

        -   **display\_width**
            [¶](#sqlalchemy.dialects.mysql.INTEGER.params.display_width)
            - 可选，此数字的最大显示宽度。
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.INTEGER.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.INTEGER.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `JSON`{.descname} （ *none\_as\_null = False* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.JSON "Permalink to this definition")
:   基础：[`sqlalchemy.types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")

    MySQL JSON类型。

    MySQL从版本5.7开始支持JSON。Note that MariaDB does **not** support
    JSON at the time of this writing.

    [`mysql.JSON`](#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")类型支持JSON值的持久性以及[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")数据类型提供的核心索引操作，方法是调整操作以呈现`JSON_EXTRACT`

    版本1.1中的新功能

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `LONGBLOB`{.descname} （ *length = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.LONGBLOB "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    MySQL LONGBLOB类型，用于最多2 \^ 32字节的二进制数据。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `LONGTEXT`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.LONGTEXT "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._StringType`

    MySQL LONGTEXT类型，文本最多2 \^ 32个字符。

    ` __初始化__  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   构建一个LONGTEXT。

        参数：

        -   **charset**[¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.ascii)
            – Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **national**
            [¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.national) -
            可选。如果为true，请使用服务器配置的国家字符集。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.LONGTEXT.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `MEDIUMBLOB`{.descname} （ *length = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.MEDIUMBLOB "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    MySQL MEDIUMBLOB类型，用于最大2 \^ 24字节的二进制数据。

*class* `sqlalchemy.dialects.mysql。 tt> MEDIUMINT`{.descclassname} （ *display\_width = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.MEDIUMINT "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._IntegerType`

    MySQL MEDIUMINTEGER类型。

    `__ init __`{.descname} （ *display\_width = None*，*\*\* kw* ） [/ T5\>](#sqlalchemy.dialects.mysql.MEDIUMINT.__init__ "Permalink to this definition")
    :   构建一个MEDIUMINTEGER

        参数：

        -   **display\_width**
            [¶](#sqlalchemy.dialects.mysql.MEDIUMINT.params.display_width)
            - 可选，此数字的最大显示宽度。
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.MEDIUMINT.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.MEDIUMINT.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `MEDIUMTEXT`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.MEDIUMTEXT "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._StringType`

    MySQL MEDIUMTEXT类型，用于最多2 \^ 24个字符的文本。

    ` __初始化__  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   构建MEDIUMTEXT。

        参数：

        -   **charset**[¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.ascii)
            – Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **national**
            [¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.national) -
            可选。如果为true，请使用服务器配置的国家字符集。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.MEDIUMTEXT.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `NCHAR`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.NCHAR "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._StringType`，[`sqlalchemy.types.NCHAR`](core_type_basics.html#sqlalchemy.types.NCHAR "sqlalchemy.types.NCHAR")

    MySQL NCHAR类型。

    用于服务器配置的国家字符集中的固定长度字符数据。

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mysql.NCHAR.__init__ "Permalink to this definition")
    :   构建NCHAR。

        参数：

        -   **长度** [¶](#sqlalchemy.dialects.mysql.NCHAR.params.length)
            - 最大数据长度，以字符为单位。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.NCHAR.params.binary)
            – Optional, use the default binary collation for the
            national character set.
            这不影响存储的数据类型，对二进制数据使用BINARY类型。
        -   **整理**
            [¶](#sqlalchemy.dialects.mysql.NCHAR.params.collation) -
            可选，请求特定的排序规则。必须与国家字符集兼容。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `NUMERIC`{.descname} （ *precision = None*，*scale = None*，*asdecimal = True*，*\*\* kw* ） [](#sqlalchemy.dialects.mysql.NUMERIC "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._NumericType`，[`sqlalchemy.types.NUMERIC`](core_type_basics.html#sqlalchemy.types.NUMERIC "sqlalchemy.types.NUMERIC")

    MySQL NUMERIC类型。

     `__init__`{.descname}(*precision=None*, *scale=None*, *asdecimal=True*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.NUMERIC.__init__ "Permalink to this definition")
    :   构建一个数字。

        参数：

        -   **精确度**
            [¶](#sqlalchemy.dialects.mysql.NUMERIC.params.precision) -
            此数字中的总数字。如果比例和精度均为无，则将值存储为服务器允许的限制。
        -   **scale**[¶](#sqlalchemy.dialects.mysql.NUMERIC.params.scale)
            – The number of digits after the decimal point.
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.NUMERIC.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.NUMERIC.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `NVARCHAR`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.NVARCHAR "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._StringType`，[`sqlalchemy.types.NVARCHAR`](core_type_basics.html#sqlalchemy.types.NVARCHAR "sqlalchemy.types.NVARCHAR")

    MySQL NVARCHAR类型。

    用于服务器配置的国家字符集中的可变长度字符数据。

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mysql.NVARCHAR.__init__ "Permalink to this definition")
    :   构建一个NVARCHAR。

        参数：

        -   **长度**
            [¶](#sqlalchemy.dialects.mysql.NVARCHAR.params.length) -
            最大数据长度，以字符为单位。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.NVARCHAR.params.binary)
            – Optional, use the default binary collation for the
            national character set.
            这不影响存储的数据类型，对二进制数据使用BINARY类型。
        -   **整理**
            [¶](#sqlalchemy.dialects.mysql.NVARCHAR.params.collation) -
            可选，请求特定的排序规则。必须与国家字符集兼容。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `REAL`{.descname} （ *precision = None*，*scale = None*，*asdecimal = True*，*\*\* kw* ） [](#sqlalchemy.dialects.mysql.REAL "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._FloatType`，[`sqlalchemy.types.REAL`](core_type_basics.html#sqlalchemy.types.REAL "sqlalchemy.types.REAL")

    MySQL REAL类型。

     `__init__`{.descname}(*precision=None*, *scale=None*, *asdecimal=True*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.REAL.__init__ "Permalink to this definition")
    :   构建一个真实的。

        注意

        默认情况下，[`REAL`](#sqlalchemy.dialects.mysql.REAL "sqlalchemy.dialects.mysql.REAL")类型将从float转换为Decimal，并使用默认为10位的截断。指定`scale=n`或`decimal_return_scale=n`以更改此比例，或`asdecimal=False`直接以Python浮点形式返回值。

        参数：

        -   **精确度**
            [¶](#sqlalchemy.dialects.mysql.REAL.params.precision) -
            此数字中的总数字。如果比例和精度均为无，则将值存储为服务器允许的限制。
        -   **scale**[¶](#sqlalchemy.dialects.mysql.REAL.params.scale) –
            The number of digits after the decimal point.
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.REAL.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.REAL.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`SET`{.descname}(*\*values*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.SET "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.enumerated._EnumeratedValues`

    MySQL SET类型。

     `__init__`{.descname}(*\*values*, *\*\*kw*)[¶](#sqlalchemy.dialects.mysql.SET.__init__ "Permalink to this definition")
    :   构建一个SET。

        例如。：

            Column('myset', SET("foo", "bar", "baz"))

        如果此组将用于为表生成DDL，或者[`SET.retrieve_as_bitwise`](#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise "sqlalchemy.dialects.mysql.SET")标志设置为True，则需要使用潜在值列表。

        参数：

        -   **values**[¶](#sqlalchemy.dialects.mysql.SET.params.values)
            – The range of valid values for this SET.
        -   **convert\_unicode**[¶](#sqlalchemy.dialects.mysql.SET.params.convert_unicode)
            – Same flag as that of [`String.convert_unicode`{.xref .py
            .py-paramref .docutils
            .literal}](core_type_basics.html#sqlalchemy.types.String.params.convert_unicode "sqlalchemy.types.String").
        -   **整理**
            [¶](#sqlalchemy.dialects.mysql.SET.params.collation) -
            与[`String.collation`{.xref .py .py-paramref .docutils
            .literal}](core_type_basics.html#sqlalchemy.types.String.params.collation "sqlalchemy.types.String")
        -   **charset**[¶](#sqlalchemy.dialects.mysql.SET.params.charset)
            – same as that of [`VARCHAR.charset`{.xref .py .py-paramref
            .docutils
            .literal}](#sqlalchemy.dialects.mysql.VARCHAR.params.charset "sqlalchemy.dialects.mysql.VARCHAR").
        -   **ascii** [¶](#sqlalchemy.dialects.mysql.SET.params.ascii) -
            与[`VARCHAR.ascii`{.xref .py .py-paramref .docutils
            .literal}](#sqlalchemy.dialects.mysql.VARCHAR.params.ascii "sqlalchemy.dialects.mysql.VARCHAR")相同。
        -   tt\> **unicode**
            [¶](#sqlalchemy.dialects.mysql.SET.params.unicode) -
            与[`VARCHAR.unicode`{.xref .py .py-paramref .docutils
            .literal}](#sqlalchemy.dialects.mysql.VARCHAR.params.unicode "sqlalchemy.dialects.mysql.VARCHAR")相同。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.SET.params.binary)
            – same as that of [`VARCHAR.binary`{.xref .py .py-paramref
            .docutils
            .literal}](#sqlalchemy.dialects.mysql.VARCHAR.params.binary "sqlalchemy.dialects.mysql.VARCHAR").
        -   **引用** [¶](#sqlalchemy.dialects.mysql.SET.params.quoting)
            -

            默认为'auto'：自动确定设定值引用。如果所有值都包含相同的引号字符，则使用“引用”模式。否则，请使用“未加引号”模式。

            '引用'：枚举中的值已被引用，它们将在生成模式时直接使用 -
            此用法已弃用。

            'unquoted'：枚举中的值不被引用，它们将在生成模式时被转义并被单引号包围。

            此类型的以前版本始终要求提供手动引用的值；未来版本将始终为您引用字符串文字。这是一个过渡选项。

            版本0.9.0中的新功能

        -   **retrieve\_as\_bitwise**
            [¶](#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise)
            -

            如果设置为True，则设置类型的数据将被持久保存，并使用整数值进行选择，其中一组被强制为持久性的按位掩码。MySQL允许这种模式具有能够明确存储值的优点，如空字符串`''`{.docutils
            .literal}。数据类型将在SELECT语句中以表达式`col + 0`{.docutils
            .literal}出现，以便将值强制到结果集中的整数值。如果希望保留一个可以存储空字符串`''`{.docutils
            .literal}作为值的集合，则此标志是必需的。

            警告

            当使用[`mysql.SET.retrieve_as_bitwise`{.xref .py
            .py-paramref .docutils
            .literal}](#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise "sqlalchemy.dialects.mysql.SET")时，设置值列表必须以与MySQL数据库上存在的**完全相同的顺序**表示。

            版本1.0.0中的新功能

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `SMALLINT`{.descname} （ *display\_width = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.SMALLINT "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._IntegerType`，[`sqlalchemy.types.SMALLINT`](core_type_basics.html#sqlalchemy.types.SMALLINT "sqlalchemy.types.SMALLINT")

    MySQL SMALLINTEGER类型。

    `__ init __`{.descname} （ *display\_width = None*，*\*\* kw* ） [/ T5\>](#sqlalchemy.dialects.mysql.SMALLINT.__init__ "Permalink to this definition")
    :   构建一个SMALLINTEGER。

        参数：

        -   **display\_width**
            [¶](#sqlalchemy.dialects.mysql.SMALLINT.params.display_width)
            - 可选，此数字的最大显示宽度。
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.SMALLINT.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.SMALLINT.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `TEXT`{.descname} （ *length = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.TEXT "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._StringType`，[`sqlalchemy.types.TEXT`](core_type_basics.html#sqlalchemy.types.TEXT "sqlalchemy.types.TEXT")

    MySQL文本类型，文本最多2 \^ 16个字符。

    ` __初始化__  T0> （ T1> 长度=无 T2>， **千瓦 T3> ） T4> ¶< / T5>`{.descname}
    :   构建一个TEXT。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.mysql.TEXT.params.length)
            – Optional, if provided the server may optimize storage by
            substituting the smallest TEXT type sufficient to store
            `length` characters.
        -   **charset**[¶](#sqlalchemy.dialects.mysql.TEXT.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.TEXT.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.TEXT.params.ascii) –
            Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.TEXT.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **national**
            [¶](#sqlalchemy.dialects.mysql.TEXT.params.national) -
            可选。如果为true，请使用服务器配置的国家字符集。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.TEXT.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`TIME`{.descname}(*timezone=False*, *fsp=None*)[¶](#sqlalchemy.dialects.mysql.TIME "Permalink to this definition")
:   基础：[`sqlalchemy.types.TIME`](core_type_basics.html#sqlalchemy.types.TIME "sqlalchemy.types.TIME")

    MySQL TIME类型。

     `__init__`{.descname}(*timezone=False*, *fsp=None*)[¶](#sqlalchemy.dialects.mysql.TIME.__init__ "Permalink to this definition")
    :   构建一个MySQL TIME类型。

        参数：

        -   **时区**
            [¶](#sqlalchemy.dialects.mysql.TIME.params.timezone) -
            MySQL方言没有使用。
        -   **fsp** [¶](#sqlalchemy.dialects.mysql.TIME.params.fsp) -

            小数秒精度值。MySQL
            5.6支持小数秒的存储；此参数将在为TIME类型发出DDL时使用。

            注意

            DBAPI驱动程序对小数秒的支持可能有限；目前的支持包括MySQL连接器/
            Python。

        0.8版本中的新功能：特定于MySQL的TIME类型以及小数秒支持。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `TIMESTAMP`{.descname} （ *timezone = False*，*FSP =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.TIMESTAMP "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TIMESTAMP`](core_type_basics.html#sqlalchemy.types.TIMESTAMP "sqlalchemy.types.TIMESTAMP")

    MySQL TIMESTAMP类型。

     `__init__`{.descname}(*timezone=False*, *fsp=None*)[¶](#sqlalchemy.dialects.mysql.TIMESTAMP.__init__ "Permalink to this definition")
    :   构建一个MySQL TIMESTAMP类型。

        参数：

        -   **时区**
            [¶](#sqlalchemy.dialects.mysql.TIMESTAMP.params.timezone) -
            MySQL方言没有使用。
        -   **fsp** [¶](#sqlalchemy.dialects.mysql.TIMESTAMP.params.fsp)
            -

            小数秒精度值。MySQL
            5.6.4支持小数秒的存储；当为TIMESTAMP类型发出DDL时将使用此参数。

            注意

            DBAPI驱动程序对小数秒的支持可能有限；目前的支持包括MySQL连接器/
            Python。

        0.8.5版新增：增加了支持小数秒的特定于MySQL的[`mysql.TIMESTAMP`{.xref
        .py .py-class .docutils
        .literal}](#sqlalchemy.dialects.mysql.TIMESTAMP "sqlalchemy.dialects.mysql.TIMESTAMP")。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `TINYBLOB`{.descname} （ *length = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.TINYBLOB "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    MySQL TINYBLOB类型，用于2 \^ 8字节的二进制数据。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `TINYINT`{.descname} （ *display\_width = None*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.TINYINT "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._IntegerType`

    MySQL TINYINT类型。

    `__ init __`{.descname} （ *display\_width = None*，*\*\* kw* ） [/ T5\>](#sqlalchemy.dialects.mysql.TINYINT.__init__ "Permalink to this definition")
    :   构建一个TINYINT。

        参数：

        -   **display\_width**
            [¶](#sqlalchemy.dialects.mysql.TINYINT.params.display_width)
            - 可选，此数字的最大显示宽度。
        -   **无符号**
            [¶](#sqlalchemy.dialects.mysql.TINYINT.params.unsigned) -
            一个布尔值，可选。
        -   **zerofill**
            [¶](#sqlalchemy.dialects.mysql.TINYINT.params.zerofill) -
            可选。如果为true，则值将被存储为左填充零的字符串。请注意，这不会影响底层数据库API返回的值，它们仍然是数字。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `TINYTEXT`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.TINYTEXT "Permalink to this definition")
:   基础：`sqlalchemy.dialects.mysql.types._StringType`

    MySQL TINYTEXT类型，文本最多2 \^ 8个字符。

    ` __初始化__  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   构建一个TINYTEXT。

        参数：

        -   **charset**[¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.ascii)
            – Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **national**
            [¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.national) -
            可选。如果为true，请使用服务器配置的国家字符集。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.TINYTEXT.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。

 *class*`sqlalchemy.dialects.mysql.`{.descclassname}`VARBINARY`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.mysql.VARBINARY "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    SQL VARBINARY类型。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `VARCHAR`{.descname} （ *length = None*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.mysql.VARCHAR "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.mysql.types._StringType`，[`sqlalchemy.types.VARCHAR`](core_type_basics.html#sqlalchemy.types.VARCHAR "sqlalchemy.types.VARCHAR")

    MySQL VARCHAR类型，用于可变长度字符数据。

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.dialects.mysql.VARCHAR.__init__ "Permalink to this definition")
    :   构建一个VARCHAR。

        参数：

        -   **charset**[¶](#sqlalchemy.dialects.mysql.VARCHAR.params.charset)
            – Optional, a column-level character set for this string
            value. 优先使用'ascii'或'unicode'。
        -   **collation**[¶](#sqlalchemy.dialects.mysql.VARCHAR.params.collation)
            – Optional, a column-level collation for this string value.
            优先考虑'二元'短手。
        -   **ascii**[¶](#sqlalchemy.dialects.mysql.VARCHAR.params.ascii)
            – Defaults to False: short-hand for the `latin1`{.docutils
            .literal} character set, generates ASCII in schema.
        -   **unicode**[¶](#sqlalchemy.dialects.mysql.VARCHAR.params.unicode)
            – Defaults to False: short-hand for the `ucs2`{.docutils
            .literal} character set, generates UNICODE in schema.
        -   **national**
            [¶](#sqlalchemy.dialects.mysql.VARCHAR.params.national) -
            可选。如果为true，请使用服务器配置的国家字符集。
        -   **binary**[¶](#sqlalchemy.dialects.mysql.VARCHAR.params.binary)
            – Defaults to False: short-hand, pick the binary collation
            type that matches the column’s character set.
            在模式中生成BINARY。这不会影响存储的数据的类型，只会影响字符数据的排序规则。

*class* `sqlalchemy.dialects.mysql。`{.descclassname} `YEAR`{.descname} （ *display\_width = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.mysql.YEAR "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    MySQL YEAR类型，用于1901-2155年的单字节存储。

的MySQL的Python [¶ T0\>](#module-sqlalchemy.dialects.mysql.mysqldb "Permalink to this headline")
------------------------------------------------------------------------------------------------

通过MySQL-Python驱动程序支持MySQL数据库。

### DBAPI [¶ T0\>](#dialect-mysql-mysqldb-url "Permalink to this headline")

MySQL-Python的文档和下载信息（如果适用）可在以下网址找到：[http://sourceforge.net/projects/mysql-python](http://sourceforge.net/projects/mysql-python)

### 连接[¶ T0\>](#dialect-mysql-mysqldb-connect "Permalink to this headline")

连接字符串：

    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

### Unicode的[¶ T0\>](#mysqldb-unicode "Permalink to this headline")

有关unicode处理的当前建议，请参阅[Unicode](#mysql-unicode)。

### Py3K支持[¶](#py3k-support "Permalink to this headline")

目前，MySQLdb只在Python
2上运行，开发已停止。[mysqlclient](https://github.com/PyMySQL/mysqlclient-python)
is fork of MySQLdb and provides Python 3 support as well as some
bugfixes.

### 在Google Cloud SQL中使用MySQLdb [¶](#using-mysqldb-with-google-cloud-sql "Permalink to this headline")

Google Cloud SQL现在推荐使用MySQLdb方言。使用以下URL连接：

    mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>

pymysql [¶ T0\>](#module-sqlalchemy.dialects.mysql.pymysql "Permalink to this headline")
----------------------------------------------------------------------------------------

通过PyMySQL驱动程序支持MySQL数据库。

### DBAPI [¶ T0\>](#dialect-mysql-pymysql-url "Permalink to this headline")

PyMySQL的文档和下载信息（如果适用）可在以下网址获得：[http://www.pymysql.org/](http://www.pymysql.org/)

### 连接[¶ T0\>](#dialect-mysql-pymysql-connect "Permalink to this headline")

连接字符串：

    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

### Unicode的[¶ T0\>](#id3 "Permalink to this headline")

有关unicode处理的当前建议，请参阅[Unicode](#mysql-unicode)。

### MySQL-Python兼容性[¶](#mysql-python-compatibility "Permalink to this headline")

pymysql
DBAPI是MySQL-python（MySQLdb）驱动程序的纯Python端口，其目标是100％的兼容性。MySQL-python的大多数行为注释也适用于pymysql驱动程序。

MySQL的 - 连接器[¶ T0\>](#module-sqlalchemy.dialects.mysql.mysqlconnector "Permalink to this headline")
-------------------------------------------------------------------------------------------------------

通过MySQL Connector / Python驱动程序支持MySQL数据库。

### DBAPI [¶ T0\>](#dialect-mysql-mysqlconnector-url "Permalink to this headline")

MySQL Connector /
Python的文档和下载信息（如果适用）可在以下网址获得：[http://dev.mysql.com/downloads/connector/python/](http://dev.mysql.com/downloads/connector/python/)

### 连接[¶ T0\>](#dialect-mysql-mysqlconnector-connect "Permalink to this headline")

连接字符串：

    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

### Unicode的[¶ T0\>](#id4 "Permalink to this headline")

有关unicode处理的当前建议，请参阅[Unicode](#mysql-unicode)。

cymysql [¶ T0\>](#module-sqlalchemy.dialects.mysql.cymysql "Permalink to this headline")
----------------------------------------------------------------------------------------

通过CyMySQL驱动程序支持MySQL数据库。

### DBAPI [¶ T0\>](#dialect-mysql-cymysql-url "Permalink to this headline")

CyMySQL的文档和下载信息（如果适用）可在以下网址获得：[https://github.com/nakagami/CyMySQL](https://github.com/nakagami/CyMySQL)

### 连接[¶ T0\>](#dialect-mysql-cymysql-connect "Permalink to this headline")

连接字符串：

    mysql+cymysql://<username>:<password>@<host>/<dbname>[?<options>]

OurSQL [¶ T0\>](#module-sqlalchemy.dialects.mysql.oursql "Permalink to this headline")
--------------------------------------------------------------------------------------

通过OurSQL驱动程序支持MySQL数据库。

### DBAPI [¶ T0\>](#dialect-mysql-oursql-url "Permalink to this headline")

OurSQL的文档和下载信息（如果适用）可在以下网址获得：[http://packages.python.org/oursql/](http://packages.python.org/oursql/)

### 连接[¶ T0\>](#dialect-mysql-oursql-connect "Permalink to this headline")

连接字符串：

    mysql+oursql://<user>:<password>@<host>[:<port>]/<dbname>

### Unicode的[¶ T0\>](#id5 "Permalink to this headline")

有关unicode处理的当前建议，请参阅[Unicode](#mysql-unicode)。

Google App Engine [¶](#module-sqlalchemy.dialects.mysql.gaerdbms "Permalink to this headline")
----------------------------------------------------------------------------------------------

通过Google Cloud SQL驱动程序支持MySQL数据库。

这种方言主要基于[`mysql.mysqldb`](#module-sqlalchemy.dialects.mysql.mysqldb "sqlalchemy.dialects.mysql.mysqldb")方言，只有很少的变化。

New in version 0.7.8.

Deprecated since version 1.0: This dialect is **no longer necessary**
for Google Cloud SQL; the MySQLdb dialect can be used directly. Cloud
SQL现在推荐使用URL格式通过mysql方言创建连接

`mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>`

### DBAPI [¶ T0\>](#dialect-mysql-gaerdbms-url "Permalink to this headline")

有关Google Cloud
SQL的文档和下载信息（如果适用），请访问：[https://developers.google.com/appengine/docs/python/cloud-sql/developers-guide](https://developers.google.com/appengine/docs/python/cloud-sql/developers-guide)

### 连接[¶ T0\>](#dialect-mysql-gaerdbms-connect "Permalink to this headline")

连接字符串：

    mysql+gaerdbms:///<dbname>?instance=<instancename>

### 汇集[¶ T0\>](#pooling "Permalink to this headline")

Google App
Engine连接似乎是随机回收的，因此方言不会集中连接。默认情况下，[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")实现安装在[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")中。

pyodbc [¶ T0\>](#module-sqlalchemy.dialects.mysql.pyodbc "Permalink to this headline")
--------------------------------------------------------------------------------------

通过PyODBC驱动程序支持MySQL数据库。

注意

用于MySQL方言的PyODBC没有得到很好的支持，并且会受到当前ODBC驱动程序中存在的未解决的字符编码问题的影响。（请参阅[http://code.google.com/p/pyodbc/issues/detail?id=25](http://code.google.com/p/pyodbc/issues/detail?id=25)）。推荐其他MySQL的方言。

### DBAPI [¶ T0\>](#dialect-mysql-pyodbc-url "Permalink to this headline")

PyODBC的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/pyodbc/](http://pypi.python.org/pypi/pyodbc/)

### 连接[¶ T0\>](#dialect-mysql-pyodbc-connect "Permalink to this headline")

连接字符串：

    mysql+pyodbc://<username>:<password>@<dsnname>

zxjdbc [¶ T0\>](#module-sqlalchemy.dialects.mysql.zxjdbc "Permalink to this headline")
--------------------------------------------------------------------------------------

通过用于Jython驱动程序的zxjdbc支持MySQL数据库。

注意

当前版本的SQLAlchemy不支持Jython。zxjdbc方言应该被认为是实验性的。

### DBAPI [¶ T0\>](#dialect-mysql-zxjdbc-url "Permalink to this headline")

此数据库的驱动程序可在以下网址找到：[http://dev.mysql.com/downloads/connector/j/](http://dev.mysql.com/downloads/connector/j/)

### 连接[¶ T0\>](#dialect-mysql-zxjdbc-connect "Permalink to this headline")

连接字符串：

    mysql+zxjdbc://<user>:<password>@<hostname>[:<port>]/<database>

### 字符集[¶](#character-sets "Permalink to this headline")

SQLAlchemy zxjdbc方言将unicode直接传递给zxjdbc / JDBC层。为了允许从MySQL
Connector / J
JDBC驱动程序发送多个字符集，默认情况下，SQLAlchemy将其`characterEncoding`连接属性设置为`UTF-8`。它可以通过`create_engine` URL参数覆盖。
