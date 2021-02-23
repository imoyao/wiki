---
title: 甲骨文oracle
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/dialects/oracle/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - dialects
tags:
  - 
---
甲骨文[¶ T0\>](#module-sqlalchemy.dialects.oracle.base "Permalink to this headline")
====================================================================================

支持Oracle数据库。

DBAPI支持[¶](#dialect-oracle "Permalink to this headline")
----------------------------------------------------------

以下dialect / DBAPI选项可用。请参阅各个DBAPI部分的连接信息。

-   [CX-甲骨文 T0\>](#module-sqlalchemy.dialects.oracle.cx_oracle)
-   Jython的[zxJDBC](#module-sqlalchemy.dialects.oracle.zxjdbc)

连接参数[¶](#connect-arguments "Permalink to this headline")
------------------------------------------------------------

The dialect supports several [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
arguments which affect the behavior of the dialect regardless of driver
in use.

-   `use_ansi` - 使用ANSI JOIN结构（请参阅Oracle
    8一节）。默认为`True`。如果`False`，则Oracle-8兼容构造用于连接。
-   `optimize_limits` - 默认为`False`。参见LIMIT / OFFSET部分。
-   `use_binds_for_limits` - 默认为`True`。参见LIMIT / OFFSET部分。

自动增量行为[¶](#auto-increment-behavior "Permalink to this headline")
----------------------------------------------------------------------

包含整数主键的SQLAlchemy表对象通常被认为具有“自动增量”行为，这意味着它们可以在INSERT时生成它们自己的主键值。由于Oracle没有“自动增量”功能，SQLAlchemy依赖序列来生成这些值。With
the Oracle dialect, *a sequence must always be explicitly specified to
enable autoincrement*.
这与假定使用具有自动增量功能的数据库的大多数文档示例不同。要指定序列，请使用传递给Column构造的sqlalchemy.schema.Sequence对象：

    t = Table('mytable', metadata,
          Column('id', Integer, Sequence('id_seq'), primary_key=True),
          Column(...), ...
    )

当使用表反射时，这一步也是必需的，即autoload = True：

    t = Table('mytable', metadata,
          Column('id', Integer, Sequence('id_seq'), primary_key=True),
          autoload=True
    )

标识符套管[¶](#identifier-casing "Permalink to this headline")
--------------------------------------------------------------

在Oracle中，数据字典使用大写文本表示所有不区分大小写的标识符名称。另一方面，SQLAlchemy认为全小写标识符名称不区分大小写。在模式级通信期间，Oracle方言将所有不区分大小写的标识符转换为和来自这两种格式，例如表和索引的反映。在SQLAlchemy侧使用大写名称表示区分大小写的标识符，并且SQLAlchemy将引用名称
-
这将导致与从Oracle接收的数据字典数据不匹配，因此除非标识名称已真正创建为区分大小写（即使用带引号的名称）
，所有小写字母名称都应该用在SQLAlchemy方面。

LIMIT / OFFSET支持[¶](#limit-offset-support "Permalink to this headline")
-------------------------------------------------------------------------

Oracle不支持LIMIT或OFFSET关键字。SQLAlchemy与ROWNUM一起使用了一个包装子查询方法。The
exact methodology is taken from
[http://www.oracle.com/technology/oramag/oracle/06-sep/o56asktom.html](http://www.oracle.com/technology/oramag/oracle/06-sep/o56asktom.html)
.

有两个选项会影响其行为：

-   “FIRST
    ROWS()”优化关键字默认不使用。要启用此优化指令，请将`optimize_limits=True`指定为[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")。
-   为极限/偏移量传递的值将作为绑定参数发送。一些用户已经观察到，如果值作为绑定发送并且不是字面呈现，Oracle会产生一个糟糕的查询计划。要在SQL语句中逐字地显示限制/偏移值，请将`use_binds_for_limits=False`指定为[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")。

当使用完全不同的窗口查询方法（即ROW\_NUMBER()OVER（ORDER
BY））来提供LIMIT /
OFFSET（注意大多数用户不会观察到此情况）时，某些用户报告了更好的性能。为了适应这种情况，用于LIMIT
/
OFFSET的方法可以完全替换。请参阅[http://www.sqlalchemy.org/trac/wiki/UsageRecipes/WindowFunctionsByDefault](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/WindowFunctionsByDefault)中的配方，该配置安装了一个选择编译器，该选择编译器使用窗口函数替代极限/偏移量的生成。

返回支持[¶](#returning-support "Permalink to this headline")
------------------------------------------------------------

Oracle数据库支持有限的RETURNING形式，以便从INSERT，UPDATE和DELETE语句中检索匹配行的结果集。Oracle的RETURNING..INTO语法只支持返回一行，因为它依赖OUT参数才能正常工作。另外，受支持的DBAPI还有其他限制（请参阅[RETURNING
Support](#cx-oracle-returning)）。

SQLAlchemy的“隐式返回”功能通常在Oracle后端启用，它在INSERT中使用RETURNING，有时使用UPDATE语句来获取新生成的主键值和其他SQL默认值和表达式。默认情况下，“隐式返回”通常只会获取嵌入到INSERT中的单个`nextval(some_seq)`表达式的值，以便在INSERT语句中递增序列并同时返回值。要全面禁用此功能，请将`implicit_returning=False`指定为[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")：

    engine = create_engine("oracle://scott:tiger@dsn",
                           implicit_returning=False)

隐式返回也可作为表选项在逐个表的基础上禁用：

    # Core Table
    my_table = Table("my_table", metadata, ..., implicit_returning=False)


    # declarative
    class MyClass(Base):
        __tablename__ = 'my_table'
        __table_args__ = {"implicit_returning": False}

也可以看看

[RETURNING Support](#cx-oracle-returning) -
对隐式返回的额外cx\_oracle特定限制。

ON UPDATE CASCADE [¶](#on-update-cascade "Permalink to this headline")
----------------------------------------------------------------------

Oracle没有本地ON UPDATE
CASCADE功能。基于触发器的解决方案可在[http://asktom.oracle.com/tkyte/update\_cascade/index.html](http://asktom.oracle.com/tkyte/update_cascade/index.html)中找到。

使用SQLAlchemy ORM时，ORM手动发布级联更新的能力有限 - 使用“deferrable =
True”，initial
='deferred'“关键字参数指定ForeignKey对象，并在每个关系()上指定”passive\_updates
= False“。

Oracle 8兼容性[¶](#oracle-8-compatibility "Permalink to this headline")
-----------------------------------------------------------------------

当检测到Oracle 8时，方言内部将其自身配置为以下行为：

-   use\_ansi标志被设置为False。这具有将所有JOIN短语转换为WHERE子句的效果，并且在LEFT
    OUTER JOIN使用Oracle的（+）运算符的情况下。
-   当使用[`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")时，NVARCHAR2和NCLOB数据类型不再生成为DDL
    - 而是发出VARCHAR2和CLOB。这是因为这些类型在Oracle
    8上似乎不能正常工作，即使它们可用。[`NVARCHAR`](core_type_basics.html#sqlalchemy.types.NVARCHAR "sqlalchemy.types.NVARCHAR")和[`NCLOB`](#sqlalchemy.dialects.oracle.NCLOB "sqlalchemy.dialects.oracle.NCLOB")类型将始终生成NVARCHAR2和NCLOB。
-   在使用cx\_oracle时，“native
    unicode”模式被禁用，即SQLAlchemy在将所有Python
    unicode对象作为绑定参数传入之前将其编码为“string”。

同义词/ DBLINK反射[¶](#synonym-dblink-reflection "Permalink to this headline")
------------------------------------------------------------------------------

When using reflection with Table objects, the dialect can optionally
search for tables indicated by synonyms, either in local or remote
schemas or accessed over DBLINK, by passing the flag
`oracle_resolve_synonyms=True` as a keyword argument
to the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
construct:

    some_table = Table('some_table', autoload=True,
                                autoload_with=some_engine,
                                oracle_resolve_synonyms=True)

设置此标志时，不仅在`ALL_TABLES`视图中搜索给定的名称（如`some_table`），还会在`ALL_SYNONYMS`如果同义词位于并指向DBLINK，则oracle方言知道如何使用DBLINK语法（例如`@dblink`）查找表的信息。

`oracle_resolve_synonyms` is accepted wherever
reflection arguments are accepted, including methods such as
[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
and [`Inspector.get_columns()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns "sqlalchemy.engine.reflection.Inspector.get_columns").

如果同义词没有被使用，这个标志应该被禁用。

日期时间兼容性[¶](#datetime-compatibility "Permalink to this headline")
-----------------------------------------------------------------------

Oracle没有称为`DATETIME`的数据类型，它只有`DATE`，它实际上可以存储日期和时间值。出于这个原因，Oracle方言提供了一个类型[`oracle.DATE`](#sqlalchemy.dialects.oracle.DATE "sqlalchemy.dialects.oracle.DATE")，它是[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的子类。这种类型没有特殊的行为，仅作为这种类型的“标记”出现；此外，当数据库列被反映并且类型被报告为`DATE`时，将使用支持时间的[`oracle.DATE`](#sqlalchemy.dialects.oracle.DATE "sqlalchemy.dialects.oracle.DATE")类型。

版本0.9.4中已更改：将[`oracle.DATE`](#sqlalchemy.dialects.oracle.DATE "sqlalchemy.dialects.oracle.DATE")添加到[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")子类中。这是一个变化，因为以前的版本会将`DATE`列反映为[`types.DATE`](core_type_basics.html#sqlalchemy.types.DATE "sqlalchemy.types.DATE")，它是[`Date`](core_type_basics.html#sqlalchemy.types.Date "sqlalchemy.types.Date")的子类。这里唯一的意义是检查在特殊Python翻译中使用的列类型或将模式迁移到其他数据库后端的方案。

Oracle表选项[¶](#oracle-table-options "Permalink to this headline")
-------------------------------------------------------------------

CREATE TABLE短语通过与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构结合使用，支持以下选项：

-   `ON COMMIT`：

        Table(
            "some_table", metadata, ...,
            prefixes=['GLOBAL TEMPORARY'], oracle_on_commit='PRESERVE ROWS')

版本1.0.0中的新功能

-   `COMPRESS`

         Table('mytable', metadata, Column('data', String(32)),
             oracle_compress=True)

         Table('mytable', metadata, Column('data', String(32)),
             oracle_compress=6)

        The ``oracle_compress`` parameter accepts either an integer compression
        level, or ``True`` to use the default compression level.

版本1.0.0中的新功能

Oracle特定索引选项[¶](#oracle-specific-index-options "Permalink to this headline")
----------------------------------------------------------------------------------

### 位图索引[¶](#bitmap-indexes "Permalink to this headline")

您可以指定`oracle_bitmap`参数来创建位图索引而不是B树索引：

    Index('my_index', my_table.c.data, oracle_bitmap=True)

位图索引不能是唯一的，也不能被压缩。SQLAlchemy不会检查这些限制，只有数据库会。

版本1.0.0中的新功能

### 索引压缩[¶](#index-compression "Permalink to this headline")

对于包含大量重复值的索引，Oracle具有更高效的存储模式。使用`oracle_compress`参数打开密钥压缩：

    Index('my_index', my_table.c.data, oracle_compress=True)

    Index('my_index', my_table.c.data1, my_table.c.data2, unique=True,
           oracle_compress=1)

`oracle_compress`参数接受指定要压缩的前缀列数的整数，或者接受`True`以使用缺省值（非唯一索引的所有列，除最后一列外的所有列为唯一索引）。

版本1.0.0中的新功能

Oracle数据类型[¶](#oracle-data-types "Permalink to this headline")
------------------------------------------------------------------

与所有SQLAlchemy方言一样，所有已知可用于Oracle的UPPERCASE类型都可以从顶级方言导入，无论它们源自[`sqlalchemy.types`](core_type_basics.html#module-sqlalchemy.types "sqlalchemy.types")还是来自当地方言：

    from sqlalchemy.dialects.oracle import \
                BFILE, BLOB, CHAR, CLOB, DATE, \
                DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
                NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
                VARCHAR2

特定于Oracle的类型或具有特定于Oracle的构造参数如下所示：

 *class*`sqlalchemy.dialects.oracle.`{.descclassname}`BFILE`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.oracle.BFILE "Permalink to this definition")
:   基础：[`sqlalchemy.types.LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.LargeBinary.__init__ "sqlalchemy.types.LargeBinary.__init__")
        *method of* [`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

        构建一个LargeBinary类型。

        参数：

        **length**[¶](#sqlalchemy.dialects.oracle.BFILE.params.length) –
        optional, a length for the column for use in DDL statements, for
        those binary types that accept a length, such as the MySQL BLOB
        type.

*class* `sqlalchemy.dialects.oracle。`{.descclassname} `DATE`{.descname} （ *timezone = False* ） T5\> [¶ T6\>](#sqlalchemy.dialects.oracle.DATE "Permalink to this definition")
:   Bases: [`sqlalchemy.types.DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

    提供oracle DATE类型。

    这种类型没有特殊的Python行为，除了它的子类[`types.DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")；这是为了适应Oracle
    `DATE`类型支持时间值的事实。

    版本0.9.4中的新功能

    ` __初始化__  T0> （ T1> 时区=假 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的
        [`__init__()`](core_type_basics.html#sqlalchemy.types.DateTime.__init__ "sqlalchemy.types.DateTime.__init__")
        **

        构建一个新的[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")。

        参数：

        **时区** [¶](#sqlalchemy.dialects.oracle.DATE.params.timezone) -
        布尔值。如果为True，并由后端支持，则会产生'TIMESTAMP WITH
        TIMEZONE'。对于不支持时区感知时间戳的后端，不起作用。

*class* `sqlalchemy.dialects.oracle。`{.descclassname} `DOUBLE_PRECISION`{.descname} （ *precision = None*，*scale = None*，*asdecimal = None* ） [¶](#sqlalchemy.dialects.oracle.DOUBLE_PRECISION "Permalink to this definition")
:   基础：[`sqlalchemy.types.Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")

*class* `sqlalchemy.dialects.oracle。`{.descclassname} `INTERVAL`{.descname} （ *day\_precision =无*，*second\_precision =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.oracle.INTERVAL "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

     `__init__`{.descname}(*day\_precision=None*, *second\_precision=None*)[¶](#sqlalchemy.dialects.oracle.INTERVAL.__init__ "Permalink to this definition")
    :   构建一个INTERVAL。

        请注意，目前仅支持DAY TO
        SECOND间隔。这是由于缺少对可用DBAPI（cx\_oracle和zxjdbc）中YEAR
        TO MONTH间隔的支持。

        参数：

        -   **day\_precision**
            [¶](#sqlalchemy.dialects.oracle.INTERVAL.params.day_precision)
            - 日间精确度值。这是一天数字要存储的位数。默认为“2”
        -   **second\_precision**
            [¶](#sqlalchemy.dialects.oracle.INTERVAL.params.second_precision)
            - 第二个精度值。这是小数秒字段存储的位数。默认为“6”。

 *class*`sqlalchemy.dialects.oracle.`{.descclassname}`NCLOB`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.oracle.NCLOB "Permalink to this definition")
:   基础：[`sqlalchemy.types.Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.oracle.NCLOB.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.String.__init__ "sqlalchemy.types.String.__init__")
        *method of* [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

        创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.oracle.NCLOB.params.length)
            – optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理**
            [¶](#sqlalchemy.dialects.oracle.NCLOB.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.dialects.oracle.NCLOB.params.convert_unicode)
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
            [¶](#sqlalchemy.dialects.oracle.NCLOB.params.unicode_error)
            -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

*class* `sqlalchemy.dialects.oracle。`{.descclassname} `NUMBER`{.descname} （ *precision = None*，*scale = None*，*asdecimal = None* ） [¶](#sqlalchemy.dialects.oracle.NUMBER "Permalink to this definition")
:   基础：[`sqlalchemy.types.Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")，[`sqlalchemy.types.Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")

 *class*`sqlalchemy.dialects.oracle.`{.descclassname}`LONG`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.oracle.LONG "Permalink to this definition")
:   基础：[`sqlalchemy.types.Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.dialects.oracle.LONG.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.String.__init__ "sqlalchemy.types.String.__init__")
        *method of* [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

        创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.dialects.oracle.LONG.params.length)
            – optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理**
            [¶](#sqlalchemy.dialects.oracle.LONG.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.dialects.oracle.LONG.params.convert_unicode)
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
            [¶](#sqlalchemy.dialects.oracle.LONG.params.unicode_error) -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

*class* `sqlalchemy.dialects.oracle。`{.descclassname} `RAW  长度=无 ） T5> ¶ T6>`{.descname}
:   基础：`sqlalchemy.types._Binary`

cx\_Oracle [¶ T0\>](#module-sqlalchemy.dialects.oracle.cx_oracle "Permalink to this headline")
----------------------------------------------------------------------------------------------

通过cx-Oracle驱动程序支持Oracle数据库。

### DBAPI [¶ T0\>](#dialect-oracle-cx_oracle-url "Permalink to this headline")

有关cx-Oracle的文档和下载信息（如果适用），请访问：[http://cx-oracle.sourceforge.net/](http://cx-oracle.sourceforge.net/)

### 连接[¶ T0\>](#dialect-oracle-cx_oracle-connect "Permalink to this headline")

连接字符串：

    oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]

### 其他连接参数[¶](#additional-connect-arguments "Permalink to this headline")

与`dbname`连接时，使用cx\_oracle
`makedsn()`函数将主机，端口和dbname标记转换为TNS名称。否则，主机令牌将直接作为TNS名称。

其他参数可以指定为URL上的查询字符串参数，也可以指定为[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的关键字参数：

-   `allow_twophase` -
    启用两阶段交易。默认为`True`。

-   `arraysize` -
    在游标上设置cx\_oracle.arraysize值，默认值为50。这个设置对于cx\_Oracle很重要，因为LOB对象的内容只能在“实时”行中读取（例如在一批50行内）。

-   `auto_convert_lobs` - 默认为True；请参阅[LOB
    Objects](#cx-oracle-lob)。

-   `auto_setinputsizes` -
    为所有绑定参数发出cx\_oracle.setinputsizes()调用。这是LOB数据类型所必需的，但可以禁用以减少开销。默认为`True`。可以使用`exclude_setinputsizes`参数从此过程中排除特定类型。

-   `coerce_to_unicode` -
    详细信息请参阅[Unicode](#cx-oracle-unicode)。

-   `coerce_to_decimal` - 详细请参阅[Precision
    Numerics](#cx-oracle-numeric)。

-   `exclude_setinputsizes` - 要从“auto
    setinputsizes”功能中排除的字符串DBAPI类型名称的元组或列表。此处的类型名称必须与“cx\_Oracle”模块名称空间中找到的DBAPI类型匹配，例如cx\_Oracle.UNICODE，cx\_Oracle.NCLOB等。默认为`（STRING， UNICODE）`。

    版本0.8中的新功能可以通过exclude\_setinputsizes属性从auto\_setinputsizes功能中排除特定的DBAPI类型。

-   `mode` -
    给出SYSDBA或SYSOPER的字符串值，或者一个整数值。该值仅作为URL查询字符串参数使用。

-   `threaded` -
    启用对cx\_oracle连接的多线程访问。默认为`True`。请注意，这是cx\_Oracle DBAPI本身的相反默认值。

-   `service_name` -
    使用连接字符串（DSN）与`SERVICE_NAME`而不是`SID`的选项。当给出`database`部分时，不能传递它。例如。
    `oracle+cx_oracle://scott:tiger@host:1521/?service_name=hr`是一个有效的url。该值仅作为URL查询字符串参数使用。

    版本1.0.0中的新功能

### Unicode的[¶ T0\>](#unicode "Permalink to this headline")

从版本5开始，cx\_Oracle
DBAPI完全支持unicode，并且能够以本地方式将字符串结果作为Python
unicode对象返回。

在Python 3中使用时，cx\_Oracle将所有字符串作为Python
unicode对象（即Python 3中的plain `str`）返回。在Python 2中，它将以Python
unicode的形式返回那些类型为`NVARCHAR`或`NCLOB`的列值。对于类型为`VARCHAR`或其他非Unicode字符串类型的列值，它将以Python字符串（例如，字节串）的形式返回值。

cx\_Oracle SQLAlchemy方言提供了两种不同的选项，用于在Python
2下将`VARCHAR`列值作为Python unicode对象返回：

-   cx\_Oracle
    DBAPI能够无条件地使用输出类型处理程序将所有字符串结果强制转换为Python
    unicode对象。这样做的好处是，对于cx\_Oracle驱动程序级别的所有语句，unicode转换是全局的，这意味着它可以与没有关联输入信息的原始文本SQL语句一起使用。然而，这个系统被认为会产生显着的性能开销，不仅因为它无条件地对所有字符串值生效，而且因为Python
    2下的cx\_Oracle似乎使用纯Python函数调用来执行解码操作，在cPython下比单独使用C函数要慢几个数量级。
-   SQLAlchemy内置了unicode解码服务，当使用SQLAlchemy的C扩展时，这些函数不会使用任何Python函数调用，而且速度非常快。The
    disadvantage to this approach is that the unicode conversion only
    takes effect for statements where the [`Unicode`](core_type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
    type or [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
    type with `convert_unicode=True` is explicitly
    associated with the result column.
    对于任何ORM或核心查询或SQL表达式以及指定输出列类型的[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构，情况都是如此，因此绝大多数情况下这不是问题。然而，当发送一个完整的原始字符串给[`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")时，该输入信息不存在，除非字符串在[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构中处理，输入信息。

从SQLAlchemy
0.9.2版开始，默认方法是使用SQLAlchemy的输入系统。除非用户明确需要，否则这会使cx\_Oracle的昂贵的Python
2方法停用。在Python
3下，SQLAlchemy检测到cx\_Oracle本地返回unicode对象，并使用cx\_Oracle的系统。

要在Python
2下重新启用cx\_Oracle的输出类型处理程序，可以将`coerce_to_unicode=True`标志（0.9.4中的新值）传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")：

    engine = create_engine("oracle+cx_oracle://dsn", coerce_to_unicode=True)

或者，如果不使用cx\_Oracle的本地处理程序，则可以使用[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")功能来运行纯字符串SQL语句并以Python
2 unicode的形式获取`VARCHAR`

    from sqlalchemy import text, Unicode
    result = conn.execute(
        text("select username from user").columns(username=Unicode))

版本0.9.2更改： cx\_Oracle的outputtypehandlers不再用于Python
2中非Unicode数据类型的unicode结果，因为它们被确定为主要的性能瓶颈。而是使用SQLAlchemy自己的unicode工具。

版本0.9.4新增：添加了`coerce_to_unicode`标志，以重新启用cx\_Oracle的outputtypehandler并恢复到0.9.2之前的行为。

### 返回支持[¶](#cx-oracle-returning "Permalink to this headline")

cx\_oracle
DBAPI支持Oracle已经有限的RETURNING支持的有限子集。通常情况下，结果只能保证最多返回一列；这是SQLAlchemy使用RETURNING获取主键关联序列值的典型情况。由于cx\_oracle缺少对更复杂的RETURNING场景所需的OCI\_DATA\_AT\_EXEC
API的支持，因此其他列表达式将以非确定的方式导致问题。

因此，通过完全禁用RETURNING支持可以提高稳定性；否则SQLAlchemy将使用RETURNING来获取新序列生成的主键。如[RETURNING
Support](#oracle-returning)所示：

    engine = create_engine("oracle://scott:tiger@dsn",
                           implicit_returning=False)

也可以看看

[http://docs.oracle.com/cd/B10501\_01/appdev.920/a96584/oci05bnd.htm\#420693](http://docs.oracle.com/cd/B10501_01/appdev.920/a96584/oci05bnd.htm#420693)
- 返回OCI文档

[http://sourceforge.net/mailarchive/message.php?msg\_id=31338136](http://sourceforge.net/mailarchive/message.php?msg_id=31338136)
- cx\_oracle开发者评论

### LOB对象[¶](#lob-objects "Permalink to this headline")

cx\_oracle使用cx\_oracle.LOB对象返回Oracle
LOB。SQLAlchemy将它们转换为字符串，以便Binary类型的接口与其他后端的接口一致，并且在result.fetchmany()和result.fetchall()等场景中不需要与活动游标的链接。这意味着默认情况下，LOB对象无条件地被SQLAlchemy完全取出，并且与活动光标的链接被中断。

要禁用此处理，请将`auto_convert_lobs=False`传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")。

### 两阶段事务支持[¶](#two-phase-transaction-support "Permalink to this headline")

两阶段事务是使用XA事务实现的，并且从SQLAlchemy
0.8.0b2,0.7.10开始，已知以最新版本的cx\_Oracle的基本工作方式工作。但是，该机制尚未被认为是有力的，应该仍然被视为实验性的。

特别是最近5.1.2的cx\_Oracle
DBAPI有一个关于两个阶段的错误，这个阶段阻止了一个特定的DBAPI连接在准备好的事务中以及传统的DBAPI使用模式中始终可用；因此，一旦通过`Connection.begin_prepared()`使用了特定的连接，底层DBAPI连接的所有后续用法都必须位于准备事务的上下文内。

[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的默认行为是维护一个DBAPI连接池。因此，由于上述故障，已在两阶段操作中使用并返回到池的DBAPI连接在非两阶段上下文中将不可用。为了避免这种情况，应用程序可以做出以下几种选择之一：

-   使用[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")禁用连接池
-   确保正在使用的特定[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")仅用于两阶段操作。绑定到包含`twophase=True`的ORM [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")将一致使用两阶段事务样式。
-   对于没有禁用池的临时两阶段操作，可以使用[`Connection.detach()`](core_connections.html#sqlalchemy.engine.Connection.detach "sqlalchemy.engine.Connection.detach")方法从连接池中清除正在使用的DBAPI连接。

在0.8.0b2,0.7.10版本中更改：已执行并测试了对cx\_oracle准备事务的支持。

### 精确数字[¶](#precision-numerics "Permalink to this headline")

SQLAlchemy方言经历了很多步骤以确保十进制数字的发送和接收完全准确。可调用的“outputtypehandler”与每个检测数字类型并将其作为字符串值接收的cx\_oracle连接对象相关联，而不是直接接收Python
`float`，然后将其传递给Python `Decimal`在cx\_oracle方言下的[`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")和[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")类型意识到这种行为，并且强制`Decimal`到`float`如果`asdecimal`标志为`False`（默认在[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")，[`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")上可选）。

由于处理程序首先在所有情况下都强制`Decimal`，该功能会显着影响性能。如果不需要精度数字，则可以通过将标志`coerce_to_decimal=False`传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")来禁用十进制处理：

    engine = create_engine("oracle+cx_oracle://dsn", coerce_to_decimal=False)

New in version 0.7.6: Add the `coerce_to_decimal`
flag.

性能的另一种替代方法是使用[cdecimal](http://pypi.python.org/pypi/cdecimal/)库；有关其他注意事项，请参阅[`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")。

该处理程序试图使用结果集列的“精度”和“比例”属性来最好地确定后续输入值是否应该被接收为`Decimal`而不是int（在这种情况下，不会添加处理）。There are several
scenarios where
[OCI](http://www.oracle.com/technetwork/database/features/oci/index.html)
does not provide unambiguous data as to the numeric type, including some
situations where individual rows may return a combination of floating
point and integer values.
已经观察到“精确度”和“比例”的某些值来确定这种情况。当它发生时，outputtypehandler接收到一个字符串，然后传递给一个处理函数，该函数检测每个返回值是否存在小数点，如果是，则转换为`Decimal`，否则转换为int。The intention is that simple int-based
statements like “SELECT my\_seq.nextval() FROM DUAL” continue to return
ints and not `Decimal` objects, and that any kind of
floating point value is received as a string so that there is no
floating point loss of precision.

“存在小数点”逻辑本身对区域设置也很敏感。在[OCI](http://www.oracle.com/technetwork/database/features/oci/index.html)下，这由NLS\_LANG环境变量控制。首次连接时，方言进行测试以确定当前的“十进制”字符，对于欧洲语言环境，该字符可以是逗号“，”。从这一点开始，outputtypehandler使用该字符来表示小数点。请注意，在处理带有不使用句点“。”作为十进制字符的区域设置的数字时，需要cx\_oracle
5.0.3或更高版本。

在版本0.6.6中更改：
outputtypehandler支持locale使用逗号“，”字符表示小数点的情况。

zxjdbc [¶ T0\>](#module-sqlalchemy.dialects.oracle.zxjdbc "Permalink to this headline")
---------------------------------------------------------------------------------------

通过zxJDBC为Jython驱动程序支持Oracle数据库。

注意

当前版本的SQLAlchemy不支持Jython。zxjdbc方言应该被认为是实验性的。

### DBAPI [¶ T0\>](#dialect-oracle-zxjdbc-url "Permalink to this headline")

此数据库的驱动程序可在以下网址找到：[http://www.oracle.com/technetwork/database/features/jdbc/index-091264.html](http://www.oracle.com/technetwork/database/features/jdbc/index-091264.html)

### 连接[¶ T0\>](#dialect-oracle-zxjdbc-connect "Permalink to this headline")

连接字符串：

    oracle+zxjdbc://user:pass@host/dbname
