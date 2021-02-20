---
title: changelog_10
date: 2021-02-20 22:41:30
permalink: /pages/738384/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
1.0更新日志[¶](#changelog "Permalink to this headline")
=======================================================

1.0.14 [¶ T0\>](#change-1.0.14 "Permalink to this headline")
------------------------------------------------------------

没有发布日期

### 发动机[¶ T0\>](#change-1.0.14-engine "Permalink to this headline")

-   **[engine] [bug]
    [postgresql]**修复了跨模式外键反射和[`MetaData.schema`](core_metadata.html#sqlalchemy.schema.MetaData.params.schema "sqlalchemy.schema.MetaData")参数的错误，其中存在“默认”模式将失败，因为无法指示模式具有“空白”的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。特殊符号[`schema.BLANK_SCHEMA`](core_metadata.html#sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA "sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA")已添加为[`Table.schema`](core_metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")和[`Sequence.schema`](core_defaults.html#sqlalchemy.schema.Sequence.params.schema "sqlalchemy.schema.Sequence")的可用值，表明模式名称应该是即使指定了[`MetaData.schema`](core_metadata.html#sqlalchemy.schema.MetaData.params.schema "sqlalchemy.schema.MetaData")，也必须被强制为`None` [¶](#change-4d7092660a51f02cf6ae2adb3e0a7fb6)

    参考文献：[＃3716](http://www.sqlalchemy.org/trac/ticket/3716)

### SQL [¶ T0\>](#change-1.0.14-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed issue in SQL math negation operator where the
    type of the expression would no longer be the numeric type of the
    original.
    这会导致类型确定结果集行为的问题。[¶](#change-2758e73b99ac7bb6a36bd8651bd1e56c)

    参考文献：[＃3735](http://www.sqlalchemy.org/trac/ticket/3735)

-   **[sql] [bug]**Fixed bug whereby the `__getstate__` / `__setstate__` methods for
    sqlalchemy.util.Properties were non-working due to the transition in
    the 1.0 series to `__slots__`.
    该问题可能会影响某些第三方应用程序。Pull请求Pieter
    Mulder提供。[¶](#change-c7059eb3012401b413610d88be5d7bb5)

    参考文献：[＃3728](http://www.sqlalchemy.org/trac/ticket/3728)

-   **[sql] [bug]** [`FromClause.count()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")正在等待1.1弃用。该函数使用表中的任意列并且不可靠；对于核心用途，应该首选`func.count()`。[¶](#change-a725e879b7b24fb36799bb76f3075d43)

    参考文献：[＃3724](http://www.sqlalchemy.org/trac/ticket/3724)

-   **[sql] [bug]**Fixed bug in [`CTE`](core_selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")
    structure which would cause it to not clone properly when a union
    was used, as is common in a recursive CTE.
    当CTE用于各种ORM环境（如[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")）时，错误的克隆会导致错误。[¶](#change-677e6c0535709018e57bdb8c064e546b)

    参考文献：[＃3722](http://www.sqlalchemy.org/trac/ticket/3722)

-   **[sql] [bug]**Fixed bug whereby [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    would make a duplicate [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
    for each [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object that featured the `unique=True`
    parameter.[¶](#change-4bb322d1beae4370564be99c7589c055)

    参考文献：[＃3721](http://www.sqlalchemy.org/trac/ticket/3721)

### 杂项[¶ T0\>](#change-1.0.14-misc "Permalink to this headline")

-   **[bug] [examples]**修复了examples / vertical /
    dictlike-polymorphic.py示例中发生的回退，该示例阻止其运行。[¶](#change-9c468f38b3c1e3c6dad918aec4386076)

    参考文献：[＃3704](http://www.sqlalchemy.org/trac/ticket/3704)

1.0.13 [¶ T0\>](#change-1.0.13 "Permalink to this headline")
------------------------------------------------------------

发布日期：2016年5月16日

### ORM [¶ T0\>](#change-1.0.13-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug in “evaluate” strategy of
    [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    and [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
    which would fail to accommodate a bound parameter with a “callable”
    value, as which occurs when filtering by a many-to-one equality
    expression along a
    relationship.[¶](#change-2047da33c78a202b1bd91983d30b7f8d)

    参考文献：[＃3700](http://www.sqlalchemy.org/trac/ticket/3700)

-   **[orm] [bug]**Fixed bug whereby the event listeners used for
    backrefs could be inadvertently applied multiple times, when using a
    deep class inheritance hierarchy in conjunction with mutiple mapper
    configuration steps.[¶](#change-5ac1c8a6e97310c3cea38f3a2cb45f13)

    参考文献：[＃3710](http://www.sqlalchemy.org/trac/ticket/3710)

-   **[orm] [bug]**Fixed bug whereby passing a [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct to the [`Query.group_by()`](orm_query.html#sqlalchemy.orm.query.Query.group_by "sqlalchemy.orm.query.Query.group_by")
    method would raise an error, instead of intepreting the object as a
    SQL fragment.[¶](#change-9b9c7cae32bb4c15ebd406b980edc2ba)

    参考文献：[＃3706](http://www.sqlalchemy.org/trac/ticket/3706)

-   **[orm] [bug]**Anonymous labeling is applied to a [`func`](core_sqlelement.html#sqlalchemy.sql.expression.Over.func "sqlalchemy.sql.expression.Over.func")
    construct that is passed to [`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
    so that if the same attribute is referred to as a column expression
    twice the names are de-duped, thus avoiding “ambiguous column”
    errors. 以前，需要应用`.label(None)`才能使名称匿名化。[¶](#change-e6ed5fa4fecae4a5036905ffce1a3264)

    参考文献：[＃3663](http://www.sqlalchemy.org/trac/ticket/3663)

-   **[orm] [bug]**Fixed regression appearing in the 1.0 series in ORM
    loading where the exception raised for an expected column missing
    would incorrectly be a `NoneType` error, rather
    than the expected [`NoSuchColumnError`](core_exceptions.html#sqlalchemy.exc.NoSuchColumnError "sqlalchemy.exc.NoSuchColumnError").[¶](#change-e3c6db557cf0e220505ebe362aaa2c9a)

    参考文献：[＃3658](http://www.sqlalchemy.org/trac/ticket/3658)

### SQL [¶ T0\>](#change-1.0.13-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug where when using
    `case_sensitive=False` with an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
    the result set would fail to correctly accomodate for duplicate
    column names in the result set, causing an error when the statement
    is executed in 1.0, and preventing the “ambiguous column” exception
    from functioning in
    1.1.[¶](#change-e022b554a55b57090216a01e442216d2)

    参考文献：[＃3690](http://www.sqlalchemy.org/trac/ticket/3690)

-   **[sql] [bug]**Fixed bug where the negation of an EXISTS expression
    would not be properly typed as boolean in the result, and also would
    fail to be anonymously aliased in a SELECT list as is the case with
    a non-negated EXISTS
    construct.[¶](#change-1bce768d6b81f3ad8d7eba8903728cfd)

    参考文献：[＃3682](http://www.sqlalchemy.org/trac/ticket/3682)

-   **[sql] [bug]**Fixed bug where “unconsumed column names” exception
    would fail to be raised in the case where [`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
    were called with a list of parameter mappings, instead of a single
    mapping of parameters. 拉请求Athena
    Yao提供。[¶](#change-2e70457f8ab9bf40e7fc276889b3238c)

    参考文献：[＃3666](http://www.sqlalchemy.org/trac/ticket/3666)

### 的PostgreSQL [¶ T0\>](#change-1.0.13-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**为错误字符串“SSL错误：解密失败或错误的记录mac”添加了断开连接检测支持。请求礼物Iuri
    de Silvio。[¶](#change-4a61289d79705f08bb15de8e6321af41)

    参考文献：[＃3715](http://www.sqlalchemy.org/trac/ticket/3715)

### MSSQL [¶ T0\>](#change-1.0.13-mssql "Permalink to this headline")

-   **[mssql] [bug]**Fixed bug where by ROW\_NUMBER OVER clause applied
    for OFFSET selects in SQL Server would inappropriately substitute a
    plain column from the local statement that overlaps with a label
    name used by the ORDER BY criteria of the
    statement.[¶](#change-e40583c1813139df7c799fc9928d38ae)

    参考文献：[＃3711](http://www.sqlalchemy.org/trac/ticket/3711)

-   **[mssql] [bug] [oracle]**Fixed regression appearing in the 1.0
    series which would cause the Oracle and SQL Server dialects to
    incorrectly account for result set columns when these dialects would
    wrap a SELECT in a subquery in order to provide LIMIT/OFFSET
    behavior, and the original SELECT statement referred to the same
    column multiple times, such as a column and a label of that same
    column. This issue is related to
    [\#3658](http://www.sqlalchemy.org/trac/ticket/3658) in that when
    the error occurred, it would also cause a `NoneType` error, rather than reporting that it couldn’t locate a
    column.[¶](#change-7b9781fe3242062ab2446367b4733bad)

    参考文献：[＃3657](http://www.sqlalchemy.org/trac/ticket/3657)

### 预言[¶ T0\>](#change-1.0.13-oracle "Permalink to this headline")

-   **[oracle]
    [bug]**修复了cx\_Oracle连接过程中的错误，当用户，密码或dsn为空时导致TypeError。这阻止了对Oracle数据库的外部认证，并阻止了连接到默认的dsn。连接字符串oracle：//现在使用操作系统用户名登录到默认dsn，相当于使用'/'连接sqlplus。[¶](#change-3d8ee495a3a4567137de79dfb9d0f81e)

    参考文献：[＃3705](http://www.sqlalchemy.org/trac/ticket/3705)

-   **[oracle] [bug]**Fixed a bug in the result proxy used mainly by
    Oracle when binary and other LOB types are in play, such that when
    query / statement caching were used, the type-level result
    processors, notably that required by the binary type itself but also
    any other processor, would become lost after the first run of the
    statement due to it being removed from the cached result
    metadata.[¶](#change-bada3dbba27a01629133de2f2f598b63)

    参考文献：[＃3699](http://www.sqlalchemy.org/trac/ticket/3699)

### 杂项[¶ T0\>](#change-1.0.13-misc "Permalink to this headline")

-   **[bug]
    [examples]**将“有向图”示例更改为不再将节点的整数标识符视为重要；
    “较高”/“较低”参考现在允许两个方向上的相互边缘。[¶](#change-1a55117321e17e5d36db13e1b974446e)

    参考文献：[＃3698](http://www.sqlalchemy.org/trac/ticket/3698)

-   **[bug]
    [py3k]**修正了“to\_list”转换中的错误，其中单个字节对象将变成单个字符列表。这将对使用字节对象的主键上的[`Query.get()`](orm_query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")方法产生影响。[¶](#change-a14dd2e73d889d065acc07a77b1ee7cb)

    参考文献：[＃3660](http://www.sqlalchemy.org/trac/ticket/3660)

1.0.12 [¶ T0\>](#change-1.0.12 "Permalink to this headline")
------------------------------------------------------------

发布日期：2016年2月15日

### ORM [¶ T0\>](#change-1.0.12-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug in [`Session.merge()`](orm_session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
    where an object with a composite primary key that has values for
    some but not all of the PK fields would emit a SELECT statement
    leaking the internal NEVER\_SET symbol into the query, rather than
    detecting that this object does not have a searchable primary key
    and no SELECT should be
    emitted.[¶](#change-39c398de2662e9f45aae57c76c6444c9)

    参考文献：[＃3647](http://www.sqlalchemy.org/trac/ticket/3647)

-   **[orm]
    [bug]**从0.9版本开始修正了回归，0.9样式加载器选项系统在单个查询中无法适应多个[`undefer_group()`](orm_loading_columns.html#sqlalchemy.orm.undefer_group "sqlalchemy.orm.undefer_group")加载器选项。现在即使对同一实体也会考虑多个[`undefer_group()`](orm_loading_columns.html#sqlalchemy.orm.undefer_group "sqlalchemy.orm.undefer_group")选项。[¶](#change-57d791a5552fab41d8a0e788f4324f65)

    参考文献：[＃3623](http://www.sqlalchemy.org/trac/ticket/3623)

### 发动机[¶ T0\>](#change-1.0.12-engine "Permalink to this headline")

-   **[engine] [bug] [mysql]**Revisiting
    [\#2696](http://www.sqlalchemy.org/trac/ticket/2696), first released
    in 1.0.10, which attempts to work around Python 2’s lack of
    exception context reporting by emitting a warning for an exception
    that was interrupted by a second exception when attempting to roll
    back the already-failed transaction; this issue continues to occur
    for MySQL backends in conjunction with a savepoint that gets
    unexpectedly lost, which then causes a “no such savepoint” error
    when the rollback is attempted, obscuring what the original
    condition was.

    这种方法已被推广到核心“安全重新评估”功能，该功能通过ORM和Core在任何发生尝试提交的错误时回滚事务的地方发生，包括由[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")和[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，并发生诸如“RELEASE
    SAVEPOINT”发生故障等操作。以前，修复只适用于ORM刷新/提交过程中的特定路径；它现在也适用于所有跨国上下文管理者。

    [¶](#change-7706b7fbecdb21a5157da093a88b9134)

    参考文献：[＃2696](http://www.sqlalchemy.org/trac/ticket/2696)

### SQL [¶ T0\>](#change-1.0.12-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed issue where the “literal\_binds” flag was not
    propagated for [`expression.insert()`](core_dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"),
    [`expression.update()`](core_dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")
    or [`expression.delete()`](core_dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")
    constructs when compiled to string SQL. 请求提供Tim
    Tate。[¶](#change-fa04be1b3106d6859abbc1ade87df175)

    参考文献：[＃3643](http://www.sqlalchemy.org/trac/ticket/3643)，[请求github：232](https://github.com/zzzeek/sqlalchemy/pull/232)

-   **[sql] [bug]**Fixed issue where inadvertent use of the Python
    `__contains__` override with a column expression
    (e.g. by using `'x' in col`) would cause an
    endless loop in the case of an ARRAY type, as Python defers this to
    `__getitem__` access which never raises for this
    type. 总的来说，所有使用`__contains__`现在引发NotImplementedError。[¶](#change-6893173c723cb93efd613ae892e07abf)

    参考文献：[＃3642](http://www.sqlalchemy.org/trac/ticket/3642)

-   **[sql] [bug]**Fixed bug in [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    metadata construct which appeared around the 0.9 series where adding
    columns to a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    that was unpickled would fail to correctly establish the
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    within the ‘c’ collection, leading to issues in areas such as ORM
    configuration. 这可能会影响`extend_existing`等用例。[¶](#change-5c11bdb4bef5dc9140eedb095bb42a18)

    参考文献：[＃3632](http://www.sqlalchemy.org/trac/ticket/3632)

### 的PostgreSQL [¶ T0\>](#change-1.0.12-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**修正了[`expression.text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构中双冒号表达式无法正确转义的问题。
    `some\:\:expr`，这是在呈现Postgresql样式的CAST表达式时最常用的。[¶](#change-5b66b429f55459d303aa6d7335f13701)

    参考文献：[＃3644](http://www.sqlalchemy.org/trac/ticket/3644)

### MSSQL [¶ T0\>](#change-1.0.12-mssql "Permalink to this headline")

-   **[mssql] [bug]**Fixed the syntax of the [`extract()`](core_sqlelement.html#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")
    function when used on MSSQL against a datetime value; the quotes
    around the keyword are removed. 拉请求礼貌Guillaume
    Doumenc。[¶](#change-d6c62d538d019244e6eb27d263e868e8)

    参考文献：[＃3624](http://www.sqlalchemy.org/trac/ticket/3624)，[拉取请求bitbucket：70](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/70)

-   **[mssql] [bug] [firebird]**Fixed 1.0 regression where the eager
    fetch of cursor.rowcount was no longer called for an UPDATE or
    DELETE statement emitted via plain text or via the [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct, affecting those drivers that erase cursor.rowcount once
    the cursor is closed such as SQL Server ODBC and Firebird
    drivers.[¶](#change-b44f1e43ef8e623b9de9ddc5c66d716a)

    参考文献：[＃3622](http://www.sqlalchemy.org/trac/ticket/3622)

### 预言[¶ T0\>](#change-1.0.12-oracle "Permalink to this headline")

-   **[oracle] [bug] [jython]**Fixed a small issue in the Jython Oracle
    compiler involving the rendering of “RETURNING” which allows this
    currently unsupported/untested dialect to work rudimentally with the
    1.0 series.
    请求卡洛斯里瓦斯请求。[¶](#change-43abedf27e93fb6c494d01efb423d1af)

    参考文献：[＃3621](http://www.sqlalchemy.org/trac/ticket/3621)

### 杂项[¶ T0\>](#change-1.0.12-misc "Permalink to this headline")

-   **[bug] [py3k]**Fixed bug where some exception re-raise scenarios
    would attach the exception to itself as the “cause”; while the
    Python 3 interpreter is OK with this, it could cause endless loops
    in iPython.[¶](#change-8aa9c8209b565aaa4251a73d5815aa70)

    参考文献：[＃3625](http://www.sqlalchemy.org/trac/ticket/3625)

1.0.11 [¶ T0\>](#change-1.0.11 "Permalink to this headline")
------------------------------------------------------------

发布日期：2015年12月22日

### ORM [¶ T0\>](#change-1.0.11-orm "Permalink to this headline")

-   **[orm]
    [bug]**修正了1.0.10中由[＃3593](http://www.sqlalchemy.org/trac/ticket/3593)修复引起的回归，其中为来自poly\_subclass-\>
    class-\> poly\_baseclass的多态连接加载添加了检查连接将失败的类 - \>
    poly\_subclass-\>类的情况。[¶](#change-14de383393c0c9af155b092fdecf8101)

    参考文献：[＃3611](http://www.sqlalchemy.org/trac/ticket/3611)

-   **[orm] [bug]**Fixed bug where
    [`Session.bulk_update_mappings()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")
    and related would not bump a version id counter when in use.
    这里的经验仍然有点粗糙，因为在给定字典中需要原始版本ID，并且还没有干净的错误报告。[¶](#change-02da59abe1c57d8646747495298a98c5)

    参考文献：[＃3610](http://www.sqlalchemy.org/trac/ticket/3610)

-   **[orm] [bug]**Major fixes to the [`Mapper.eager_defaults`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.params.eager_defaults "sqlalchemy.orm.mapper.Mapper")
    flag, this flag would not be honored correctly in the case that
    multiple UPDATE statements were to be emitted, either as part of a
    flush or a bulk update operation.
    此外，RETURNING将在更新语句中不必要地发出。[¶](#change-b0b97f1c028f72f272a01f842b36d622)

    参考文献：[＃3609](http://www.sqlalchemy.org/trac/ticket/3609)

-   **[orm] [bug]**Fixed bug where use of the
    [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    method would cause a subsequent call to the
    [`Query.with_parent()`](orm_query.html#sqlalchemy.orm.query.Query.with_parent "sqlalchemy.orm.query.Query.with_parent")
    method to fail.[¶](#change-b1030568ebfc6b93a82a5eba2ed64e72)

    参考文献：[＃3606](http://www.sqlalchemy.org/trac/ticket/3606)

### SQL [¶ T0\>](#change-1.0.11-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug in [`Update.return_defaults()`](core_dml.html#sqlalchemy.sql.expression.Update.return_defaults "sqlalchemy.sql.expression.Update.return_defaults")
    which would cause all insert-default holding columns not otherwise
    included in the SET clause (such as primary key cols) to get
    rendered into the RETURNING even though this is an
    UPDATE.[¶](#change-e8ae984d3fe8f909f4e67567acda10e1)

    参考文献：[＃3609](http://www.sqlalchemy.org/trac/ticket/3609)

### MySQL的[¶ T0\>](#change-1.0.11-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**调整用于解析MySQL视图的正则表达式，以便我们不再假设反射视图源中存在“ALGORITHM”关键字，因为有些用户已经报告过在某些Amazon
    RDS环境中不存在。[¶](#change-c1b3ad084945fc5a7f4d711d989ebdf2)

    参考文献：[＃3613](http://www.sqlalchemy.org/trac/ticket/3613)

-   **[mysql] [bug]**为MySQL
    5.7增加了MySQL保留字，包括'generated'，'optimizer\_costs'，'stored'，'virtual'。请求礼貌Hanno
    Schlichting。[¶](#change-62b28bb5936942f4483f018dacdaac57)

    参考文献：[请求github：222](https://github.com/zzzeek/sqlalchemy/pull/222)

### 杂项[¶ T0\>](#change-1.0.11-misc "Permalink to this headline")

-   **[bug]
    [ext]**进一步修正[＃3605](http://www.sqlalchemy.org/trac/ticket/3605)，[`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")上的弹出方法，其中未包含“default”参数[¶
    T6\>](#change-134a03f81d13c85951a47bd2a9b7b9a1)

    参考文献：[＃3605](http://www.sqlalchemy.org/trac/ticket/3605)

-   **[bug] [ext]**Fixed bug in baked loader system where the systemwide
    monkeypatch for setting up baked lazy loaders would interfere with
    other loader strategies that rely on lazy loading as a fallback,
    e.g. joined and subquery eager loaders, leading to
    `IndexError` exceptions at mapper configuration
    time.[¶](#change-9e6966523927542f8808ecf8005c6737)

    参考文献：[＃3612](http://www.sqlalchemy.org/trac/ticket/3612)

1.0.10 [¶ T0\>](#change-1.0.10 "Permalink to this headline")
------------------------------------------------------------

发布日期：2015年12月11日

### ORM [¶ T0\>](#change-1.0.10-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed issue where post\_update on a many-to-one
    relationship would fail to emit an UPDATE in the case where the
    attribute were set to None and not previously
    loaded.[¶](#change-0fc136fefdb6fd903b2e0036636f6328)

    参考文献：[＃3599](http://www.sqlalchemy.org/trac/ticket/3599)

-   **[orm]
    [bug]**修正了错误，这实际上是由于[＃2714](http://www.sqlalchemy.org/trac/ticket/2714)而在版本0.8.0和0.8.1之间发生的回归。当“with\_polymorphic”也被使用时，加入的渴望加载需要连接到子类绑定关系的情况将无法从正确的实体中加入。[¶](#change-d64c29536ad61c8d456ffd6b38359a9f)

    参考文献：[＃3593](http://www.sqlalchemy.org/trac/ticket/3593)

-   **[orm]
    [bug]**修正了当a。该查询包含强制子查询b的限制/偏移量标准。该关系使用“次要”c。关系的主连接是指不是主键的一部分的列，或者是在与父表的主键列d不同的属性名下的连接继承子类表中的PK列。查询将延迟primaryjoin中存在的列，通常不会包含在load\_only()中；子查询中不会出现必要的列并产生无效的SQL。[¶](#change-8804e40dd20d4c09ef022fe4e8881288)

    参考文献：[＃3592](http://www.sqlalchemy.org/trac/ticket/3592)

-   **[orm] [bug]**A rare case which occurs when a
    [`Session.rollback()`](orm_session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
    fails in the scope of a [`Session.flush()`](orm_session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
    operation that’s raising an exception, as has been observed in some
    MySQL SAVEPOINT cases, prevents the original database exception from
    being observed when it was emitted during flush, but only on Py2K
    because Py2K does not support exception chaining; on Py3K the
    originating exception is chained.
    作为一种解决方法，在我们继续引发回滚起始异常之前，在这个特定情况下会发出警告，至少显示原始数据库错误的字符串消息。[¶](#change-b70e428b82707f753989ef9820a13e0d)

    参考文献：[＃2696](http://www.sqlalchemy.org/trac/ticket/2696)

### orm declarative [¶](#change-1.0.10-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**Fixed bug where in Py2K a unicode
    literal would not be accepted as the string name of a class or other
    argument within declarative using [`backref()`](orm_relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")
    on [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship").
    拉尔请求礼貌Nils
    Philippsen。[¶](#change-9794c3c81c4b53dbb39703dcad6555dc)

    参考文献：[请求github：212](https://github.com/zzzeek/sqlalchemy/pull/212)

### SQL [¶ T0\>](#change-1.0.10-sql "Permalink to this headline")

-   **[sql]
    [feature]**增加了对UPDATE语句中参数排序的SET子句的支持。通过将[`preserve_parameter_order`](core_dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志传递给核心[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构或者将其添加到[`Query.update.update_args`](orm_query.html#sqlalchemy.orm.query.Query.update.params.update_args "sqlalchemy.orm.query.Query.update")字典ORM级别，还将参数本身作为2元组列表传递。感谢Gorka
    Eguileor进行实施和测试。

    也可以看看

    [Parameter-Ordered
    Updates](core_tutorial.html#updates-order-parameters)

    [¶](#change-4f37b666e375903193eb70016d8146b6)

    参考文献：[请求github：200](https://github.com/zzzeek/sqlalchemy/pull/200)

-   **[sql] [bug]**Fixed issue within the [`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
    construct whereby the [`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
    construct would have its `._raw_columns`
    collection mutated in-place when compiling the [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
    construct, when the target [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    has Python-side defaults. 在编译[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")之后，[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")结构将独立编译出现错误的列，并且[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句本身会在一秒钟后失败由于重复的绑定参数而导致的编译尝试。[¶](#change-88ed0853e830fdd4b502a42c53f9834a)

    参考文献：[＃3603](http://www.sqlalchemy.org/trac/ticket/3603)

-   **[sql] [bug] [postgresql]**Fixed bug where CREATE TABLE with a
    no-column table, but a constraint such as a CHECK constraint would
    render an erroneous comma in the definition; this scenario can occur
    such as with a Postgresql INHERITS table that has no columns of its
    own.[¶](#change-cbe154666f524c9aa07e3106e8574c65)

    参考文献：[＃3598](http://www.sqlalchemy.org/trac/ticket/3598)

### 的PostgreSQL [¶ T0\>](#change-1.0.10-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**Fixed issue where the “FOR UPDATE OF”
    Postgresql-specific SELECT modifier would fail if the referred table
    had a schema qualifier; PG needs the schema name to be omitted.
    拉请求礼貌戴安娜克拉克。[¶](#change-fdd814f30b8ba213274656c1948795cb)

    参考文献：[＃3573](http://www.sqlalchemy.org/trac/ticket/3573)，[请求github：216](https://github.com/zzzeek/sqlalchemy/pull/216)

-   **[postgresql] [bug]**Fixed bug where some varieties of SQL
    expression passed to the “where” clause of
    [`postgresql.ExcludeConstraint`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint "sqlalchemy.dialects.postgresql.ExcludeConstraint")
    would fail to be accepted correctly.
    拉请求礼貌aisch。[¶](#change-ae0c216328001852e3c068b6bef5438b)

    参考文献：[请求github：215](https://github.com/zzzeek/sqlalchemy/pull/215)

-   **[postgresql] [bug]**修复了[`postgresql.INTERVAL`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL "sqlalchemy.dialects.postgresql.INTERVAL")的`.python_type`属性以返回`datetime.timedelta`与`types.Interval.python_type`相同，而不是引发`NotImplementedError`。[¶](#change-d0267c6d6507bf37598b0250b57cd5f7)

    参考文献：[＃3571](http://www.sqlalchemy.org/trac/ticket/3571)

### MySQL的[¶ T0\>](#change-1.0.10-mysql "Permalink to this headline")

-   **[mysql] [bug]**Fixed bug in MySQL reflection where the “fractional
    sections portion” of the [`mysql.DATETIME`](dialects_mysql.html#sqlalchemy.dialects.mysql.DATETIME "sqlalchemy.dialects.mysql.DATETIME"),
    [`mysql.TIMESTAMP`](dialects_mysql.html#sqlalchemy.dialects.mysql.TIMESTAMP "sqlalchemy.dialects.mysql.TIMESTAMP")
    and [`mysql.TIME`](dialects_mysql.html#sqlalchemy.dialects.mysql.TIME "sqlalchemy.dialects.mysql.TIME")
    types would be incorrectly placed into the `timezone` attribute, which is unused by MySQL, instead of the
    `fsp`
    attribute.[¶](#change-6974522ee331218a2318e6b0dc52bebd)

    参考文献：[＃3602](http://www.sqlalchemy.org/trac/ticket/3602)

### MSSQL [¶ T0\>](#change-1.0.10-mssql "Permalink to this headline")

-   **[mssql]
    [bug]**将错误“20006：写入服务器失败”添加到pymssql驱动程序的断开连接错误列表中，因为已经发现这会导致连接不可用。[¶
    T2\>](#change-be7c80f619f565c72db723a14bcbeba8)

    参考文献：[＃3585](http://www.sqlalchemy.org/trac/ticket/3585)

-   **[mssql]
    [bug]**如果SQL服务器从DATE或TIME列中返回无效的日期或时间格式，而不是失败并返回一个NoneType错误，则会引发一个描述性的ValueError。请求礼貌Ed
    Avis。[¶](#change-ee5c541eb9c67a758fa50b2406d4ff75)

    参考文献：[请求github：206](https://github.com/zzzeek/sqlalchemy/pull/206)

-   **[mssql] [bug]**Fixed issue where DDL generated for the MSSQL types
    DATETIME2, TIME and DATETIMEOFFSET with a precision of “zero” would
    not generate the precision field. 请求礼貌Jacobo de
    Vera。[¶](#change-da04d72c61e38ea860c327ffdd4d41e2)

    参考文献：[请求github：213](https://github.com/zzzeek/sqlalchemy/pull/213)

### 杂项[¶ T0\>](#change-1.0.10-misc "Permalink to this headline")

-   **[bug] [ext]**Added support for the `dict.pop()` and `dict.popitem()` methods to the
    [`mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    class.[¶](#change-1fe7359b44816908ec7c979731f2d99f)

    参考文献：[＃3605](http://www.sqlalchemy.org/trac/ticket/3605)

-   **[bug] [py3k]**Updates to internal getargspec() calls, some
    py36-related fixture updates, and alterations to two iterators to
    “return” instead of raising StopIteration, to allow tests to pass
    without errors or warnings on Py3.5, Py3.6, pull requests courtesy
    Jacob MacDonald, Luri de Silvio, and Phil
    Jones.[¶](#change-19c50f7c3ae4d9fc7e580152f196f68d)

    引用：[请求github：210](https://github.com/zzzeek/sqlalchemy/pull/210)，[请求github：218](https://github.com/zzzeek/sqlalchemy/pull/218)，[请求github：211](https://github.com/zzzeek/sqlalchemy/pull/211)

-   **[bug] [ext]**Fixed an issue in baked queries where the .get()
    method, used either directly or within lazy loads, didn’t consider
    the mapper’s “get clause” as part of the cache key, causing bound
    parameter mismatches if the clause got re-generated.
    该子句由mappers实时缓存，但在高度并发的情况下，第一次访问时可能会多次生成。[¶](#change-8403645e6ecab28e501dbfb4d00224fd)

    参考文献：[＃3597](http://www.sqlalchemy.org/trac/ticket/3597)

-   **[tests] [change]** ORM和Core教程始终处于doctest格式，现在在Python
    2和Python
    3的普通单元测试套件中运行。[T2\>](#change-679c9f0f8241f2d807a6d969b04062ac)

1.0.9 [¶ T0\>](#change-1.0.9 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年10月20日

### ORM [¶ T0\>](#change-1.0.9-orm "Permalink to this headline")

-   **[orm] [feature]**增加了新的方法[`Query.one_or_none()`](orm_query.html#sqlalchemy.orm.query.Query.one_or_none "sqlalchemy.orm.query.Query.one_or_none")；与[`Query.one()`](orm_query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")相同，但如果未找到任何行，则返回None。请求礼貌esiegerman。[¶](#change-036a3c5dc5a79efaf54c986efe1de824)

    参考文献：[请求github：201](https://github.com/zzzeek/sqlalchemy/pull/201)

-   **[orm] [bug] [postgresql]**Fixed regression in 1.0 where new
    feature of using “executemany” for UPDATE statements in the ORM
    (e.g. [UPDATE statements are now batched with executemany() in a
    flush](migration_10.html#feature-updatemany)) would break on
    Postgresql and other RETURNING backends when using server-side
    version generation schemes, as the server side value is retrieved
    via RETURNING which is not supported with
    executemany.[¶](#change-60963a199ad3f0a534b9a82b4b2fae67)

    参考文献：[＃3556](http://www.sqlalchemy.org/trac/ticket/3556)

-   **[orm] [bug]**Fixed rare TypeError which could occur when
    stringifying certain kinds of internal column loader options within
    internal logging.[¶](#change-8afb9b23354a19cca287e476b397cd10)

    参考文献：[＃3539](http://www.sqlalchemy.org/trac/ticket/3539)

-   **[orm] [bug]**Fixed bug in [`Session.bulk_save_objects()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")
    where a mapped column that had some kind of “fetch on update” value
    and was not locally present in the given object would cause an
    AttributeError within the
    operation.[¶](#change-28c1d20d00a8faa94ad7c40b4b239a48)

    参考文献：[＃3525](http://www.sqlalchemy.org/trac/ticket/3525)

-   **[orm] [bug]**Fixed 1.0 regression where the “noload” loader
    strategy would fail to function for a many-to-one relationship.
    加载器使用API​​将“无”放入不再实际写入值的字典中；这是[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)。[¶](#change-05874c2cf9d4c41757ed8ac0c488bdec)的副作用

    参考文献：[＃3510](http://www.sqlalchemy.org/trac/ticket/3510)

### SQL [¶ T0\>](#change-1.0.9-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed regression in 1.0-released default-processor
    for multi-VALUES insert statement,
    [\#3288](http://www.sqlalchemy.org/trac/ticket/3288), where the
    column type for the default-holding column would not be propagated
    to the compiled statement in the case where the default was being
    used, leading to bind-level type handlers not being
    invoked.[¶](#change-eb651eba6b167e1485192d8bd8f43bd6)

    参考文献：[＃3520](http://www.sqlalchemy.org/trac/ticket/3520)

### 的PostgreSQL [¶ T0\>](#change-1.0.9-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**对1.0.6中发布的反映存储选项和使用[＃3455](http://www.sqlalchemy.org/trac/ticket/3455)的新Postgresql功能进行调整，以禁用Postgresql版本的功能\<
    8.2未提供`reloptions`栏的地方；这允许Amazon
    Redshift再次运行，因为它基于PostgreSQL的8.0.x版本。修正Pete
    Hollobon提供的礼貌。[¶](#change-6bf7a5266dbb0b3f26b74d2cd173cd4d)

    参考文献：[请求github：190](https://github.com/zzzeek/sqlalchemy/pull/190)

### 预言[¶ T0\>](#change-1.0.9-oracle "Permalink to this headline")

-   **[oracle] [bug] [py3k]**Fixed support for cx\_Oracle version 5.2,
    which was tripping up SQLAlchemy’s version detection under Python 3
    and inadvertently not using the correct unicode mode for Python 3.
    这会导致绑定变量被错误地解释为NULL，并且行无声无息地返回。[¶](#change-e892caf5c83c911133f4fe685a6b90c9)

    这个改变也被**backported**改为：0.9.11

    参考文献：[＃3491](http://www.sqlalchemy.org/trac/ticket/3491)

-   **[oracle] [bug]**Fixed bug in Oracle dialect where reflection of
    tables and other symbols with names quoted to force all-lower-case
    would not be identified properly in reflection queries.
    [`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")结构现在应用于传入的符号名称，该名称在“name
    normalize”过程中检测为强制全部小写。[¶](#change-f35d719e83c23631bc4bce923fa7c168)

    参考文献：[＃3548](http://www.sqlalchemy.org/trac/ticket/3548)

### 杂项[¶ T0\>](#change-1.0.9-misc "Permalink to this headline")

-   **[feature] [ext]**Added the [`AssociationProxy.info`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.params.info "sqlalchemy.ext.associationproxy.AssociationProxy")
    parameter to the [`AssociationProxy`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")
    constructor, to suit the [`AssociationProxy.info`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.info "sqlalchemy.ext.associationproxy.AssociationProxy.info")
    accessor that was added in
    [\#2971](http://www.sqlalchemy.org/trac/ticket/2971).
    这是可能的，因为[`AssociationProxy`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")是显式构造的，与通过装饰器语法隐式构造的混合不同。[¶](#change-0e6786c673e336a819a7d69ab3e4e94f)

    参考文献：[＃3551](http://www.sqlalchemy.org/trac/ticket/3551)

-   **[bug] [examples]**Fixed two issues in the “history\_meta” example
    where history tracking could encounter empty history, and where a
    column keyed to an alternate attribute name would fail to track
    properly. 修正Alex
    Fraser的礼貌。[¶](#change-4d194a4a74cbfbf7fe6e942c90398724)

-   **[bug] [sybase]**Fixed two issues regarding Sybase reflection,
    allowing tables without primary keys to be reflected as well as
    ensured that a SQL statement involved in foreign key detection is
    pre-fetched up front to avoid driver issues upon nested queries.
    在这里修复Eugene
    Zapolsky；请注意，我们目前无法测试Sybase以在本地验证这些更改。[¶](#change-75effcc51432ea1848ea2d5f00fd9e30)

    参考文献：[＃3508](http://www.sqlalchemy.org/trac/ticket/3508)，[＃3509](http://www.sqlalchemy.org/trac/ticket/3509)

1.0.8 [¶ T0\>](#change-1.0.8 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年7月22日

### 发动机[¶ T0\>](#change-1.0.8-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed critical issue whereby the pool “checkout”
    event handler may be called against a stale connection without the
    “connect” event handler having been called, in the case where the
    pool attempted to reconnect after being invalidated and failed; the
    stale connection would remain present and would be used on a
    subsequent attempt.
    这个问题在1.0.2之后的1.0系列中有更大的影响，因为它还向事件处理程序提供了一个空白的`.info`字典；在1.0.2之前，`.info`字典仍然是前一个。[¶](#change-05bc0d20cc8959cd096fe1065ee72b6d)

    这个改变也被**backported**改为：0.9.11

    参考文献：[＃3497](http://www.sqlalchemy.org/trac/ticket/3497)

### 源码[¶ T0\>](#change-1.0.8-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**Fixed bug in SQLite dialect where reflection of
    UNIQUE constraints that included non-alphabetic characters in the
    names, like dots or spaces, would not be reflected with their
    name.[¶](#change-6134cd2764da1ab4c4d3248e1286a1ea)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3495](http://www.sqlalchemy.org/trac/ticket/3495)

### 杂项[¶ T0\>](#change-1.0.8-misc "Permalink to this headline")

-   **[misc] [bug]**修复了utils中的特定基类没有实现`__slots__`的问题，因此意味着该类的所有子类都没有，否定`__slots__`的基本原理将被使用。除了IronPython之外没有任何问题，它显然没有实现兼容cPython的`__slots__`行为。[¶](#change-24c5326bfca21e965dae7fe158cafd8e)

    参考文献：[＃3494](http://www.sqlalchemy.org/trac/ticket/3494)

1.0.7 [¶ T0\>](#change-1.0.7 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年7月20日

### ORM [¶ T0\>](#change-1.0.7-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed 1.0 regression where value objects that
    override `__eq__()` to return a
    non-boolean-capable object, such as some geoalchemy types as well as
    numpy types, were being tested for `bool()`
    during a unit of work update operation, where in 0.9 the return
    value of `__eq__()` was tested against “is True”
    to guard against this.[¶](#change-d8257a12a5e639cc3b2c05a3479592cd)

    参考文献：[＃3469](http://www.sqlalchemy.org/trac/ticket/3469)

-   **[orm] [bug]**Fixed 1.0 regression where a “deferred” attribute
    would not populate correctly if it were loaded within the “optimized
    inheritance load”, which is a special SELECT emitted in the case of
    joined table inheritance used to populate expired or unloaded
    attributes against a joined table without loading the base table.
    这与SQLA
    1.0不再猜测加载延迟列的事实有关，必须明确指示。[¶](#change-e746b68ee9723f9830729a8b48705cc0)

    参考文献：[＃3468](http://www.sqlalchemy.org/trac/ticket/3468)

-   **[orm] [bug]**Fixed 1.0 regression where the “parent entity” of a
    synonym- mapped attribute on top of an [`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")
    object would resolve to the original mapper, not the
    [`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")
    version of it, thereby causing problems for a [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    that relies on this attribute (e.g. it’s the only representative
    attribute given in the constructor) to figure out the correct FROM
    clause for the query.[¶](#change-5fde27efe6d3b70810bf2221b87e06b2)

    参考文献：[＃3466](http://www.sqlalchemy.org/trac/ticket/3466)

### orm declarative [¶](#change-1.0.7-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**修正了[`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")扩展中的错误，其中ABC基础上具有不同属性名称与列名称的列设置不正确映射到最终的基类。0.9上的失败将是无声的，而在1.0上它会引发一个ArgumentError，所以在1.0之前可能没有被注意到。[¶](#change-14091d56b0a4b381f6ca76bf3b1c27e1)

    参考文献：[＃3480](http://www.sqlalchemy.org/trac/ticket/3480)

### 发动机[¶ T0\>](#change-1.0.7-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed regression where new methods on
    [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
    used by the ORM [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object (part of the performance enhancements of
    [\#3175](http://www.sqlalchemy.org/trac/ticket/3175)) would not
    raise the “this result does not return rows” exception in the case
    where the driver (typically MySQL) fails to generate
    cursor.description correctly; an AttributeError against NoneType
    would be raised
    instead.[¶](#change-a8f444887b4e02dd0ebb799cd316449e)

    参考文献：[＃3481](http://www.sqlalchemy.org/trac/ticket/3481)

-   **[engine] [bug]**Fixed regression where [`ResultProxy.keys()`](core_connections.html#sqlalchemy.engine.ResultProxy.keys "sqlalchemy.engine.ResultProxy.keys")
    would return un-adjusted internal symbol names for “anonymous”
    labels, which are the “foo\_1” types of labels we see generated for
    SQL functions without labels and similar.
    这是作为＃918的一部分实现的性能增强的副作用。[¶](#change-cec9d3d58a6ea531cc16fc2bfe7cc705)

    参考文献：[＃3483](http://www.sqlalchemy.org/trac/ticket/3483)

### SQL [¶ T0\>](#change-1.0.7-sql "Permalink to this headline")

-   **[sql] [feature]**添加了一个[`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")方法，它与独立的[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数具有相同的用途。请求Sebastian
    Bank提供。[¶](#change-43b6d3363b92faa5bbb53e4513946b06)

    参考文献：[＃3459](http://www.sqlalchemy.org/trac/ticket/3459)，[拉取请求bitbucket：56](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/56)

-   **[sql] [bug]**Fixed bug where coersion of literal `True` or `False` constant in conjunction
    with [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
    or [`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
    would fail with an
    AttributeError.[¶](#change-bf5b877405938832cc764301281c8eaa)

    参考文献：[＃3490](http://www.sqlalchemy.org/trac/ticket/3490)

-   **[sql] [bug]**Fixed potential issue where a custom subclass of
    [`FunctionElement`](core_functions.html#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")
    or other column element that incorrectly states ‘None’ or any other
    invalid object as the `.type` attribute will
    report this exception instead of recursion
    overflow.[¶](#change-b370520554bd5df73fbe6c051d269d8d)

    参考文献：[＃3485](http://www.sqlalchemy.org/trac/ticket/3485)

-   **[sql] [bug]**Fixed bug where the modulus SQL operator wouldn’t
    work in reverse due to a missing `__rmod__`
    method.
    拉请求礼貌dan-gittik。[¶](#change-0987e97a44de7599027c6110b0dc7d3e)

    参考文献：[请求github：188](https://github.com/zzzeek/sqlalchemy/pull/188)

### 架构[¶ T0\>](#change-1.0.7-schema "Permalink to this headline")

-   **[schema] [feature]**增加了Postgresql和Oracle支持的对CREATE
    SEQUENCE的MINVALUE，MAXVALUE，NO MINVALUE，NO
    MAXVALUE和CYCLE参数的支持。请求礼貌jakeogh。[¶](#change-8f1453e149271dd9f8aef4a28b9fe43b)

    参考文献：[请求github：186](https://github.com/zzzeek/sqlalchemy/pull/186)

1.0.6 [¶ T0\>](#change-1.0.6 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年6月25日

### ORM [¶ T0\>](#change-1.0.6-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed a major regression in the 1.0 series where the
    version\_id\_counter feature would cause an object’s version counter
    to be incremented when there was no net change to the object’s row,
    but instead an object related to it via relationship (e.g. typically
    many-to-one) were associated or de-associated with it, resulting in
    an UPDATE statement that updates the object’s version counter and
    nothing else.
    在使用相对较新的“服务器端”和/或“编程/条件”版本计数器功能的情况下（例如，将version\_id\_generator设置为False），该错误可能会导致发生无需发出有效SET子句的UPDATE
    [¶ T0\>](#change-04e09fd9acaa6bca943798ba105b4b25)

    参考文献：[＃3465](http://www.sqlalchemy.org/trac/ticket/3465)

-   **[orm] [bug]**Fixed 1.0 regression where the enhanced behavior of
    single-inheritance joins of
    [\#3222](http://www.sqlalchemy.org/trac/ticket/3222) takes place
    inappropriately for a JOIN along explicit join criteria with a
    single-inheritance subclass that does not make use of any
    discriminator, resulting in an additional “AND NULL”
    clause.[¶](#change-a89cda0a0765a524834f1d22bae66a2c)

    参考文献：[＃3462](http://www.sqlalchemy.org/trac/ticket/3462)

-   **[orm] [bug]**Fixed bug in new
    [`Session.bulk_update_mappings()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")
    feature where the primary key columns used in the WHERE clause to
    locate the row would also be included in the SET clause, setting
    their value to themselves unnecessarily.
    请求帕特里克·海斯提出。[¶](#change-82e3d4362a36c994cf4680b0b62dbd96)

    参考文献：[＃3451](http://www.sqlalchemy.org/trac/ticket/3451)，[请求github：181](https://github.com/zzzeek/sqlalchemy/pull/181)

-   **[orm] [bug]**Fixed an unexpected-use regression whereby custom
    [`Comparator`](core_type_basics.html#sqlalchemy.types.JSON.Comparator "sqlalchemy.types.JSON.Comparator")
    objects that made use of the `__clause_element__()` method and returned an object that was an ORM-mapped
    [`InstrumentedAttribute`](orm_internals.html#sqlalchemy.orm.attributes.InstrumentedAttribute "sqlalchemy.orm.attributes.InstrumentedAttribute")
    and not explicitly a [`ColumnElement`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    would fail to be correctly handled when passed as an expression to
    [`Session.query()`](orm_session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query").
    0.9中的逻辑碰巧成功了，所以现在支持这个用例。[¶](#change-1b5aa56f5daacaf0d6b72f2a3660367b)

    参考文献：[＃3448](http://www.sqlalchemy.org/trac/ticket/3448)

### SQL [¶ T0\>](#change-1.0.6-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed a bug where clause adaption as applied to a
    [`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")
    object would fail to accommodate the labeled SQL expression in all
    cases, such that any SQL operation that made use of
    `Label.self_group()` would
    use the original unadapted expression. 这样做的一个影响是ORM
    [`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")结构不能完全容纳由[`column_property`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")映射的属性，这样当属性出现时，无锯齿表可能会泄漏用于某些类型的SQL比较。[¶](#change-13ad1c4b46b46eef73ee80da9b69b7c7)

    参考文献：[＃3445](http://www.sqlalchemy.org/trac/ticket/3445)

### 的PostgreSQL [¶ T0\>](#change-1.0.6-postgresql "Permalink to this headline")

-   **[postgresql]
    [feature]**使用新的关键字参数`postgresql_with`增加了对CREATE
    INDEX下存储参数的支持。还增加了对反射的支持，以支持`postgresql_with`标志以及`postgresql_using`标志，该标志现在将设置在反映的[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象上，并在[`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")的结果中出现在新的“dialect\_options”字典中。拉请求Pete
    Hollobon提供。

    也可以看看

    [Index Storage
    Parameters](dialects_postgresql.html#postgresql-index-storage)

    [¶](#change-a1da751254775f355493a4ce8c269b31)

    参考文献：[＃3455](http://www.sqlalchemy.org/trac/ticket/3455)，[请求github：179](https://github.com/zzzeek/sqlalchemy/pull/179)

-   **[postgresql]
    [feature]**增加了新的执行选项`max_row_buffer`，当使用`stream_results`选项时，psycopg2方言解释该选项，关于可能分配的行缓冲区的大小。该值也是基于发送给[`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")的整数值提供的。拉请求礼貌mcclurem。[¶](#change-dbf0b8a22c79871cbf0aa7090384697a)

    参考文献：[请求github：182](https://github.com/zzzeek/sqlalchemy/pull/182)

-   **[postgresql] [bug] [pypy]**Re-fixed this issue first released in
    1.0.5 to fix psycopg2cffi JSONB support once again, as they suddenly
    switched on unconditional decoding of JSONB types in version 2.7.1.
    版本检测现在指定2.7.1作为我们应该期望DBAPI为我们执行json编码的地方。[¶](#change-b6f3e6dc6d48ee3c97373314cbf5a1d2)

    参考文献：[＃3439](http://www.sqlalchemy.org/trac/ticket/3439)

-   **[postgresql] [bug]**修复了[`ExcludeConstraint`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint "sqlalchemy.dialects.postgresql.ExcludeConstraint")结构，以支持像[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")等其他对象现在可以使用的常用功能，可以指定列表达式作为任意的SQL表达式，如[`cast`](core_metadata.html#sqlalchemy.schema.Column.cast "sqlalchemy.schema.Column.cast")或[`text`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")。[¶](#change-be2b184e44dd8cb506c1edf0abb96861)

    参考文献：[＃3454](http://www.sqlalchemy.org/trac/ticket/3454)

### MSSQL [¶ T0\>](#change-1.0.6-mssql "Permalink to this headline")

-   **[mssql] [bug]**修正了将[`VARBINARY`](dialects_mysql.html#sqlalchemy.dialects.mysql.VARBINARY "sqlalchemy.dialects.mysql.VARBINARY")类型与INSERT的NULL
    + pyodbc结合使用的问题； pyodbc需要传递一个特殊对象才能保持NULL。As
    the [`VARBINARY`](dialects_mysql.html#sqlalchemy.dialects.mysql.VARBINARY "sqlalchemy.dialects.mysql.VARBINARY")
    type is now usually the default for [`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")
    due to [\#3039](http://www.sqlalchemy.org/trac/ticket/3039), this
    issue is partially a regression in 1.0.
    pymssql驱动程序似乎不受影响。[¶](#change-c172051273efb1de12dcb17d2c004ef7)

    参考文献：[＃3464](http://www.sqlalchemy.org/trac/ticket/3464)

### 杂项[¶ T0\>](#change-1.0.6-misc "Permalink to this headline")

-   **[bug] [documentation]**Fixed an internal “memoization” routine for
    method types such that a Python descriptor is no longer used;
    repairs inspectability of these methods including support for Sphinx
    documentation.[¶](#change-b866346f95d8f41069d193ae0433445a)

    参考文献：[＃2077](http://www.sqlalchemy.org/trac/ticket/2077)

1.0.5 [¶ T0\>](#change-1.0.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年6月7日

### ORM [¶ T0\>](#change-1.0.5-orm "Permalink to this headline")

-   **[orm] [feature]**Added new event
    [`InstanceEvents.refresh_flush()`](orm_events.html#sqlalchemy.orm.events.InstanceEvents.refresh_flush "sqlalchemy.orm.events.InstanceEvents.refresh_flush"),
    invoked when an INSERT or UPDATE level default value fetched via
    RETURNING or Python-side default is invoked within the flush
    process.
    这是为了提供一个不再作为[＃3167](http://www.sqlalchemy.org/trac/ticket/3167)的结果存在的钩子，其中在flush过程中不再调用属性和验证事件。[¶](#change-6f39fdde16df0990bd8ef09baff4f315)

    参考文献：[＃3427](http://www.sqlalchemy.org/trac/ticket/3427)

-   **[orm] [bug]**The “lightweight named tuple” used when a
    [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    returns rows failed to implement `__slots__`
    correctly such that it still had a `__dict__`.
    这已经解决了，但是在极不可能的情况下，有人正在为返回的元组赋值，这将不再有效。[¶](#change-8dff32ea855329842148a57ea75d4663)

    参考文献：[＃3420](http://www.sqlalchemy.org/trac/ticket/3420)

### 发动机[¶ T0\>](#change-1.0.5-engine "Permalink to this headline")

-   **[engine]
    [feature]**添加了新的引擎事件[`ConnectionEvents.engine_disposed()`](core_events.html#sqlalchemy.events.ConnectionEvents.engine_disposed "sqlalchemy.events.ConnectionEvents.engine_disposed")。在[`Engine.dispose()`](core_connections.html#sqlalchemy.engine.Engine.dispose "sqlalchemy.engine.Engine.dispose")方法被调用后调用。[¶](#change-8fa73745239a3c7507b7d191c9f3578e)

-   **[engine] [feature]**Adjustments to the engine plugin hook, such
    that the [`URL.get_dialect()`](core_engines.html#sqlalchemy.engine.url.URL.get_dialect "sqlalchemy.engine.url.URL.get_dialect")
    method will continue to return the ultimate [`Dialect`](core_internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
    object when a dialect plugin is used, without the need for the
    caller to be aware of the [`Dialect.get_dialect_cls()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.get_dialect_cls "sqlalchemy.engine.interfaces.Dialect.get_dialect_cls")
    method.[¶](#change-7cad7183efd71f8b53336f756c01bd4d)

    参考文献：[＃3379](http://www.sqlalchemy.org/trac/ticket/3379)

-   **[engine] [bug]**Fixed bug where known boolean values used by
    [`engine_from_config()`](core_engines.html#sqlalchemy.engine_from_config "sqlalchemy.engine_from_config")
    were not being parsed correctly; these included
    `pool_threadlocal` and the psycopg2 argument
    `use_native_unicode`.[¶](#change-5aaf85c9f6df16c1044c4ad2c76bb2c2)

    参考文献：[＃3435](http://www.sqlalchemy.org/trac/ticket/3435)

-   **[engine] [bug]**Added support for the case of the misbehaving
    DBAPI that has pep-249 exception names linked to exception classes
    of an entirely different name, preventing SQLAlchemy’s own exception
    wrapping from wrapping the error appropriately. The SQLAlchemy
    dialect in use needs to implement a new accessor
    [`DefaultDialect.dbapi_exception_translation_map`](core_internals.html#sqlalchemy.engine.default.DefaultDialect.dbapi_exception_translation_map "sqlalchemy.engine.default.DefaultDialect.dbapi_exception_translation_map")
    to support this feature; this is implemented now for the
    py-postgresql dialect.[¶](#change-cb20239967e5596291f1b8c8d0932231)

    参考文献：[＃3421](http://www.sqlalchemy.org/trac/ticket/3421)

-   **[engine] [bug]**Fixed bug involving the case when pool checkout
    event handlers are used and connection attempts are made in the
    handler itself which fail, the owning connection record would not be
    freed until the stack trace of the connect error itself were freed.
    对于仅使用单个连接的测试池的情况，这意味着该池将被完全检出，直到该堆栈跟踪被释放。这主要影响非常具体的调试场景，并且不可能在任何生产应用程序中显示出来。该修补程序在重新引发捕获的异常之前应用显式签入记录。[¶](#change-82a9e2855bd62701c659a0acd3b49568)

    参考文献：[＃3419](http://www.sqlalchemy.org/trac/ticket/3419)

### SQL [¶ T0\>](#change-1.0.5-sql "Permalink to this headline")

-   **[sql] [feature]**增加了对[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")中存在的SELECT所使用的CTE的官方支持。这种行为意外地一直运行到0.9.9，当它由于作为[＃3248](http://www.sqlalchemy.org/trac/ticket/3248)的一部分的不相关更改而不再起作用时。请注意，这是在SELECT之前的INSERT之后的WITH子句的呈现；在INSERT，UPDATE，DELETE顶层呈现的CTE的全部功能是针对以后版本的一项新功能。[¶](#change-6a7bcfa66a36b1ded7b8cf68cab71db2)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3418](http://www.sqlalchemy.org/trac/ticket/3418)

### 的PostgreSQL [¶ T0\>](#change-1.0.5-postgresql "Permalink to this headline")

-   **[postgresql] [bug] [pypy]**Repaired some typing and test issues
    related to the pypy psycopg2cffi dialect, in particular that the
    current 2.7.0 version does not have native support for the JSONB
    type.
    psycopg2功能的版本检测已被调整为psycopg2cffi的特定子版本。此外，psycopg2cffi下的全系列psycopg2功能已启用测试覆盖。[¶](#change-5e1e9b8242becfeda0232f1306c98782)

    参考文献：[＃3439](http://www.sqlalchemy.org/trac/ticket/3439)

### MSSQL [¶ T0\>](#change-1.0.5-mssql "Permalink to this headline")

-   **[mssql] [bug]**为MSSQL方言`legacy_schema_aliasing`添加了一个新的方言标志，当设置为False时，将禁用一个非常陈旧和过时的行为，将所有模式限定的表名称转换为别名，以解决SQL
    Server无法在所有情况下解析多部分标识符名称的旧且不再可定位的问题。该行为阻止更复杂的语句正常工作，包括使用提示的语句以及嵌入相关SELECT语句的CRUD语句。而不是继续修复该功能以使用更复杂的语句，最好禁用它，因为任何现代SQL服务器版本都不再需要它。对于1.0.x系列，该标志默认为True，此版本系列的当前行为不变。在1.1系列中，它将默认为False。对于1.0系列，如果未明确设置任何值，则在语句中第一次使用模式限定表时会发出警告，这表明该标志对于所有现代SQL
    Server版本都设置为False。

    也可以看看

    [Legacy Schema Mode](dialects_mssql.html#legacy-schema-rendering)

    [¶](#change-2f1eef92d4aa9867a4dd243e49dee047)

    参考文献：[＃3430](http://www.sqlalchemy.org/trac/ticket/3430)，[＃3424](http://www.sqlalchemy.org/trac/ticket/3424)

### 杂项[¶ T0\>](#change-1.0.5-misc "Permalink to this headline")

-   **[feature] [ext]**Added support for `*args` to
    be passed to the baked query initial callable, in the same way that
    `*args` are supported for the
    [`BakedQuery.add_criteria()`](orm_extensions_baked.html#sqlalchemy.ext.baked.BakedQuery.add_criteria "sqlalchemy.ext.baked.BakedQuery.add_criteria")
    and [`BakedQuery.with_criteria()`](orm_extensions_baked.html#sqlalchemy.ext.baked.BakedQuery.with_criteria "sqlalchemy.ext.baked.BakedQuery.with_criteria")
    methods.
    最初的PR礼节直接由田中直彦提供。[¶](#change-86d91bf49f3ad357db03bf080fc3f56a)

    参考：[拉请求bitbucket：54](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/54)

-   **[feature] [ext]**为[`MutableBase`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")
    `MutableBase._get_listen_keys()`添加了一个新的半公开方法。Overriding this method is needed
    in the case where a [`MutableBase`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableBase "sqlalchemy.ext.mutable.MutableBase")
    subclass needs events to propagate for attribute keys other than the
    key to which the mutable type is associated with, when intercepting
    the [`InstanceEvents.refresh()`](orm_events.html#sqlalchemy.orm.events.InstanceEvents.refresh "sqlalchemy.orm.events.InstanceEvents.refresh")
    or [`InstanceEvents.refresh_flush()`](orm_events.html#sqlalchemy.orm.events.InstanceEvents.refresh_flush "sqlalchemy.orm.events.InstanceEvents.refresh_flush")
    events. 当前的例子是使用[`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")的合成。[¶](#change-45b215195b147f63665e4cc884206096)

    参考文献：[＃3427](http://www.sqlalchemy.org/trac/ticket/3427)

-   **[bug] [ext]**Fixed regression in the
    [`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")
    extension as a result of the bugfix for
    [\#3167](http://www.sqlalchemy.org/trac/ticket/3167), where
    attribute and validation events are no longer called within the
    flush process.
    如果列级别的Python端默认负责在INSERT或UPDATE上生成新值，或者在RETURNING子句中为“预设默认值”模式提取值，则可变扩展依赖于此行为。新值在人口稠密时不会受到任何事件的影响，并且可变延伸无法建立适当的强制或历史聆听。添加了一个新事件[`InstanceEvents.refresh_flush()`](orm_events.html#sqlalchemy.orm.events.InstanceEvents.refresh_flush "sqlalchemy.orm.events.InstanceEvents.refresh_flush")，这个可变扩展现在用于这个用例。[¶](#change-f20e8c1e79cd741af716e380224f1b6b)

    参考文献：[＃3427](http://www.sqlalchemy.org/trac/ticket/3427)

1.0.4 [¶ T0\>](#change-1.0.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年5月7日

### ORM [¶ T0\>](#change-1.0.4-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed unexpected-use regression where in the odd case
    that the primaryjoin of a relationship involved comparison to an
    unhashable type such as an HSTORE, lazy loads would fail due to a
    hash-oriented check on the statement parameters, modified in 1.0 as
    a result of [\#3061](http://www.sqlalchemy.org/trac/ticket/3061) to
    use hashing and modified in
    [\#3368](http://www.sqlalchemy.org/trac/ticket/3368) to occur in
    cases more common than “load on pending”.
    现在先检查`__hash__`属性的值。[¶](#change-66020c540100c79f6234033e002fbaeb)

    参考文献：[＃3416](http://www.sqlalchemy.org/trac/ticket/3416)

-   **[orm] [bug]**Liberalized an assertion that was added as part of
    [\#3347](http://www.sqlalchemy.org/trac/ticket/3347) to protect
    against unknown conditions when splicing inner joins together within
    joined eager loads with `innerjoin=True`; if
    some of the joins use a “secondary” table, the assertion needs to
    unwrap further joins in order to
    pass.[¶](#change-ea65721f797c6d148bc5fc07146b2cb4)

    参考文献：[＃3412](http://www.sqlalchemy.org/trac/ticket/3412)，[＃3347](http://www.sqlalchemy.org/trac/ticket/3347)

-   **[orm]
    [bug]**修复/添加到测试中的更多表达式被报告为失败，新的'实体'键值添加到[`Query.column_descriptions`](orm_query.html#sqlalchemy.orm.query.Query.column_descriptions "sqlalchemy.orm.query.Query.column_descriptions")发现“from”子句再次被修改以容纳来自别名类的列，并且在这些情况下报告“别名”标志的正确值。[](#change-20137d7b96aff19d996aa7342e06ff37)

    参考文献：[＃3409](http://www.sqlalchemy.org/trac/ticket/3409)，[＃3320](http://www.sqlalchemy.org/trac/ticket/3320)

### 架构[¶ T0\>](#change-1.0.4-schema "Permalink to this headline")

-   **[schema] [bug]**Fixed bug in enhanced constraint-attachment logic
    introduced in [\#3341](http://www.sqlalchemy.org/trac/ticket/3341)
    where in the unusual case of a constraint that refers to a mixture
    of [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects and string column names at the same time, the
    auto-attach-on-column-attach logic will be skipped; for the
    constraint to be auto-attached in this case, all columns must be
    assembled on the target table up front.
    为迁移文档添加了关于原始功能以及此更改的新部分。

    也可以看看

    [Constraints referring to unattached Columns can auto-attach to the
    Table when their referred columns are
    attached](migration_10.html#change-3341)

    [¶](#change-b46fad3ee45e73a10c8ae452bcd560ff)

    参考文献：[＃3411](http://www.sqlalchemy.org/trac/ticket/3411)

### 杂项[¶ T0\>](#change-1.0.4-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug where when using extended attribute
    instrumentation system, the correct exception would not be raised
    when [`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")
    were called with an invalid input that also happened to not be weak
    referencable, such as an
    integer.[¶](#change-241707a9f4ceecb1f1f621bdd850aee5)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3408](http://www.sqlalchemy.org/trac/ticket/3408)

-   **[bug] [tests] [pypy]**修正了阻止“pypy setup.py
    test”正常工作的导入。[¶](#change-059d5e52209320ca09099434293d4ddd)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3406](http://www.sqlalchemy.org/trac/ticket/3406)

1.0.3 [¶ T0\>](#change-1.0.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年4月30日

### ORM [¶ T0\>](#change-1.0.3-orm "Permalink to this headline")

-   **[orm] [bug] [pypy]**Fixed regression from 0.9.10 prior to release
    due to [\#3349](http://www.sqlalchemy.org/trac/ticket/3349) where
    the check for query state on [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    or [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
    compared the empty tuple to itself using `is`,
    which fails on Pypy to produce `True` in this
    case; this would erronously emit a warning in 0.9 and raise an
    exception in 1.0.[¶](#change-2bd0d3b1393f8f24f850225969757976)

    参考文献：[＃3405](http://www.sqlalchemy.org/trac/ticket/3405)

-   **[orm] [bug]**从发布之前0.9.10开始修正回归，其中`entity`新添加到[`Query.column_descriptions`](orm_query.html#sqlalchemy.orm.query.Query.column_descriptions "sqlalchemy.orm.query.Query.column_descriptions")访问器将失败如果目标实体是从核心可选择的如[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`CTE`](core_selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象生成的。[¶](#change-8fc631d0b34377b720c0895b56608e6a)

    参考文献：[＃3320](http://www.sqlalchemy.org/trac/ticket/3320)，[＃3403](http://www.sqlalchemy.org/trac/ticket/3403)

-   **[orm] [bug]**Fixed regression within the flush process when an
    attribute were set to a SQL expression for an UPDATE, and the SQL
    expression when compared to the previous value of the attribute
    would produce a SQL comparison other than `==`
    or `!=`, the exception “Boolean value of this
    clause is not defined” would raise.
    该修复确保工作单元不会以这种方式解释SQL表达式。[¶](#change-734ee8c88ef7db37b98e8e9bfc172c15)

    参考文献：[＃3402](http://www.sqlalchemy.org/trac/ticket/3402)

-   **[orm] [bug]**Fixed unexpected use regression due to
    [\#2992](http://www.sqlalchemy.org/trac/ticket/2992) where textual
    elements placed into the [`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")
    clause in conjunction with joined eager loading would be added to
    the columns clause of the inner query in such a way that they were
    assumed to be table-bound column names, in the case where the joined
    eager load needs to wrap the query in a subquery to accommodate for
    a limit/offset.

    最初，这里的行为是有意的，因为诸如`query(User).order_by('name').limit(1)`的查询将按照`user.name`即使查询是通过将加载的加载修改为子查询来修改的，因为`'name'`将被解释为位于FROM子句中的符号，在这种情况下`User.name`，然后将其复制到columns子句中以确保它存在于ORDER
    BY中。但是，该功能无法预测`order_by("name")`引用本地列子句中存在的特定标签名称的情况，而不是与FROM子句中的可选择名称绑定的名称。

    Beyond that, the feature also fails for deprecated cases such as
    `order_by("name desc")`, which, while it emits a
    warning that [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    should be used here (note that the issue does not impact cases where
    [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    is used explicitly), still produces a different query than
    previously where the “name desc” expression is copied into the
    columns clause inappropriately.
    分辨率是这样的，当增加内部列子句时，特征的“加入的加载加载”方面将跳过这些所谓的“标签引用”表达式，就好像它们已经是[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构。

    [¶](#change-3edda67f000658f898770488bd7887ae)

    参考文献：[＃3392](http://www.sqlalchemy.org/trac/ticket/3392)

-   **[orm] [bug]**Fixed a regression regarding the
    [`MapperEvents.instrument_class()`](orm_events.html#sqlalchemy.orm.events.MapperEvents.instrument_class "sqlalchemy.orm.events.MapperEvents.instrument_class")
    event where its invocation was moved to be after the class manager’s
    instrumentation of the class, which is the opposite of what the
    documentation for the event explicitly states. The rationale for the
    switch was due to Declarative taking the step of setting up the full
    “instrumentation manager” for a class before it was mapped for the
    purpose of the new `@declared_attr` features
    described in [Improvements to declarative mixins, @declared\_attr
    and related features](migration_10.html#feature-3150), but the
    change was also made against the classical use of [`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
    for consistency.
    但是，SQLSoup依赖于经典映射下的任何检测之前发生的检测事件。该行为在经典和声明式映射的情况下被恢复，后者通过使用简单的记忆而不使用类管理器来实现。[¶](#change-57ac0f1083635c3e249664704f5f8681)

    参考文献：[＃3388](http://www.sqlalchemy.org/trac/ticket/3388)

-   **[orm] [bug]**Fixed issue in new
    [`QueryEvents.before_compile()`](orm_events.html#sqlalchemy.orm.events.QueryEvents.before_compile "sqlalchemy.orm.events.QueryEvents.before_compile")
    event where changes made to the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object’s collection of entities to load within the event would
    render in the SQL, but would not be reflected during the loading
    process.[¶](#change-f030dd13b152b403de3872b0d7fc16be)

    参考文献：[＃3387](http://www.sqlalchemy.org/trac/ticket/3387)

### 发动机[¶ T0\>](#change-1.0.3-engine "Permalink to this headline")

-   **[engine]
    [feature]**添加了新功能以支持具有高级功能的引擎/池插件。在检出的连接包装以及[`_ConnectionRecord`](core_pooling.html#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")级别向连接池添加了一个新的“软无效”特性。这与现代游泳池失效类似，因为连接没有被主动关闭，但仅在下次结账时才被回收；这实质上是该功能的每个连接版本。添加一个新事件`PoolEvents.soft_invalidate`以补充它。

    还添加了新标志[`ExceptionContext.invalidate_pool_on_disconnect`](core_connections.html#sqlalchemy.engine.ExceptionContext.invalidate_pool_on_disconnect "sqlalchemy.engine.ExceptionContext.invalidate_pool_on_disconnect")。允许[`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error")中的错误处理程序维护“断开连接”条件，但在事件中以特定方式处理对单个连接的无效调用。

    [¶](#change-76cdcabbfea8e248bd78644174c5517b)

    参考文献：[＃3379](http://www.sqlalchemy.org/trac/ticket/3379)

-   **[engine] [feature]**Added new event
    `DialectEvents.do_connect`,
    which allows interception / replacement of when the
    [`Dialect.connect()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.connect "sqlalchemy.engine.interfaces.Dialect.connect")
    hook is called to create a DBAPI connection.
    还添加了方言插件钩子[`Dialect.get_dialect_cls()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.get_dialect_cls "sqlalchemy.engine.interfaces.Dialect.get_dialect_cls")和[`Dialect.engine_created()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.engine_created "sqlalchemy.engine.interfaces.Dialect.engine_created")，允许外部插件使用入口点将事件添加到现有方言。[T6\>](#change-817fff0e7254e8e5723cbbeea9baa552)

    参考文献：[＃3355](http://www.sqlalchemy.org/trac/ticket/3355)

### SQL [¶ T0\>](#change-1.0.3-sql "Permalink to this headline")

-   **[sql]
    [feature]**添加了一个占位符方法[`TypeEngine.compare_against_backend()`](core_type_api.html#sqlalchemy.types.TypeEngine.compare_against_backend "sqlalchemy.types.TypeEngine.compare_against_backend")，该方法现在由Alembic
    migrations从0.7.6开始使用。用户定义的类型可以实现此方法，以帮助比较数据库中反映的类型与类型。[¶](#change-6bec4ab076ee2fa285da1e7c5209da3b)

-   **[sql] [bug]**Fixed bug where the truncation of long labels in SQL
    could produce a label that overlapped another label that is not
    truncated; this because the length threshhold for truncation was
    greater than the portion of the label that remains after truncation.
    现在这两个数值已经相同； label\_length -
    6。这里的效果是，较短的列标签将被“截断”，之前它们不会被截断。[¶](#change-c5574f4752ab5cec2695a9af0c8f84b2)

    参考文献：[＃3396](http://www.sqlalchemy.org/trac/ticket/3396)

-   **[sql] [bug]**Fixed regression due to
    [\#3282](http://www.sqlalchemy.org/trac/ticket/3282) where the
    `tables` collection passed as a keyword argument
    to the [`DDLEvents.before_create()`](core_events.html#sqlalchemy.events.DDLEvents.before_create "sqlalchemy.events.DDLEvents.before_create"),
    [`DDLEvents.after_create()`](core_events.html#sqlalchemy.events.DDLEvents.after_create "sqlalchemy.events.DDLEvents.after_create"),
    [`DDLEvents.before_drop()`](core_events.html#sqlalchemy.events.DDLEvents.before_drop "sqlalchemy.events.DDLEvents.before_drop"),
    and [`DDLEvents.after_drop()`](core_events.html#sqlalchemy.events.DDLEvents.after_drop "sqlalchemy.events.DDLEvents.after_drop")
    events would no longer be a list of tables, but instead a list of
    tuples which contained a second entry with foreign keys to be added
    or dropped. 由于`tables`集合虽然被记录为不一定稳定，但依赖于此，这种变化被认为是一种回归。此外，在某些情况下，“收集”将会是一个迭代器，如果过早迭代，会导致操作失败。该集合现在是所有情况下的表对象列表，并且现在添加了用于此集合格式的测试覆盖。[¶](#change-556a9afc8de654667f5ab9b749086dff)

    参考文献：[＃3391](http://www.sqlalchemy.org/trac/ticket/3391)

### 杂项[¶ T0\>](#change-1.0.3-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug in association proxy where an any()/has()
    on an relationship-\>scalar non-object attribute comparison would
    fail, e.g.
    `filter(Parent.some_collection_to_attribute.any(Child.attr == 'foo'))`[¶](#change-deb397d6ec2ff20a860f9f9d05ea50bf)

    参考文献：[＃3397](http://www.sqlalchemy.org/trac/ticket/3397)

1.0.2 [¶ T0\>](#change-1.0.2 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年4月24日

### orm declarative [¶](#change-1.0.2-orm-declarative "Permalink to this headline")

-   **[bug] [orm]
    [declarative]**修复了关于声明式`__declare_first__`和`__declare_last__`访问器的意外使用回归，声明性基类的超类。[¶](#change-fb796750b45072da56370dc233b06603)

    参考文献：[＃3383](http://www.sqlalchemy.org/trac/ticket/3383)

### SQL [¶ T0\>](#change-1.0.2-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed a regression that was incorrectly fixed in
    1.0.0b4 (hence becoming two regressions); reports that SELECT
    statements would GROUP BY a label name and fail was misconstrued
    that certain backends such as SQL Server should not be emitting
    ORDER BY or GROUP BY on a simple label name at all; when in fact, we
    had forgotten that 0.9 was already emitting ORDER BY on a simple
    label name for all backends, as described in [Label constructs can
    now render as their name alone in an ORDER
    BY](migration_09.html#migration-1068), even though 1.0 includes a
    rewrite of this logic as part of
    [\#2992](http://www.sqlalchemy.org/trac/ticket/2992).
    就针对简单标签发布GROUP
    BY而言，即使Postgresql也会引发错误，即使要标记的标签应该是显而易见的，所以显然GROUP
    BY不应该以这种方式自动呈现。

    在1.0.2中，SQL
    Server，Firebird和其他人在传递也存在于columns子句中的[`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")结构时，会再次在简单标签名称上发出ORDER
    BY。此外，仅当传递[`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")结构时，后端才会针对简单标签名称发出GROUP
    BY。

    [¶](#change-728ce9fb29e31d643429b92816fa188c)

    参考文献：[＃3338](http://www.sqlalchemy.org/trac/ticket/3338)，[＃3385](http://www.sqlalchemy.org/trac/ticket/3385)

1.0.1 [¶ T0\>](#change-1.0.1 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年4月23日

### ORM [¶ T0\>](#change-1.0.1-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed issue where a query of the form
    `query(B).filter(B.a != A(id=7))` would render
    the `NEVER_SET` symbol, when given a transient
    object.
    对于持久对象，它总是使用持久数据库值而不是当前设置的值。假设autoflush已打开，通常这对于持久性值来说并不明显，因为在任何情况下都会首先刷新任何挂起的更改。然而，这与用于非否定比较的逻辑不一致，`query（B）.filter（Ba == A = 7））`，它可以使用当前值，并且还可以与瞬态对象进行比较。现在比较使用当前值而不是数据库持久值。

    与本版本中由[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)引起的回归修复的其他`NEVER_SET`问题不同，这个特定问题的存在时间至少早于0.8且可能更早，但它被发现是因为修复了相关的`NEVER_SET`问题。

    也可以看看

    [A “negated contains or equals” relationship comparison will use the
    current value of attributes, not the database
    value](migration_10.html#bug-3374)

    [¶](#change-c3046cef1c62baa499a720ee4f37dc00)

    参考文献：[＃3374](http://www.sqlalchemy.org/trac/ticket/3374)

-   **[orm] [bug]**Fixed unexpected use regression cause by
    [\#3061](http://www.sqlalchemy.org/trac/ticket/3061) where the
    NEVER\_SET symbol could leak into relationship-oriented queries,
    including `filter()` and
    `with_parent()` queries.
    所有情况下都会返回`None`符号，但是，在任何情况下，这些查询中的许多都从未得到正确支持，并且在不使用IS运算符的情况下将其与NULL进行比较。因此，警告还会添加到当前不提供`IS NULL`的关系查询的子集中。

    也可以看看

    [Warnings emitted when comparing objects with None values to
    relationships](migration_10.html#bug-3371)进行比较时发出警告

    [¶](#change-367bfbbb798543fcd661f5a7f129f5d6)

    参考文献：[＃3371](http://www.sqlalchemy.org/trac/ticket/3371)

-   **[orm] [bug]**Fixed a regression caused by
    [\#3061](http://www.sqlalchemy.org/trac/ticket/3061) where the
    NEVER\_SET symbol could leak into a lazyload query, subsequent to
    the flush of a pending object.
    这通常会发生在不使用简单的“获取”策略的多对一关系中。好消息是修复程序的效率提高了0.9，因为我们现在可以在检测参数中存在的NEVER\_SET符号时完全跳过SELECT语句；在[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)之前，我们无法辨别这里是否设置了None。[¶](#change-16c7878b69c66a7b45e984cf7ddea43b)

    参考文献：[＃3368](http://www.sqlalchemy.org/trac/ticket/3368)

### 发动机[¶ T0\>](#change-1.0.1-engine "Permalink to this headline")

-   **[engine] [bug]**Added the string value `"none"` to those accepted by the [`Pool.reset_on_return`](core_pooling.html#sqlalchemy.pool.Pool.params.reset_on_return "sqlalchemy.pool.Pool")
    parameter as a synonym for `None`, so that
    string values can be used for all settings, allowing utilities like
    [`engine_from_config()`](core_engines.html#sqlalchemy.engine_from_config "sqlalchemy.engine_from_config")
    to be usable without
    issue.[¶](#change-64a5444055f49209fa585e76ac99afdf)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3375](http://www.sqlalchemy.org/trac/ticket/3375)

### SQL [¶ T0\>](#change-1.0.1-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed issue where a straight SELECT EXISTS query
    would fail to assign the proper result type of Boolean to the result
    mapping, and instead would leak column types from within the query
    into the result map.
    此问题也存在于0.9及更早版本中，但在这些版本中影响较小。在1.0中，由于[＃918](http://www.sqlalchemy.org/trac/ticket/918)，这成为一种回归，因为我们现在依赖于结果映射非常准确，否则我们可以将结果类型的处理器分配到错误的列。在所有版本中，这个问题也有一个效果，即一个简单的EXISTS不会应用布尔类型处理程序，导致后端的简单1/0值不使用本地布尔值而不是True
    /
    False。修复包括EXISTS列参数将像其他列表达式一样被匿名标记；对于纯布尔表达式（如`not_(True())`）实现了类似的修复。[¶](#change-c38b9512685589dea5443f525d104643)

    参考文献：[＃3372](http://www.sqlalchemy.org/trac/ticket/3372)

### 源码[¶ T0\>](#change-1.0.1-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**Fixed a regression due to
    [\#3282](http://www.sqlalchemy.org/trac/ticket/3282), where due to
    the fact that we attempt to assume the availability of ALTER when
    creating/dropping schemas, in the case of SQLite we simply said to
    not worry about foreign keys at all, since ALTER is not available,
    when creating and dropping tables.
    这意味着在SQLite的情况下基本上跳过了表的排序，对于绝大多数的SQLite用例来说，这不是问题。

    然而，那些在SQLite上执行DROP并且带有数据并且参照完整性被打开的用户将会遇到错误，因为依赖关系排序*在强制约束DROP的情况下很重要，当那些表有数据（只要没有数据被引用，SQLite仍然很乐意让你创建外键到不存在的表，并删除引用已有约束的现有表的表）。*

    In order to maintain the new feature of
    [\#3282](http://www.sqlalchemy.org/trac/ticket/3282) while still
    allowing a SQLite DROP operation to maintain ordering, we now do the
    sort with full FKs taken under consideration, and if we encounter an
    unresolvable cycle, only *then* do we forego attempting to sort the
    tables; we instead emit a warning and go with the unsorted list. If
    an environment needs both ordered DROPs *and* has foreign key
    cycles, then the warning notes they will need to restore the
    `use_alter` flag to their [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    and [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    objects so that just those objects will be omitted from the
    dependency sort.

    也可以看看

    [The use\_alter flag on ForeignKeyConstraint is (usually) no longer
    needed](migration_10.html#feature-3282) - 包含有关SQLite的更新注释。

    [¶](#change-3bf8faa066b4a78884ef6bf04b5ebc2b)

    参考文献：[＃3378](http://www.sqlalchemy.org/trac/ticket/3378)

### 火鸟[¶ T0\>](#change-1.0.1-firebird "Permalink to this headline")

-   **[firebird]
    [bug]**修正了由于[＃3034](http://www.sqlalchemy.org/trac/ticket/3034)造成的回归，其中限制/偏移子句未被Firebird方言正确解释。请求礼貌effem-git。[¶](#change-dba16e624daeccaf8cb85b4704fadcf9)

    参考文献：[＃3380](http://www.sqlalchemy.org/trac/ticket/3380)，[请求github：168](https://github.com/zzzeek/sqlalchemy/pull/168)

-   **[firebird] [bug]**Fixed support for “literal\_binds” mode when
    using limit/offset with Firebird, so that the values are again
    rendered inline when this is selected.
    与[＃3034](http://www.sqlalchemy.org/trac/ticket/3034)。[¶](#change-454ec28afe6a7226f901467602c5e493)相关

    参考文献：[＃3381](http://www.sqlalchemy.org/trac/ticket/3381)

1.0.0 [¶ T0\>](#change-1.0.0 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015年4月16日

### ORM [¶ T0\>](#change-1.0.0-orm "Permalink to this headline")

-   **[orm] [feature]**添加了新的参数[`Query.update.update_args`](orm_query.html#sqlalchemy.orm.query.Query.update.params.update_args "sqlalchemy.orm.query.Query.update")，它允许将诸如`mysql_limit`之类的kw参数传递给底层的[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构。请求礼貌Amir
    Sadoughi。[¶](#change-d6a9012ea02989676f613aa443e77cfc)

    参考文献：[请求github：164](https://github.com/zzzeek/sqlalchemy/pull/164)

-   **[orm] [bug]**多次处理[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")到同一个目标时发现不一致；它仅在关系连接的情况下隐含地进行了重复数据删除，并且由于[＃3233](http://www.sqlalchemy.org/trac/ticket/3233)，1.0中对同一个表的两次连接的行为与0.9不同，因为它不再是错误的别名。为了帮助记录这种变化，移植说明中关于[＃3233](http://www.sqlalchemy.org/trac/ticket/3233)的措辞已经被推广，并且在针对相同的[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")调用时添加了警告目标关系不止一次。[¶](#change-f7fa40f7d0ccb7891bd8c505b5445a0e)

    参考文献：[＃3367](http://www.sqlalchemy.org/trac/ticket/3367)

-   **[orm] [bug]**Made a small improvement to the heuristics of
    relationship when determining remote side with semi-self-referential
    (e.g. two joined inh subclasses referring to each other), non-simple
    join conditions such that the parententity is taken into account and
    can reduce the need for using the `remote()`
    annotation; this can restore some cases that might have worked
    without the annotation prior to 0.9.4 via
    [\#2948](http://www.sqlalchemy.org/trac/ticket/2948).[¶](#change-f24cfb05e58edcba962d50d47c745bf1)

    参考文献：[＃3364](http://www.sqlalchemy.org/trac/ticket/3364)

### SQL [¶ T0\>](#change-1.0.0-sql "Permalink to this headline")

-   **[sql] [feature]**The topological sorting used to sort
    [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    objects and available via the [`MetaData.sorted_tables`](core_metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")
    collection will now produce a **deterministic** ordering; that is,
    the same ordering each time given a set of tables with particular
    names and dependencies.
    这有助于比较DDL脚本和其他用例。这些表被发送到按名称排序的拓扑排序，并且拓扑排序本身将以有序方式处理输入数据。拉请求塞巴斯蒂安银行礼貌。

    也可以看看

    [MetaData.sorted\_tables accessor is
    “deterministic”](migration_10.html#feature-3084)

    [¶](#change-aab332eedafc8e090f42b89ac7a67e6c)

    References: [\#3084](http://www.sqlalchemy.org/trac/ticket/3084),
    [pull request
    bitbucket:47](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/47)

-   **[sql] [bug]**Fixed issue where a [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    object that used a naming convention would not properly work with
    pickle. 如果使用不带钩的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象来构建附加表格，则跳过该属性会导致不一致和失败。[¶](#change-41cee2035e8cd5037366cfcb88fe424c)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3362](http://www.sqlalchemy.org/trac/ticket/3362)

### 的PostgreSQL [¶ T0\>](#change-1.0.0-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**修复了长期存在的bug，其中psycopg2方言使用的[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型与非ascii值和`native_enum=False`将无法正确解码返回结果。这源于PG [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")类型曾经是没有“非本地”选项的独立类型。[¶](#change-863813ed9984daf0fde8f4a84fcaf02a)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3354](http://www.sqlalchemy.org/trac/ticket/3354)

### MSSQL [¶ T0\>](#change-1.0.0-mssql "Permalink to this headline")

-   **[mssql] [bug]**Fixed a regression where the “last inserted id”
    mechanics would fail to store the correct value for MSSQL on an
    INSERT where the primary key value was present in the insert params
    before execution, as well as in the case where an INSERT from SELECT
    would state the target columns as column objects, instead of string
    keys.[¶](#change-af05e4dd4a311a3d1bfb497d1d748f61)

    参考文献：[＃3360](http://www.sqlalchemy.org/trac/ticket/3360)

-   **[mssql] [bug]**使用pymssql中现在存在的`Binary`构造函数，而不是修补其中的一个。请求拉米罗莫拉莱斯提供。[¶](#change-e184664c46b2999f9724d1e3c1efc30a)

    参考文献：[请求github：166](https://github.com/zzzeek/sqlalchemy/pull/166)

### 杂项[¶ T0\>](#change-1.0.0-misc "Permalink to this headline")

-   **[bug]
    [tests]**修复测试运行时使用的路径；对于sqla\_nose.py和py.test，“./lib”前缀再次插入到sys.path的头部，但前提是sys.flags.no\_user\_site未设置；这使得它的行为就像Python在默认情况下在当前路径中放置“。”一样。对于tox，我们现在设置PYTHONNOUSERSITE标志。[¶](#change-767cbbf7a16d3556b45934d148b75590)

    参考文献：[＃3356](http://www.sqlalchemy.org/trac/ticket/3356)

1.0.0b5 [¶ T0\>](#change-1.0.0b5 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2015年4月3日

### ORM [¶ T0\>](#change-1.0.0b5-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug where the state tracking within multiple,
    nested [`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")
    operations would fail to propagate the “dirty” flag for an object
    that had been updated within the inner savepoint, such that if the
    enclosing savepoint were rolled back, the object would not be part
    of the state that was expired and therefore reverted to its database
    state.[¶](#change-4dc519d63b37a4f457ef287d947f10a8)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3352](http://www.sqlalchemy.org/trac/ticket/3352)

-   **[orm] [bug]**[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    doesn’t support joins, subselects, or special FROM clauses when
    using the [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    or [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
    methods; instead of silently ignoring these fields if methods like
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    or [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    has been called, an error is raised.
    在0.9.10中，这只会发出警告。[¶](#change-13d3f0158003a7617db3b63ddcf497d1)

    参考文献：[＃3349](http://www.sqlalchemy.org/trac/ticket/3349)

-   **[orm] [bug]**Added a list() call around a weak dictionary used
    within the commit phase of the session, which without it could cause
    a “dictionary changed size during iter” error if garbage collection
    interacted within the process.
    变更由＃3139引入。[¶](#change-f3cfafae76ecf50510e353cf7dddeca5)

-   **[orm] [bug]**Fixed a bug related to “nested” inner join eager
    loading, which exists in 0.9 as well but is more of a regression in
    1.0 due to [\#3008](http://www.sqlalchemy.org/trac/ticket/3008)
    which turns on “nested” by default, such that a joined eager load
    that travels across sibling paths from a common ancestor using
    innerjoin=True will correctly splice each “innerjoin” sibling into
    the appropriate part of the join, when a series of inner/outer joins
    are mixed together.[¶](#change-d2fc894ca158a0ac1ac0bd16c128a42c)

    参考文献：[＃3347](http://www.sqlalchemy.org/trac/ticket/3347)

### SQL [¶ T0\>](#change-1.0.0b5-sql "Permalink to this headline")

-   **[sql] [bug]**The warning emitted by the unicode type for a
    non-unicode type has been liberalized to warn for values that aren’t
    even string values, such as integers; previously, the updated
    warning system of 1.0 made use of string formatting operations which
    would raise an internal TypeError.
    尽管理想情况下这些情况应该完全提升，但像SQLite和MySQL这样的后端会接受它们，并且可能会被遗留代码使用，更不用说如果目标后端关闭unicode转换，它们将始终通过。[T0\>](#change-985d8b07c9b5d0ce36d2ac39ed07d053)

    参考文献：[＃3346](http://www.sqlalchemy.org/trac/ticket/3346)

### 的PostgreSQL [¶ T0\>](#change-1.0.0b5-postgresql "Permalink to this headline")

-   修正了由于[＃3184](http://www.sqlalchemy.org/trac/ticket/3184)引起的更新PG索引反射会导致索引操作在Postgresql
    8.4及更早版本上失败的错误。**[postgresql]
    [bug]**使用旧版Postgresql时，现在禁用了这些增强功能。[¶](#change-ea6acf6124c25077db337001ff4dd2cb)

    参考文献：[＃3343](http://www.sqlalchemy.org/trac/ticket/3343)

1.0.0b4 [¶ T0\>](#change-1.0.0b4 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2015年3月29日

### SQL [¶ T0\>](#change-1.0.0b4-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug in new “label resolution” feature of
    [\#2992](http://www.sqlalchemy.org/trac/ticket/2992) where a label
    that was anonymous, then labeled again with a name, would fail to be
    locatable via a textual label.
    如果在查询中为映射的[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")赋予显式标签，则这种情况自然会发生。[¶](#change-aa46baa3af25851e9a3b23c4cf081182)

    参考文献：[＃3340](http://www.sqlalchemy.org/trac/ticket/3340)

-   **[sql] [bug]**Fixed bug in new “label resolution” feature of
    [\#2992](http://www.sqlalchemy.org/trac/ticket/2992) where the
    string label placed in the order\_by() or group\_by() of a statement
    would place higher priority on the name as found inside the FROM
    clause instead of a more locally available name inside the columns
    clause.[¶](#change-842ea77e51f1517d3e1d9d918929b5a6)

    参考文献：[＃3335](http://www.sqlalchemy.org/trac/ticket/3335)

### 架构[¶ T0\>](#change-1.0.0b4-schema "Permalink to this headline")

-   **[schema] [feature]**The “auto-attach” feature of constraints such
    as [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
    and [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    has been further enhanced such that when the constraint is
    associated with non-table-bound [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects, the constraint will set up event listeners with the columns
    themselves such that the constraint auto attaches at the same time
    the columns are associated with the table.
    这特别有助于一些边缘案例的声明，但也是一般用途。

    也可以看看

    [Constraints referring to unattached Columns can auto-attach to the
    Table when their referred columns are
    attached](migration_10.html#change-3341)

    [¶](#change-6995af73c8bb8ff0a94424837ca173bf)

    参考文献：[＃3341](http://www.sqlalchemy.org/trac/ticket/3341)

### MySQL的[¶ T0\>](#change-1.0.0b4-mysql "Permalink to this headline")

-   **[mysql] [bug]
    [pymysql]**修正了使用unicode参数使用“executemany”操作时对PyMySQL的Unicode支持。SQLAlchemy现在将语句以及绑定参数作为unicode对象传递，因为PyMySQL通常在内部使用字符串插值来生成最终语句，而在executemany的情况下，仅在最后语句中执行“编码”步骤。[¶
    T0\>](#change-266a2c933324f8199da8adcbe84e6365)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3337](http://www.sqlalchemy.org/trac/ticket/3337)

### MSSQL [¶ T0\>](#change-1.0.0b4-mssql "Permalink to this headline")

-   **[mssql] [bug] [sybase] [firebird] [oracle]**Turned off the “simple
    order by” flag on the MSSQL, Oracle dialects; this is the flag that
    per [\#2992](http://www.sqlalchemy.org/trac/ticket/2992) causes an
    order by or group by an expression that’s also in the columns clause
    to be copied by label, even if referenced as the expression object.
    MSSQL的行为现在是默认情况下复制整个表达式的旧行为，因为MSSQL对这些行为尤其在GROUP
    BY表达式中很挑剔。对于Firebird和Sybase方言，该标志在防御方面也被关闭。

    注意

    这个解决方案是不正确的，请参阅1.0.2版对这个决议的返工。

    [¶](#change-dcda11a97947dd7e426511bc4af55102)

    参考文献：[＃3338](http://www.sqlalchemy.org/trac/ticket/3338)

1.0.0b3 [¶ T0\>](#change-1.0.0b3 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2015年3月20日

### MySQL的[¶ T0\>](#change-1.0.0b3-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**修复了被无意中注释掉的问题＃2771的提交。[¶](#change-618be62c1ace7b1a9c3d132a7b410c7c)

    参考文献：[＃2771](http://www.sqlalchemy.org/trac/ticket/2771)

1.0.0b2 [¶ T0\>](#change-1.0.0b2 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2015年3月20日

### ORM [¶ T0\>](#change-1.0.0b2-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed unexpected use regression from pullreq
    github:137 where Py2K unicode literals (e.g. `u""`) would not be accepted by the
    [`relationship.cascade`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")
    option. 请求礼貌Julien
    Castets。[¶](#change-4c044b2c0a16bca90a751e90c5071191)

    参考文献：[＃3327](http://www.sqlalchemy.org/trac/ticket/3327)，[请求github：160](https://github.com/zzzeek/sqlalchemy/pull/160)

### orm declarative [¶](#change-1.0.0b2-orm-declarative "Permalink to this headline")

-   **[orm] [declarative]
    [change]**松散了一些添加到`@declared_attr`对象的限制，以防止在声明过程之外调用它们；这与＃3150的增强有关，它允许`@declared_attr`返回一个根据当前类配置缓存的值。异常引发已被删除，并且行为发生了变化，因此在声明过程之外，由`@declared_attr`装饰的函数每次都会像常规`@property`一样调用，没有使用任何缓存，因为在这个阶段没有任何缓存。[¶](#change-a790c86836f12d50614920b63573998a)

    参考文献：[＃3331](http://www.sqlalchemy.org/trac/ticket/3331)

### 发动机[¶ T0\>](#change-1.0.0b2-engine "Permalink to this headline")

-   **[engine] [bug]**The “auto close” for [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
    is now a “soft” close.
    也就是说，在使用提取方法排除所有行之后，DBAPI游标将像以前一样被释放，并且可以安全地丢弃该对象，但可能会继续调用获取方法，以便返回结果对象（无为fetchone，fetchmany和fetchall空列表）。只有明确调用[`ResultProxy.close()`](core_connections.html#sqlalchemy.engine.ResultProxy.close "sqlalchemy.engine.ResultProxy.close")时，这些方法才会引发“result
    is closed”错误。

    也可以看看

    [ResultProxy “auto close” is now a “soft”
    close](migration_10.html#change-3330)

    [¶](#change-95589804661b80fa4b64b69f3b32b165)

    参考文献：[＃3329](http://www.sqlalchemy.org/trac/ticket/3329)，[＃3330](http://www.sqlalchemy.org/trac/ticket/3330)

### MySQL的[¶ T0\>](#change-1.0.0b2-mysql "Permalink to this headline")

-   **[mysql] [bug] [py3k]**修正了Py3K上没有正确使用`ord()`函数的[`mysql.BIT`](dialects_mysql.html#sqlalchemy.dialects.mysql.BIT "sqlalchemy.dialects.mysql.BIT")类型。请求礼貌David
    Marin。[¶](#change-d5a00477ae396554230dc380ca9cff6c)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3333](http://www.sqlalchemy.org/trac/ticket/3333)，[请求github：158](https://github.com/zzzeek/sqlalchemy/pull/158)

-   **[mysql] [bug]**Fixes to fully support using the
    `'utf8mb4'` MySQL-specific charset with MySQL
    dialects, in particular MySQL-Python and PyMySQL.
    另外，报告诸如'koi8u'或'eucjpms'等更多不寻常字符集的MySQL数据库也能正常工作。拉格请求托马斯格兰杰提供[¶](#change-d371fa3b0a2b4808035e7e50eac2a491)

    参考文献：[＃2771](http://www.sqlalchemy.org/trac/ticket/2771)，[拉取请求bitbucket：49](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/49)

1.0.0b1 [¶ T0\>](#change-1.0.0b1 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2015年3月13日

版本1.0.0b1是1.0系列的第一个版本。这里描述的许多变化也存在于0.9和0.8系列中。对于特定于1.0的更改，强调兼容性问题，请参阅[*What’s
New in SQLAlchemy 1.0?*](migration_10.html)。

### 一般[¶ T0\>](#change-1.0.0b1-general "Permalink to this headline")

-   **[general] [feature]**通过对许多内部对象使用`__slots__`，结构内存使用得到了改进。此优化尤其适用于具有大量表和列的大型应用程序的基本内存大小，并大大减少各种大容量对象（包括事件监听内部事件，比较对象以及ORM属性和加载器策略的某些部分）的内存大小系统。

    也可以看看

    [Significant Improvements in Structural Memory
    Use](migration_10.html#feature-slots)

    [¶](#change-2f14e668cc239752997ac9b41f224ec6)

-   **[general] [bug]**The `__module__` attribute is
    now set for all those SQL and ORM functions that are derived as
    “public factory” symbols, which should assist with documentation
    tools being able to report on the target
    module.[¶](#change-be87e00250d24db1082e7f44ee07d44e)

    参考文献：[＃3218](http://www.sqlalchemy.org/trac/ticket/3218)

### ORM [¶ T0\>](#change-1.0.0b1-orm "Permalink to this headline")

-   **[orm] [feature]**向由[`Query.column_descriptions`](orm_query.html#sqlalchemy.orm.query.Query.column_descriptions "sqlalchemy.orm.query.Query.column_descriptions")返回的字典添加了一个新条目`"entity"`。这是指由表达式引用的主要ORM映射类或别名类。与`"type"`的现有条目相比，即使从列表达式中提取，它也将始终是映射实体，如果给定表达式是纯粹核心表达式，它将始终为None。另见[＃3403](http://www.sqlalchemy.org/trac/ticket/3403)，它修复了此功能中的回归，该功能在0.9.10中未发布，但在1.0版本中发布。[¶](#change-616a1ffdd35a65e93fd791c48eee3e2a)

    这个改变也被**backported**改为：0.9.10

    参考文献：[＃3320](http://www.sqlalchemy.org/trac/ticket/3320)

-   **[orm]
    [feature]**添加了一个新参数[`Session.connection.execution_options`](orm_session_api.html#sqlalchemy.orm.session.Session.connection.params.execution_options "sqlalchemy.orm.session.Session.connection")，它可用于在[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上设置执行选项在交易开始之前首先检查出来。这用于在事务启动之前设置连接上的隔离级别等选项。

    也可以看看

    [Setting Transaction Isolation
    Levels](orm_session_transaction.html#session-transaction-isolation)
    - 新的文档部分详细介绍了使用会话设置事务隔离的最佳实践。

    [¶](#change-3acdcfd8019bdf552158d7f199e9d4a7)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3296](http://www.sqlalchemy.org/trac/ticket/3296)

-   **[orm] [feature]**Added new method [`Session.invalidate()`](orm_session_api.html#sqlalchemy.orm.session.Session.invalidate "sqlalchemy.orm.session.Session.invalidate"),
    functions similarly to [`Session.close()`](orm_session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close"),
    except also calls [`Connection.invalidate()`](core_connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")
    on all connections, guaranteeing that they will not be returned to
    the connection pool.
    这在例如情况下是有用的在进一步使用连接不安全时处理gevent超时，即使是回滚。[¶](#change-9a67336d5098be7fa6d5d1712e13abf7)

    这个改变也被**backported**改为：0.9.9

-   **[orm] [feature]**The “primaryjoin” model has been stretched a bit
    further to allow a join condition that is strictly from a single
    column to itself, translated through some kind of SQL function or
    expression.
    这是一种实验，但概念的第一个证明是“物化路径”连接条件，其中路径字符串使用“like”与自身进行比较。[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")运算符也被添加到在primaryjoin条件中使用的有效运算符列表中。[¶](#change-bc2f57a8dd0b3e0854cf5c5fe90779ae)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3029](http://www.sqlalchemy.org/trac/ticket/3029)

-   **[orm]
    [feature]**添加了新的实用程序函数[`make_transient_to_detached()`](orm_session_api.html#sqlalchemy.orm.session.make_transient_to_detached "sqlalchemy.orm.session.make_transient_to_detached")，可用于制造表现如同从会话加载，然后分离的对象。不存在的属性被标记为过期，并且该对象可以被添加到会话中，它将像一个持久的行为一样。[¶](#change-ad1b3230bf3a35c539d3800bd7eaa906)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3017](http://www.sqlalchemy.org/trac/ticket/3017)

-   **[orm] [feature]**新增了一个新的事件套件[`QueryEvents`](orm_events.html#sqlalchemy.orm.events.QueryEvents "sqlalchemy.orm.events.QueryEvents")。The
    [`QueryEvents.before_compile()`](orm_events.html#sqlalchemy.orm.events.QueryEvents.before_compile "sqlalchemy.orm.events.QueryEvents.before_compile")
    event allows the creation of functions which may place additional
    modifications to [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    objects before the construction of the SELECT statement.
    希望通过新的检查系统的出现使这一事件变得更加有用，这将允许以自动方式对[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象进行详细的修改。

    也可以看看

    [`QueryEvents`](orm_events.html#sqlalchemy.orm.events.QueryEvents "sqlalchemy.orm.events.QueryEvents")

    [¶](#change-224c208adb8b17c4d5402a6d062f720b)

    参考文献：[＃3317](http://www.sqlalchemy.org/trac/ticket/3317)

-   **[orm]
    [feature]**在使用联接的预加载时发生的子查询包装与一个一对多查询一起使用，该查询还具有LIMIT，OFFSET或DISTINCT在一个一对一关系，即[`relationship.uselist`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.uselist "sqlalchemy.orm.relationship")设置为False的一对多关系。这将在这些情况下产生更高效的查询。

    也可以看看

    [Subqueries no longer applied to uselist=False joined eager
    loads](migration_10.html#change-3249)

    [¶](#change-4ffb78c7f1d4662a75b3c14e8865497b)

    参考文献：[＃3249](http://www.sqlalchemy.org/trac/ticket/3249)

-   **[orm]
    [feature]**对映射状态内部进行了重新设计，以允许特定于对象“过期”的callcounts减少50％，如[`Session.commit()`](orm_session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")和[`Session.expire_all()`](orm_session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")，以及在对象状态被垃圾收集时发生的“清除”步骤。[¶](#change-ba2e12d237fd1b8dd5b88441ad712dd5)

    参考文献：[＃3307](http://www.sqlalchemy.org/trac/ticket/3307)

-   **[orm]
    [feature]**将相同的多态标识分配给同一层次结构中的两个不同映射器时，会发出警告。这通常是用户错误，并且意味着在加载时不能正确区分这两种不同的映射类型。请求Sebastian
    Bank提供。[¶](#change-06fec19f82dae0028e9f912dc0a37eaf)

    参考文献：[＃3262](http://www.sqlalchemy.org/trac/ticket/3262)，[拉取请求bitbucket：38](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/38)

-   **[orm] [feature]**已经创建了一系列新的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")方法，它们将工作单元直接提供给工作单元以发出INSERT和UPDATE语句。如果使用正确，这个面向专家的系统可以允许ORM映射用于生成批量插入和更新语句，批量插入到executemany组中，从而允许语句以与直接使用Core相媲美的速度进行。

    也可以看看

    [Bulk Operations](orm_persistence_techniques.html#bulk-operations)

    [¶](#change-e101a9e2bfc2d51486dfbb485d2a7d97)

    参考文献：[＃3100](http://www.sqlalchemy.org/trac/ticket/3100)

-   **[orm] [feature]**添加了与调用[`Query.outerjoin()`](orm_query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")同义的参数[`Query.join.isouter`](orm_query.html#sqlalchemy.orm.query.Query.join.params.isouter "sqlalchemy.orm.query.Query.join")；与Core
    [`FromClause.join()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")相比，此标志提供更一致的接口。请求Jonathan
    Vanasco提供。[¶](#change-2144e6087f689d4bdb021d19044edc77)

    参考文献：[＃3217](http://www.sqlalchemy.org/trac/ticket/3217)

-   **[orm]
    [feature]**添加了新的事件处理程序[`AttributeEvents.init_collection()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.init_collection "sqlalchemy.orm.events.AttributeEvents.init_collection")和[`AttributeEvents.dispose_collection()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.dispose_collection "sqlalchemy.orm.events.AttributeEvents.dispose_collection")与实例相关联以及何时被替换。这些处理程序取代[`collection.linker()`](orm_collections.html#sqlalchemy.orm.collections.collection.linker "sqlalchemy.orm.collections.collection.linker")注释。旧挂钩仍然通过事件适配器支持。[¶](#change-0e828b26dd65117f3478db52f1f0e546)

-   **[orm] [feature]**The [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    will raise an exception when [`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")
    is used with mappings or options where either subquery eager
    loading, or joined eager loading with collections, would take place.
    这些加载策略目前与yield\_per不兼容，所以通过提高这个错误，该方法更安全。可以使用`lazyload('*')`选项或[`Query.enable_eagerloads()`](orm_query.html#sqlalchemy.orm.query.Query.enable_eagerloads "sqlalchemy.orm.query.Query.enable_eagerloads")来禁用预加载。

    也可以看看

    [Joined/Subquery eager loading explicitly disallowed with
    yield\_per](migration_10.html#migration-yield-per-eager-loading)加入/子查询加载加载

    [¶](#change-b616294de6debb7de491e4493f524c6b)

-   **[orm] [feature]**A new implementation for [`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")
    used by the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object offers dramatic speed improvements when fetching large
    numbers of column-oriented rows.

    也可以看看

    [New KeyedTuple implementation dramatically
    faster](migration_10.html#feature-3176)

    [¶](#change-8965eb2566f786710793ef1a6281b74d)

    参考文献：[＃3176](http://www.sqlalchemy.org/trac/ticket/3176)

-   **[orm] [feature]**The behavior of [`joinedload.innerjoin`](orm_loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")
    as well as [`relationship.innerjoin`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")
    is now to use “nested” inner joins, that is, right-nested, as the
    default behavior when an inner join joined eager load is chained to
    an outer join eager load.

    也可以看看

    [Right inner join nesting now the default for joinedload with
    innerjoin=True](migration_10.html#migration-3008)

    [¶](#change-b3169a2d87d3780499be2e7f2821729b)

    参考文献：[＃3008](http://www.sqlalchemy.org/trac/ticket/3008)

-   **[orm] [feature]**UPDATE statements can now be batched within an
    ORM flush into more performant executemany() call, similarly to how
    INSERT statements can be batched; this will be invoked within flush
    to the degree that subsequent UPDATE statements for the same mapping
    and table involve the identical columns within the VALUES clause,
    that no SET-level SQL expressions are embedded, and that the
    versioning requirements for the mapping are compatible with the
    backend dialect’s ability to return a correct rowcount for an
    executemany operation.[¶](#change-c2a7ce636a44564eadf2a903567d4605)

-   **[orm] [feature]**The `info` parameter has been
    added to the constructor for [`SynonymProperty`](orm_internals.html#sqlalchemy.orm.descriptor_props.SynonymProperty "sqlalchemy.orm.descriptor_props.SynonymProperty")
    and [`ComparableProperty`](orm_internals.html#sqlalchemy.orm.properties.ComparableProperty "sqlalchemy.orm.properties.ComparableProperty").[¶](#change-f11e5a48b55d152ba27006a0c7a50f69)

    参考文献：[＃2963](http://www.sqlalchemy.org/trac/ticket/2963)

-   **[orm] [feature]**The `InspectionAttr.info`collection is now moved down to
    [`InspectionAttr`](orm_internals.html#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr"),
    where in addition to being available on all [`MapperProperty`](orm_internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
    objects, it is also now available on hybrid properties, association
    proxies, when accessed via [`Mapper.all_orm_descriptors`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors").[¶](#change-dc2eac33191482c15be6aab0b79ac2ee)

    参考文献：[＃2971](http://www.sqlalchemy.org/trac/ticket/2971)

-   **[orm] [changed]**The `proc()` callable passed
    to the `create_row_processor()` method of custom
    [`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")
    classes now accepts only a single “row” argument.

    也可以看看

    [API Change for new Bundle feature when custom row loaders are
    used](migration_10.html#bundle-api-change)

    [¶](#change-95474fb930794e4ecf37bfbc1331505e)

-   **[orm] [changed]**Deprecated event hooks removed:
    `populate_instance`, `create_instance`, `translate_row`,
    `append_result`

    也可以看看

    [Deprecated ORM Event Hooks
    Removed](migration_10.html#migration-deprecated-orm-events)

    [¶](#change-560ef9d31daf212e20d665eb2eec3570)

-   **[orm] [bug]**Fixed bugs in ORM object comparisons where comparison
    of many-to-one `!= None` would fail if the
    source were an aliased class, or if the query needed to apply
    special aliasing to the expression due to aliased joins or
    polymorphic querying; also fixed bug in the case where comparing a
    many-to-one to an object state would fail if the query needed to
    apply special aliasing due to aliased joins or polymorphic
    querying.[¶](#change-6f298ded8801c07d3257fd19d0ec9d86)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3310](http://www.sqlalchemy.org/trac/ticket/3310)

-   修正了在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的`after_rollback()`处理程序错误地将状态添加到内部断言的情况下会失败的问题。**[orm]
    [bug]** [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处理程序中，以及警告和移除此状态的任务（由[＃2389](http://www.sqlalchemy.org/trac/ticket/2389)建立）尝试继续。[¶](#change-04a3bda01df00148ba3b83fbf9bbe294)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3309](http://www.sqlalchemy.org/trac/ticket/3309)

-   **[orm] [bug]**Fixed bug where TypeError raised when
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    called with unknown kw arguments would raise its own TypeError due
    to broken formatting. 请求Malthe
    Borch提出请求。[¶](#change-376e2904e02255469c634ee04c021623)

    这个改变也被**backported**改为：0.9.9

    参考文献：[请求github：147](https://github.com/zzzeek/sqlalchemy/pull/147)

-   **[orm] [bug]**Fixed bug in lazy loading SQL construction whereby a
    complex primaryjoin that referred to the same “local” column
    multiple times in the “column that points to itself” style of
    self-referential join would not be substituted in all cases.
    这里确定替代的逻辑已被重新设计为更加开放。[¶](#change-2986f6b48420a5a13faf87400ceb4a0f)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3300](http://www.sqlalchemy.org/trac/ticket/3300)

-   **[orm] [bug]**“通配符”加载器选项，特别是由[`orm.load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")选项设置的选项，以覆盖未明确提及的所有属性，现在考虑给定实体的超类，如果该实体使用继承映射进行映射，那么超类中的属性名也从加载中省略。此外，多态判别器列无条件地包含在列表中，就像主键列一样，所以即使设置了load\_only()，子类型的多态加载也能正常运行。[¶
    t0 \>](#change-70b361455e80b62dcaf98a303f010d7b)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3287](http://www.sqlalchemy.org/trac/ticket/3287)

-   **[orm] [bug] [pypy]**Fixed bug where if an exception were thrown at
    the start of a [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    before it fetched results, particularly when row processors can’t be
    formed, the cursor would stay open with results pending and not
    actually be closed.
    对于像Pypy这样的解释器来说，这通常只是一个问题，在这种解释器中，光标没有立即被GC化，并且在某些情况下会导致事务/锁的打开时间超过所需的时间。[¶](#change-16483765b5b469f2aeb8abd7abfc6035)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3285](http://www.sqlalchemy.org/trac/ticket/3285)

-   **[orm] [bug]**Fixed a leak which would occur in the unsupported and
    highly non-recommended use case of replacing a relationship on a
    fixed mapped class many times, referring to an arbitrarily growing
    number of target mappers.
    当旧的关系被替换时发出警告，但是如果映射已经用于查询，旧的关系仍然会在一些注册表中被引用。[¶](#change-2e12bc9781aa2298691dc48360ef2c6e)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3251](http://www.sqlalchemy.org/trac/ticket/3251)

-   **[orm] [bug] [sqlite]**Fixed bug regarding expression mutations
    which could express itself as a “Could not locate column” error when
    using [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    to select from multiple, anonymous column entities when querying
    against SQLite, as a side effect of the “join rewriting” feature
    used by the SQLite
    dialect.[¶](#change-57a644cbb8d635a77fa5615f0d5e72a1)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3241](http://www.sqlalchemy.org/trac/ticket/3241)

-   **[orm] [bug]**Fixed bug where the ON clause for
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join"),
    and [`Query.outerjoin()`](orm_query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")
    to a single-inheritance subclass using `of_type()` would not render the “single table criteria” in the ON
    clause if the `from_joinpoint=True` flag were
    set.[¶](#change-ece99f4e425237d28766bafcb908f9c8)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3232](http://www.sqlalchemy.org/trac/ticket/3232)

-   **[orm] [bug] [engine]**Fixed bug that affected generally the same
    classes of event as that of
    [\#3199](http://www.sqlalchemy.org/trac/ticket/3199), when the
    `named=True` parameter would be used.
    一些事件将无法注册，而其他事件不会正确地调用事件参数，通常是在事件被“包装”以便以其他方式进行适应的情况下。“命名”机制已重新排列，不会干扰内部包装函数期望的参数签名。[¶](#change-5f4ad543840a3c34916641cc4f26dfd7)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3197](http://www.sqlalchemy.org/trac/ticket/3197)

-   **[orm] [bug]**Fixed bug that affected many classes of event,
    particularly ORM events but also engine events, where the usual
    logic of “de duplicating” a redundant call to
    [`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")
    with the same arguments would fail, for those events where the
    listener function is wrapped.
    断言将在registry.py中发生。这一说法现在已经被纳入重复数据删除检查中，并带来更简单的方法来检查重复数据删除的额外好处。[¶](#change-13967322d0db184e4ffb1c9b2b8391a2)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3199](http://www.sqlalchemy.org/trac/ticket/3199)

-   **[orm]
    [bug]**固定警告，当复杂的自引用primaryjoin包含函数时会发出警告，同时指定remote\_side；警告会建议设置“远程端”。如果remote\_side不存在，它现在只会发射。[¶](#change-75a312cfcc6e096469f40858cff9a1c6)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3194](http://www.sqlalchemy.org/trac/ticket/3194)

-   **[orm] [bug] [eagerloading]**Fixed a regression caused by
    [\#2976](http://www.sqlalchemy.org/trac/ticket/2976) released in
    0.9.4 where the “outer join” propagation along a chain of joined
    eager loads would incorrectly convert an “inner join” along a
    sibling join path into an outer join as well, when only descendant
    paths should be receiving the “outer join” propagation;
    additionally, fixed related issue where “nested” join propagation
    would take place inappropriately between two sibling join
    paths.[¶](#change-011e2d22662edc5f79a8c6b840409cd7)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3131](http://www.sqlalchemy.org/trac/ticket/3131)

-   **[orm] [bug]**Fixed a regression from 0.9.0 due to
    [\#2736](http://www.sqlalchemy.org/trac/ticket/2736) where the
    [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    method no longer set up the “from entity” of the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object correctly, so that subsequent [`Query.filter_by()`](orm_query.html#sqlalchemy.orm.query.Query.filter_by "sqlalchemy.orm.query.Query.filter_by")
    or [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    calls would fail to check the appropriate “from” entity when
    searching for attributes by string
    name.[¶](#change-c8c83da8d054bbd7ec8173da1ea832f7)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃2736](http://www.sqlalchemy.org/trac/ticket/2736)，[＃3083](http://www.sqlalchemy.org/trac/ticket/3083)

-   **[orm] [bug]**Fixed bug where items that were persisted, deleted,
    or had a primary key change within a savepoint block would not
    participate in being restored to their former state (not in session,
    in session, previous PK) after the outer transaction were rolled
    back.[¶](#change-09e0b3775e3126481bf907cdd3c8a22c)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3108](http://www.sqlalchemy.org/trac/ticket/3108)

-   **[orm] [bug]**Fixed bug in subquery eager loading in conjunction
    with [`with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic"),
    the targeting of entities and columns in the subquery load has been
    made more accurate with respect to this type of entity and
    others.[¶](#change-09c6751d1497c418a77af762659e38ef)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3106](http://www.sqlalchemy.org/trac/ticket/3106)

-   **[orm] [bug]**Additional checks have been added for the case where
    an inheriting mapper is implicitly combining one of its column-based
    attributes with that of the parent, where those columns normally
    don’t necessarily share the same value.
    这是通过[＃1892](http://www.sqlalchemy.org/trac/ticket/1892)添加的现有支票的扩展。然而，这个新的检查仅发出警告，而不是例外，以允许可能依赖现有行为的应用程序。

    也可以看看

    [I’m getting a warning or error about “Implicitly combining column X
    under attribute Y”](faq_ormconfiguration.html#faq-combining-columns)

    [¶](#change-57fece0f852794967517d0a22cbe10e7)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3042](http://www.sqlalchemy.org/trac/ticket/3042)

-   **[orm] [bug]**Modified the behavior of [`orm.load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")
    such that primary key columns are always added to the list of
    columns to be “undeferred”; otherwise, the ORM can’t load the row’s
    identity. 显然，可以推迟映射的主键，并且ORM将失败，这并没有改变。But
    as load\_only is essentially saying “defer all but X”, it’s more
    critical that PK cols not be part of this
    deferral.[¶](#change-33b5e0cd5517f6c4fc5131ce5e6124cc)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3080](http://www.sqlalchemy.org/trac/ticket/3080)

-   **[orm] [bug]**Fixed a few edge cases which arise in the so-called
    “row switch” scenario, where an INSERT/DELETE can be turned into an
    UPDATE.
    在这种情况下，将多对一关系设置为无，或者在某些情况下将标量属性设置为无，可能不会将其检测为值的净更改，因此UPDATE不会重置上一行中的内容。这是由于一些尚未解决的方式属性历史的工作方式隐含地假设None不是真正的“改变”以前未设置的属性。另见[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)。

    注意

    This change has been **REVERTED** in 0.9.6.
    完整的修补程序将在SQLAlchemy 1.0版中。

    [¶](#change-c9f980a739ab915284d71db0b46f1cff)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)

-   **[orm]
    [bug]**与[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)相关，已对工作单元进行了调整，以使相关的多对一对象的加载稍微更积极在要删除的自引用对象的图形的情况下；如果未设置passive\_deletes，则相关对象的负载将帮助确定正确的删除顺序。[](#change-50f44a6d5929b19a0805c7112c0d27ad)

    这个改变也被**backported**改为：0.9.5

-   **[orm] [bug]**Fixed bug in SQLite join rewriting where anonymized
    column names due to repeats would not correctly be rewritten in
    subqueries.
    这会影响任何类型的子查询+连接的SELECT查询。[¶](#change-16b352ed9b306320c6e8315ed89d5a2b)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3057](http://www.sqlalchemy.org/trac/ticket/3057)

-   **[orm] [bug] [sql]**Fixes to the newly enhanced boolean coercion in
    [\#2804](http://www.sqlalchemy.org/trac/ticket/2804) where the new
    rules for “where” and “having” woudn’t take effect for the
    “whereclause” and “having” kw arguments of the [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    construct, which is also what [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    uses so wasn’t working in the ORM
    either.[¶](#change-aecdd4c095256f1086a037c2ef111fdc)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3013](http://www.sqlalchemy.org/trac/ticket/3013)

-   **[orm] [bug]**Fixed bug in subquery eager loading where a long
    chain of eager loads across a polymorphic-subclass boundary in
    conjunction with polymorphic loading would fail to locate the
    subclass-link in the chain, erroring out with a missing property
    name on an [`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass").[¶](#change-15fc39532a23156ee7c64b1f7fc460b1)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3055](http://www.sqlalchemy.org/trac/ticket/3055)

-   **[orm] [bug]**Fixed ORM bug where the [`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")
    function would mask AttributeErrors or KeyErrors that should raise
    during mapper configuration due to user errors.
    对属性/键错误的捕获更具体，不包括配置步骤。[¶](#change-a0449e3beb0c1ac9e913ca55add64fd5)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3047](http://www.sqlalchemy.org/trac/ticket/3047)

-   **[orm] [bug]**Fixed bug where the session attachment error “object
    is already attached to session X” would fail to prevent the object
    from also being attached to the new session, in the case that
    execution continued after the error raise
    occurred.[¶](#change-7025ea4b0c6347ad5a8b4ec049fb17e7)

    参考文献：[＃3301](http://www.sqlalchemy.org/trac/ticket/3301)

-   **[orm] [bug]**The primary [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
    of a [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    is now passed to the [`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")
    method when calling upon [`Query.count()`](orm_query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count"),
    [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update"),
    [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete"),
    as well as queries against mapped columns, [`column_property`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")
    objects, and SQL functions and expressions derived from mapped
    columns. 这允许依赖于定制的[`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方案或“绑定”元数据的会话在所有相关情况下都能够工作。

    也可以看看

    [Session.get\_bind() will receive the Mapper in all relevant Query
    cases](migration_10.html#bug-3227)

    [¶](#change-536752c99cbc5490b91573baaeb7d5f4)

    References: [\#3242](http://www.sqlalchemy.org/trac/ticket/3242),
    [\#3227](http://www.sqlalchemy.org/trac/ticket/3227),
    [\#1326](http://www.sqlalchemy.org/trac/ticket/1326)

-   **[orm] [bug]**The [`PropComparator.of_type()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")
    modifier has been improved in conjunction with loader directives
    such as [`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")
    and [`contains_eager()`](orm_loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")
    such that if two [`PropComparator.of_type()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")
    modifiers of the same base type/path are encountered, they will be
    joined together into a single “polymorphic” entity, rather than
    replacing the entity of type A with the one of type B. E.g. a
    joinedload of `A.b.of_type(BSub1)->BSub1.c`
    combined with joinedload of `A.b.of_type(BSub2)->BSub2.c` will create a single joinedload of
    `A.b.of_type((BSub1, BSub2)) -> BSub1.c, BSub2.c`, without the need for the `with_polymorphic` to be explicit in the query.

    也可以看看

    [Eager Loading of Specific or Polymorphic
    Subtypes](orm_inheritance.html#eagerloading-polymorphic-subtypes) -
    包含说明新格式的更新示例。

    [¶](#change-ea41da3074acd0052766bd3df13f9711)

    参考文献：[＃3256](http://www.sqlalchemy.org/trac/ticket/3256)

-   **[orm] [bug]**Repaired support of the `copy.deepcopy()` call when used by the [`orm.util.CascadeOptions`](orm_internals.html#sqlalchemy.orm.util.CascadeOptions "sqlalchemy.orm.util.CascadeOptions")
    argument, which occurs if `copy.deepcopy()` is
    being used with [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    (not an officially supported use case).
    拉请求由duesenfranz提供。[¶](#change-48bcac0d4325cf6d45c78e2b87c7bc18)

    参考文献：[请求github：137](https://github.com/zzzeek/sqlalchemy/pull/137)

-   **[orm] [bug]**Fixed bug where [`Session.expunge()`](orm_session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")
    would not fully detach the given object if the object had been
    subject to a delete operation that was flushed, but not committed.
    这也会影响相关的操作，如[`make_transient()`](orm_session_api.html#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")。

    也可以看看

    [session.expunge() will fully detach an object that’s been
    deleted](migration_10.html#bug-3139)

    [¶](#change-59caee694a457e7e0024d37366ccc4af)

    参考文献：[＃3139](http://www.sqlalchemy.org/trac/ticket/3139)

-   **[orm] [bug]**A warning is emitted in the case of multiple
    relationships that ultimately will populate a foreign key column in
    conflict with another, where the relationships are attempting to
    copy values from different source columns.
    这发生在具有重叠列的组合外键映射到每个引用不同引用列的关系的情况下。新的文档部分将说明该示例以及如何通过在每个关系的基础上专门指定“外来”列来解决该问题。

    也可以看看

    [Overlapping Foreign
    Keys](orm_join_conditions.html#relationship-overlapping-foreignkeys)

    [¶](#change-242697352354ba812f1570b0e04e2b68)

    参考文献：[＃3230](http://www.sqlalchemy.org/trac/ticket/3230)

-   **[orm] [bug]**The [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    method will now convert string key names in the given dictionary of
    values into mapped attribute names against the mapped class being
    updated.
    以前，字符串名称直接被采用并传递给核心更新语句，没有任何方法可以根据映射实体进行解析。支持同义词和混合属性作为[`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")的主题属性。

    也可以看看

    [query.update() now resolves string names into mapped attribute
    names](migration_10.html#bug-3228)

    [¶](#change-04f95fecb0cc472b5f37e7ad801ce005)

    参考文献：[＃3228](http://www.sqlalchemy.org/trac/ticket/3228)

-   **[orm] [bug]**Improvements to the mechanism used by
    [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    to locate “binds” (e.g. engines to use), such engines can be
    associated with mixin classes, concrete subclasses, as well as a
    wider variety of table metadata such as joined inheritance tables.

    也可以看看

    [Session.get\_bind() handles a wider variety of inheritance
    scenarios](migration_10.html#bug-3035)

    [¶](#change-1503884aa0f4847e8b48adc09e62f9fe)

    参考文献：[＃3035](http://www.sqlalchemy.org/trac/ticket/3035)

-   **[orm] [bug]**Fixed bug in single table inheritance where a chain
    of joins that included the same single inh entity more than once
    (normally this should raise an error) could, in some cases depending
    on what was being joined “from”, implicitly alias the second case of
    the single inh entity, producing a query that “worked”.
    但是，由于这种隐式别名并不适用于单表继承的情况，因此它并没有真正“充分发挥作用”，而且非常具有误导性，因为它并不总是显示出来。

    也可以看看

    [Changes and fixes in handling of duplicate join
    targets](migration_10.html#bug-3233)

    [¶](#change-d320a6f7b1d2612830586f2eff0be2ed)

    参考文献：[＃3233](http://www.sqlalchemy.org/trac/ticket/3233)

-   **[orm] [bug]**The ON clause rendered when using
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join"),
    [`Query.outerjoin()`](orm_query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin"),
    or the standalone [`orm.join()`](orm_query.html#sqlalchemy.orm.join "sqlalchemy.orm.join")
    / [`orm.outerjoin()`](orm_query.html#sqlalchemy.orm.outerjoin "sqlalchemy.orm.outerjoin")
    functions to a single-inheritance subclass will now include the
    “single table criteria” in the ON clause even if the ON clause is
    otherwise hand-rolled; it is now added to the criteria using AND,
    the same way as if joining to a single-table target using
    relationship or similar.

    这是介于特征和缺陷之间的一种。

    也可以看看

    [single-table-inheritance criteria added to all ON clauses
    unconditionally](migration_10.html#migration-3222)

    [¶](#change-99003d65e049410824e42ce9dab0c51b)

    参考文献：[＃3222](http://www.sqlalchemy.org/trac/ticket/3222)

-   **[orm] [bug]**A major rework to the behavior of expression labels,
    most specifically when used with ColumnProperty constructs with
    custom SQL expressions and in conjunction with the “order by labels”
    logic first introduced in 0.9.
    修复包括即使实体受到混淆，一个`order_by(Entity.some_col_prop)`现在可以使用“按标签排序”规则，可以通过继承呈现或通过使用`aliased()`结构；使用别名（例如，`查询（Entity.some_prop， tt> entity_alias.some_prop）`）多次渲染同一列属性将标记每次出现实体具有不同的标签，并且另外“按标签排序”规则适用于两者（例如，`order_by（Entity.some_prop， entity_alias.some_prop）  t7 >）。`其他问题可能会阻止“按标签排序”逻辑在0.9下工作，最值得注意的是标签的状态可能发生变化，使得“按标签排序”将停止工作，具体取决于调用方式，已得到修复。

    也可以看看

    [ColumnProperty constructs work a lot better with aliases,
    order\_by](migration_10.html#bug-3188)

    [¶](#change-4dc82827da24b55f91128a02f9b3f695)

    参考文献：[＃3148](http://www.sqlalchemy.org/trac/ticket/3148)，[＃3188](http://www.sqlalchemy.org/trac/ticket/3188)

-   **[orm] [bug]**更改了使用[`Query.from_self()`](orm_query.html#sqlalchemy.orm.query.Query.from_self "sqlalchemy.orm.query.Query.from_self")时应用“单一继承标准”的方法或其普通用户[`Query.count()`](orm_query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")现在，在内部子查询中而不是外部子查询中指定了将行限制为具有某种类型的标准的条件，以便即使“列”子句中“类型”列不可用，我们也可以在“内部“查询。

    也可以看看

    [Change to single-table-inheritance criteria when using
    from\_self(),
    count()](migration_10.html#migration-3177)时更改为单表继承条件

    [¶](#change-e1840eaa8736367b7f48e48d04d2d7d2)

    参考文献：[＃3177](http://www.sqlalchemy.org/trac/ticket/3177)

-   **[orm]
    [bug]**对延迟加载的机制做了一些小调整，这样在对象指向自身的非常罕见的情况下，干涉joinload()的可能性就会降低；在这种情况下，对象在加载其属性时会引用自身，这会导致加载器之间出现混淆。“对象指向自身”的用例并不完全支持，但修复还会消除一些开销，所以现在是测试的一部分。[¶](#change-c17ae9c4ebca0e74f469b58a3f8ac5a1)

    参考文献：[＃3145](http://www.sqlalchemy.org/trac/ticket/3145)

-   **[orm]
    [bug]**“resurrect”ORM事件已被删除。这个事件钩子没有用处，因为在0.8中删除了旧的“可变属性”系统。[¶](#change-ee661e992971bab23524715b4fd7af05)

    参考文献：[＃3171](http://www.sqlalchemy.org/trac/ticket/3171)

-   **[orm] [bug]**Fixed bug where attribute “set” events or columns
    with `@validates` would have events triggered
    within the flush process, when those columns were the targets of a
    “fetch and populate” operation, such as an autoincremented primary
    key, a Python side default, or a server-side default “eagerly”
    fetched via RETURNING.[¶](#change-b5c339b9efafb2a17766bcb8e791ab2b)

    参考文献：[＃3167](http://www.sqlalchemy.org/trac/ticket/3167)

-   **[orm] [bug] [py3k]**The [`IdentityMap`](orm_internals.html#sqlalchemy.orm.identity.IdentityMap "sqlalchemy.orm.identity.IdentityMap")
    exposed from [`Session.identity_map`{](orm_session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")
    now returns lists for `items()` and
    `values()` in Py3K.
    早期移植到Py3K这里有这些返回的迭代器，当它们在技术上应该是“可迭代的视图”时。现在，列表是可以的。[¶](#change-21c5bfbd3c59afd9373dca8d8606a34e)

-   **[orm] [bug]**The “evaluator” for query.update()/delete() won’t
    work with multi-table updates, and needs to be set to
    synchronize\_session=False or synchronize\_session=’fetch’; this now
    raises an exception, with a message to change the synchronize
    setting.
    这是从0.9.7发出的警告升级而来的。[¶](#change-9f773e193791199cf150187e1e900de3)

    参考文献：[＃3117](http://www.sqlalchemy.org/trac/ticket/3117)

-   **[orm]
    [change]**即使列中的某些列以某种方式存在于结果集中，标记为deferred的映射属性现在仍保持“延迟”状态。这是一种性能增强，因为当获得结果集时，ORM加载不再花费时间搜索每个延迟列。但是，对于依赖于此的应用程序，现在应该使用明确的[`undefer()`](orm_loading_columns.html#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")或类似选项。[¶](#change-0b4a0dfd1c62dd4c3d1b1194d31a4ca3)

-   **[orm]
    [enhancement]**调整属性的机制，涉及何时将值通过第一次访问隐式初始化为None；这种一直导致人口属性的行为不再这样做；将返回None值，但底层属性不会收到设置事件。这与集合的工作方式一致，并允许属性机制的行为更加一致；特别是，如果值实际设置为None，则获取不带值的属性不会压缩应继续执行的事件。

    也可以看看

    [Changes to attribute events and other operations regarding
    attributes that have no pre-existing
    value](migration_10.html#migration-3061)的属性的操作

    根据编译时选项将绑定参数内联呈现为字符串。此功能的工作是由Dobes
    Vandermeer提供的。

    > 也可以看看
    >
    > [Select/Query LIMIT / OFFSET may be specified as an arbitrary SQL
    > expression](migration_10.html#feature-3034).

    [¶](#change-adcdeaea46191497621f88dc5dc2e323)

    参考文献：[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)

### orm declarative [¶](#change-1.0.0b1-orm-declarative "Permalink to this headline")

-   **[feature] [orm] [declarative]** [`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")构造具有与声明式结合的新改进的行为和特征。装饰后的函数现在可以在调用时访问本地mixin上存在的最终列副本，并且每次映射的类也会被调用一次，返回的结果将被记忆。还添加了新的修饰符[`declared_attr.cascading`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr.cascading "sqlalchemy.ext.declarative.declared_attr.cascading")。

    也可以看看

    [Improvements to declarative mixins, @declared\_attr and related
    features](migration_10.html#feature-3150)

    [¶](#change-4705f0764e48b2f5eb3aab8ef41313f3)

    参考文献：[＃3150](http://www.sqlalchemy.org/trac/ticket/3150)

-   **[bug] [declarative] [orm]**Fixed “‘NoneType’ object has no
    attribute ‘concrete’” error when using [`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    in conjunction with a subclass that declares
    `__abstract__`.[¶](#change-35f8b8e11566fd75025e1d45a0b5bb5f)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3185](http://www.sqlalchemy.org/trac/ticket/3185)

-   **[bug] [orm] [declarative]**Fixed bug where using an
    `__abstract__` mixin in the middle of a
    declarative inheritance hierarchy would prevent attributes and
    configuration being correctly propagated from the base class to the
    inheriting class.[¶](#change-c38f0b260fc330da3a825c0062499246)

    参考文献：[＃3240](http://www.sqlalchemy.org/trac/ticket/3240)，[＃3219](http://www.sqlalchemy.org/trac/ticket/3219)

-   **[bug] [orm] [declarative]**A relationship set up with
    [`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")
    on a [`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    base class will now be configured on the abstract base mapping
    automatically, in addition to being set up on descendant concrete
    classes as usual.

    也可以看看

    [Improvements to declarative mixins, @declared\_attr and related
    features](migration_10.html#feature-3150)

    [¶](#change-51f59e6c6a8a87ad61d8e37d86ecd144)

    参考文献：[＃2670](http://www.sqlalchemy.org/trac/ticket/2670)

### 发动机[¶ T0\>](#change-1.0.0b1-engine "Permalink to this headline")

-   **[engine] [feature]**增加了用于查看事务隔离级别的新用户空间访问器；
    [`Connection.get_isolation_level()`](core_connections.html#sqlalchemy.engine.Connection.get_isolation_level "sqlalchemy.engine.Connection.get_isolation_level")，[`Connection.default_isolation_level`](core_connections.html#sqlalchemy.engine.Connection.default_isolation_level "sqlalchemy.engine.Connection.default_isolation_level")。[¶](#change-c5f37fab842327e43b9fdbd6c63bb80c)

    这个改变也被**backported**改为：0.9.9

-   **[engine] [feature]**Added new event
    [`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error"),
    a more fully featured and comprehensive replacement for
    [`ConnectionEvents.dbapi_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.dbapi_error "sqlalchemy.events.ConnectionEvents.dbapi_error").[¶](#change-ce4694f9946ff09e6367694b4c41ac6f)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3076](http://www.sqlalchemy.org/trac/ticket/3076)

-   **[engine]
    [feature]**可以发出一种新的警告样式，它将“过滤”出现N次参数化字符串。这允许可以引用参数的参数化警告被传递固定次数，直到允许Python警告过滤器压制它们，并且防止内存在Python的警告注册表中无限增长。

    也可以看看

    [Session.get\_bind() handles a wider variety of inheritance
    scenarios](migration_10.html#feature-3178)

    [¶](#change-bec11487773ec538543ddd3dac610199)

    参考文献：[＃3178](http://www.sqlalchemy.org/trac/ticket/3178)

-   **[engine] [bug]**Fixed bug in [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    and pool where the [`Connection.invalidate()`](core_connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")
    method, or an invalidation due to a database disconnect, would fail
    if the `isolation_level` parameter had been used
    with [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options");
    the “finalizer” that resets the isolation level would be called on
    the no longer opened
    connection.[¶](#change-1cbe7376cc9712fd0fa0633c798b04b5)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3302](http://www.sqlalchemy.org/trac/ticket/3302)

-   **[engine] [bug]**A warning is emitted if the
    `isolation_level` parameter is used with
    [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")
    when a [`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")
    is in play; DBAPIs and/or SQLAlchemy dialects such as psycopg2,
    MySQLdb may implicitly rollback or commit the transaction, or not
    change the setting til next transaction, so this is never
    safe.[¶](#change-35e91e4cf37ed9f5f5338f624ccfac94)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3296](http://www.sqlalchemy.org/trac/ticket/3296)

-   **[engine] [bug]**The execution options passed to an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    either via [`create_engine.execution_options`](core_engines.html#sqlalchemy.create_engine.params.execution_options "sqlalchemy.create_engine")
    or [`Engine.update_execution_options()`](core_connections.html#sqlalchemy.engine.Engine.update_execution_options "sqlalchemy.engine.Engine.update_execution_options")
    are not passed to the special [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    used to initialize the dialect within the “first connect” event;
    dialects will usually perform their own queries in this phase, and
    none of the current available options should be applied here.
    特别是，“自动提交”选项会导致尝试在此初始连接中自动提交，由于[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的非标准状态，该选项将因AttributeError失败。[¶](#change-d3615ec97e4cb3d677b23aae37c5f9a1)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3200](http://www.sqlalchemy.org/trac/ticket/3200)

-   **[engine]
    [bug]**用于确定受INSERT或UPDATE影响的列的字符串键现在在对“编译缓存”缓存键作出贡献时被排序。这些键以前没有确定性地排序，这意味着相同的语句可以在相同的键上多次缓存，从内存和性能两个方面来说都是这样。[¶](#change-17ea7031c46ba798ed90caf31a4ec215)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3165](http://www.sqlalchemy.org/trac/ticket/3165)

-   **[engine] [bug]**Fixed bug which would occur if a DBAPI exception
    occurs when the engine first connects and does its initial checks,
    and the exception is not a disconnect exception, yet the cursor
    raises an error when we try to close it.
    在这种情况下，当我们试图通过连接池记录游标关闭异常并且失败时，真正的异常将被废除，因为我们试图以在这种特定情况下不合适的方式访问池的记录器。[T0\>](#change-61f8e288cabf0d93da08c5bf8b0da4f5)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3063](http://www.sqlalchemy.org/trac/ticket/3063)

-   **[engine] [bug]**Fixed some “double invalidate” situations were
    detected where a connection invalidation could occur within an
    already critical section like a connection.close(); ultimately,
    these conditions are caused by the change in
    [\#2907](http://www.sqlalchemy.org/trac/ticket/2907), in that the
    “reset on return” feature calls out to the Connection/Transaction in
    order to handle it, where “disconnect detection” might be caught.
    然而，[＃2985](http://www.sqlalchemy.org/trac/ticket/2985)中最近发生的变化可能会导致这种情况出现，因为“连接无效”操作的速度更快，因为问题在0.9.4上的可重复性高于0.9.3。

    现在在任何可能出现失效的部分添加检查，以暂停对失效的连接进一步禁止的操作。这包括在引擎级别和池级别的两个修补程序。虽然在高度并发的基因事件中观察到这个问题，但理论上可以发生在连接关闭操作内发生断开连接的任何情况下。

    [¶](#change-b3e19fc9b61e48ed28a2d41b53aa789b)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3043](http://www.sqlalchemy.org/trac/ticket/3043)

-   **[engine] [bug]**The engine-level error handling and wrapping
    routines will now take effect in all engine connection use cases,
    including when user-custom connect routines are used via the
    [`create_engine.creator`](core_engines.html#sqlalchemy.create_engine.params.creator "sqlalchemy.create_engine")
    parameter, as well as when the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    encounters a connection error on revalidation.

    也可以看看

    [DBAPI exception wrapping and handle\_error() event
    improvements](migration_10.html#change-3266)

    [¶](#change-305888802341ee5b5704384fe2d5d5df)

    参考文献：[＃3266](http://www.sqlalchemy.org/trac/ticket/3266)

-   **[engine]
    [bug]**在事件正在自己运行的同时，从侦听器内部或并发线程中移除（或添加）事件侦听器，现在会引发RuntimeError，如所使用的集合现在是`colletions.deque()`的一个实例，并且在迭代时不支持更改。以前，使用普通的Python列表从事件本身中删除会产生沉默失败。[¶](#change-f9df77c38b48404825304dd1b5099cbc)

    参考文献：[＃3163](http://www.sqlalchemy.org/trac/ticket/3163)

### SQL [¶ T0\>](#change-1.0.0b1-sql "Permalink to this headline")

-   **[sql] [feature]**稍微放宽了[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的契约，因为您可以指定一个[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")表达式作为目标；如果要通过内联声明或通过[`Table.append_constraint()`](core_metadata.html#sqlalchemy.schema.Table.append_constraint "sqlalchemy.schema.Table.append_constraint")将索引手动添加到表中，则索引不再需要存在表格绑定列。[T11\>](#change-553972af1791bce62b6e70a2b4b58c62)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3028](http://www.sqlalchemy.org/trac/ticket/3028)

-   **[sql] [feature]**Added new flag
    [`expression.between.symmetric`](core_sqlelement.html#sqlalchemy.sql.expression.between.params.symmetric "sqlalchemy.sql.expression.between"),
    when set to True renders “BETWEEN SYMMETRIC”.
    还添加了一个新的否定运算符“notbetween\_op”，该运算符现在允许像`〜col.between（x， y）`这样的表达式呈现为“ col NOT BETWEEN x AND
    y“，而不是一个带括号的NOT字符串。[¶](#change-02c788316ab5dac725919f22d513af61)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃2990](http://www.sqlalchemy.org/trac/ticket/2990)

-   **[sql] [feature]**The SQL compiler now generates the mapping of
    expected columns such that they are matched to the received result
    set positionally, rather than by name.
    最初，这被视为一种处理我们的列返回了难以预测的名称的案例，尽管在现代使用中这个问题已经被匿名标签克服。在这个版本中，该方法基本上通过几十次调用减少了每个结果的函数调用次数，对于更大的结果列集则更多。如果在编译的列集与接收到的列集之间存在任何差异，那么这种方法仍然会降级为现代版本的旧方法，因此，对于部分或全部文本编译方案而言，这些列表可能不一致时没有问题。[¶
    T0\>](#change-8f6d04c8049c045718d8b2c153efd641)

    参考文献：[＃918](http://www.sqlalchemy.org/trac/ticket/918)

-   **[sql] [feature]**使用[`Column.server_default`](core_metadata.html#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")参数调用的[`DefaultClause`](core_defaults.html#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")中的文字值现在将使用“内联”编译器，以便它们按原样呈现，而不是作为绑定参数。

    也可以看看

    [Column server defaults now render literal
    values](migration_10.html#change-3087)

    [¶](#change-70c132d171b14712cef0e03b38e36176)

    参考文献：[＃3087](http://www.sqlalchemy.org/trac/ticket/3087)

-   **[sql]
    [feature]**传递给SQL表达式单元的对象不能被解释为SQL片段时，报告表达式的类型；请求礼貌Ryan
    P. Kelly。[¶](#change-0d5ede096a0fc28dba2ae3cc966f7ce4)

    参考文献：[请求github：150](https://github.com/zzzeek/sqlalchemy/pull/150)

-   **[sql] [feature]**为[`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")方法添加了一个新参数[`Table.tometadata.name`](core_metadata.html#sqlalchemy.schema.Table.tometadata.params.name "sqlalchemy.schema.Table.tometadata")。与[`Table.tometadata.schema`](core_metadata.html#sqlalchemy.schema.Table.tometadata.params.schema "sqlalchemy.schema.Table.tometadata")类似，此参数会使新复制的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")采用新名称而不是现有名称。这增加了一个有趣的功能，即用一个新名称将[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象复制到*相同的*
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")目标。拉提出请求n.d.帕克。[¶
    T0\>](#change-ec77f5fb7c2ec01c645e9f8d9b4832b8)

    参考文献：[请求github：139](https://github.com/zzzeek/sqlalchemy/pull/139)

-   **[sql] [feature]**Exception messages have been spiffed up a bit.
    如果为None，则不显示SQL语句和参数，从而减少与语句无关的错误消息的混淆。显示DBAPI级别异常的完整模块和类名，清楚地表明这是一个包装的DBAPI异常。语句和参数本身被限制在括号内的部分，以更好地将它们与错误消息和相互之间隔离。[¶](#change-38450c605d2df954cca91dfb84d0b5de)

    参考文献：[＃3172](http://www.sqlalchemy.org/trac/ticket/3172)

-   **[sql] [feature]**[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
    now includes Python and SQL-expression defaults if otherwise
    unspecified; the limitation where non- server column defaults aren’t
    included in an INSERT FROM SELECT is now lifted and these
    expressions are rendered as constants into the SELECT statement.

    也可以看看

    [INSERT FROM SELECT now includes Python and SQL-expression
    defaults](migration_10.html#feature-insert-from-select-defaults)

    [¶](#change-b54916ee4be6c995b86450e0be4f551a)

-   **[sql] [feature]**对于适用的数据库，[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")构造现在包含在反映[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象时。为了以足够的准确性达到这个目的，MySQL和Postgresql现在包含了在反映表，索引和约束时纠正索引重复和唯一约束的功能。In
    the case of MySQL, there is not actually a “unique constraint”
    concept independent of a “unique index”, so for this backend
    [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
    continues to remain non-present for a reflected [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").
    For Postgresql, the query used to detect indexes against
    `pg_index` has been improved to check for the
    same construct in `pg_constraint`, and the
    implicitly constructed unique index is not included with a reflected
    [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

    In both cases, the [`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")
    and the [`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")
    methods return both constructs individually, but include a new token
    `duplicates_constraint` in the case of
    Postgresql or `duplicates_index` in the case of
    MySQL to indicate when this condition is detected. 拉约请求Johannes
    Erdfelt提供。

    也可以看看

    [UniqueConstraint is now part of the Table reflection
    process](migration_10.html#feature-3184)

    [¶](#change-79b21344c66473f22ca547a5bd1db39a)

    参考文献：[＃3184](http://www.sqlalchemy.org/trac/ticket/3184)，[拉取请求bitbucket：30](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/30)

-   **[sql] [feature]**Added new method
    [`Select.with_statement_hint()`](core_selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint "sqlalchemy.sql.expression.Select.with_statement_hint")
    and ORM method [`Query.with_statement_hint()`](orm_query.html#sqlalchemy.orm.query.Query.with_statement_hint "sqlalchemy.orm.query.Query.with_statement_hint")
    to support statement-level hints that are not specific to a
    table.[¶](#change-828e90507d9e510ed8982e8e4765b3c4)

    参考文献：[＃3206](http://www.sqlalchemy.org/trac/ticket/3206)

-   **[sql] [feature]**The `info` parameter has been
    added as a constructor argument to all schema constructs including
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"),
    [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index"),
    [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey"),
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint"),
    [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint"),
    [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint"),
    [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint").[¶](#change-29a46a76843336a7bb96c5eb8e10d349)

    参考文献：[＃2963](http://www.sqlalchemy.org/trac/ticket/2963)

-   **[sql] [feature]**The [`Table.autoload_with`](core_metadata.html#sqlalchemy.schema.Table.params.autoload_with "sqlalchemy.schema.Table")
    flag now implies that [`Table.autoload`](core_metadata.html#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")
    should be `True`. 请求Malik
    Diarra提供。[¶](#change-8c119ef8352a4ded12f21ceeb8206401)

    参考文献：[＃3027](http://www.sqlalchemy.org/trac/ticket/3027)

-   **[sql] [feature]**The [`Select.limit()`](core_selectable.html#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")
    and [`Select.offset()`](core_selectable.html#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")
    methods now accept any SQL expression, in addition to integer
    values, as arguments.
    通常，这用于允许传递绑定参数，该参数可以稍后用值替换，从而允许SQL查询的Python端缓存。这里的实现完全向后兼容现有的第三方方言，但是那些实现特殊LIMIT
    /
    OFFSET系统的方言需要修改才能利用新的功能。限制和偏移也支持“literal\_binds”模式，[¶](#change-11ea70249f3dd8a1cbfa008dfd6b3b7d)

    参考文献：[＃3034](http://www.sqlalchemy.org/trac/ticket/3034)

-   **[sql] [changed]**The [`column()`](core_sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    and [`table()`](core_selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")
    constructs are now importable from the “from sqlalchemy” namespace,
    just like every other Core
    construct.[¶](#change-47e8252f60bddcee7241fffca1f31f22)

-   **[sql] [changed]**The implicit conversion of strings to
    [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    constructs when passed to most builder methods of [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    as well as [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    now emits a warning with just the plain string sent.
    然而，文本转换仍然正常进行。接受不带警告字符串的唯一方法是像“order\_by()”，“group\_by()”这样的“标签引用”方法。这些函数现在将在编译时尝试将单个字符串参数解析为可选择的列或标签表达式；如果没有找到，表达式仍会呈现，但您会再次收到警告。这里的基本原理是，从字符串到文本的隐式转换比现在更不可预期，并且最好是在传递原始字符串时向用户发送更多方向以指示应采取的方向。core\_ORM教程已更新，以深入了解如何处理文本。

    也可以看看

    [Warnings emitted when coercing full SQL fragments into
    text()](migration_10.html#migration-2992)

    [¶](#change-684a942e0874832475bc4b2d6b3ecbd9)

    参考文献：[＃2992](http://www.sqlalchemy.org/trac/ticket/2992)

-   **[sql] [bug]**将`native_enum`标志添加到[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")的`__repr__()`与Alembic自动生成一起使用时很重要。拉请求礼貌Dimitris
    Theodorou。[¶](#change-9ae9e60a64156ef8b01aa18d9ab79582)

    这个改变也被**backported**改为：0.9.9

    参考文献：[pull request
    bitbucket：41](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/41)

-   **[sql] [bug]**Fixed bug where using a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    that implemented a type that was also a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    would fail with Python’s “Cannot create a consistent method
    resolution order (MRO)” error, when any kind of SQL comparison
    expression were used against an object using this
    type.[¶](#change-c4ca12ab497a943945db5eadb8afdcb1)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3278](http://www.sqlalchemy.org/trac/ticket/3278)

-   **[sql] [bug]**Fixed issue where the columns from a SELECT embedded
    in an INSERT, either through the values clause or as a “from
    select”, would pollute the column types used in the result set
    produced by the RETURNING clause when columns from both statements
    shared the same name, leading to potential errors or mis-adaptation
    when retrieving the returning
    rows.[¶](#change-0fa65101409965b00ae87e09df2deccd)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3248](http://www.sqlalchemy.org/trac/ticket/3248)

-   **[sql] [bug]**Fixed bug where a fair number of SQL elements within
    the sql package would fail to `__repr__()`
    successfully, due to a missing `description`
    attribute that would then invoke a recursion overflow when an
    internal AttributeError would then re-invoke `__repr__()`.[¶](#change-c518fd751f15c7bd9ca6846998ca1123)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3195](http://www.sqlalchemy.org/trac/ticket/3195)

-   **[sql] [bug]**An adjustment to table/index reflection such that if
    an index reports a column that isn’t found to be present in the
    table, a warning is emitted and the column is skipped.
    对于一些特殊的系统列情况，可能会发生这种情况，正如Oracle观察到的那样。[¶](#change-3dda9c816b245a162ae7caa498e557ca)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3180](http://www.sqlalchemy.org/trac/ticket/3180)

-   **[sql] [bug]**Fixed bug in CTE where `literal_binds` compiler argument would not be always be correctly
    propagated when one CTE referred to another aliased CTE in a
    statement.[¶](#change-4f0c952d23b07cabacb2f2b5506144a0)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3154](http://www.sqlalchemy.org/trac/ticket/3154)

-   **[sql]
    [bug]**修正了由[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)导致的0.9.7回归与错误的单元测试的结合，使得所谓的“模式”类型如[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")和[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")不能再被腌制。[¶](#change-c84995f2c63b6054e2cace46281a86e2)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3144](http://www.sqlalchemy.org/trac/ticket/3144)，[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)

-   **[sql] [bug]**Fix bug in naming convention feature where using a
    check constraint convention that includes
    `constraint_name` would then force all
    [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    and [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    types to require names as well, as these implicitly create a
    constraint, even if the ultimate target backend were one that does
    not require generation of the constraint such as Postgresql.
    这些特定约束的命名约定的机制已重新组织，以便在DDL编译时完成命名确定，而不是在约束/表构造时完成命令。[¶](#change-0b7554df5bbc7c044d69d2b40ba9ba35)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)

-   **[sql] [bug]**Fixed bug in common table expressions whereby
    positional bound parameters could be expressed in the wrong final
    order when CTEs were nested in certain
    ways.[¶](#change-9881397eb449cc15f8ace6fbcbd4eb09)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3090](http://www.sqlalchemy.org/trac/ticket/3090)

-   修正了多值[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造无法检查给定的字面SQL表达式第一个以后的值的问题。[**[sql]
    [bug]**](#change-c9422f7c699644c36a03c9721b9e9960)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3069](http://www.sqlalchemy.org/trac/ticket/3069)

-   **[sql]
    [bug]**在Python版本\<2.6.5的dialect\_kwargs迭代中添加了一个“str()”步骤，解决了“no
    unicode="" keyword="" arg”关键字在一些反射过程中引用。¶

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3123](http://www.sqlalchemy.org/trac/ticket/3123)

-   **[sql] [bug]**The [`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    method will now accept a type class as an argument which is
    internally converted to an instance, using the same convention long
    established by other constructs such as [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column").[¶](#change-e5ef7cae58e33445c054718ec2361f1d)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3122](http://www.sqlalchemy.org/trac/ticket/3122)

-   **[sql] [bug]**The [`Column.nullable`](core_metadata.html#sqlalchemy.schema.Column.params.nullable "sqlalchemy.schema.Column")
    flag is implicitly set to `False` when that
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    is referred to in an explicit [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    for that table. 这种行为现在与[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")本身将[`Column.primary_key`](core_metadata.html#sqlalchemy.schema.Column.params.primary_key "sqlalchemy.schema.Column")标志设置为`True`时的行为相匹配，该行为旨在成为一个完全等效的情况[¶
    T8\>](#change-281f7135707711426544c956bad3dc76)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3023](http://www.sqlalchemy.org/trac/ticket/3023)

-   **[sql] [bug]**Fixed bug where the [`Operators.__and__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__and__ "sqlalchemy.sql.operators.Operators.__and__"),
    [`Operators.__or__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__or__ "sqlalchemy.sql.operators.Operators.__or__")
    and [`Operators.__invert__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__invert__ "sqlalchemy.sql.operators.Operators.__invert__")
    operator overload methods could not be overridden within a custom
    [`TypeEngine.Comparator`](core_type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")
    implementation.[¶](#change-3ea444f027c5e125d738d7c910e350ea)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3012](http://www.sqlalchemy.org/trac/ticket/3012)

-   **[sql] [bug]**Fixed bug in new
    [`DialectKWArgs.argument_for()`](core_sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
    method where adding an argument for a construct not previously
    included for any special arguments would
    fail.[¶](#change-0d2c9fb4311c501e2c7be559308fe61d)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3024](http://www.sqlalchemy.org/trac/ticket/3024)

-   **[sql] [bug]**Fixed regression introduced in 0.9 where new “ORDER
    BY ” feature from
    [\#1068](http://www.sqlalchemy.org/trac/ticket/1068) would not apply
    quoting rules to the label name as rendered in the ORDER
    BY.[¶](#change-1e6a69139b4a3648c3a1ccc79e3e9fbb)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃1068](http://www.sqlalchemy.org/trac/ticket/1068)，[＃3020](http://www.sqlalchemy.org/trac/ticket/3020)

-   **[sql] [bug]**将[`Function`](core_functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")的导入恢复到`sqlalchemy.sql.expression`导入命名空间，该空间在0.9开始时被删除[¶
    T7\>](#change-7023fa6f794789bffac1141bc7ecf86b)

    这个改变也被**backported**改为：0.9.5

-   **[sql] [bug]**Fixed bug in [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and other [`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    subclasses where direct association of the type with a
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    would lead to a hang when events (like create events) were emitted
    on the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").[¶](#change-39ff64c9a38a07a10351e5eac319e215)

    This change is also **backported** to: 0.9.7, 0.8.7

    参考文献：[＃3124](http://www.sqlalchemy.org/trac/ticket/3124)

-   **[sql] [bug]**Fixed a bug within the custom operator plus
    [`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    system, whereby using a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    in conjunction with variant would fail with an MRO error when a
    comparison operator was
    used.[¶](#change-3f0858c763a82a38425a4f5cd06df17b)

    This change is also **backported** to: 0.9.7, 0.8.7

    参考文献：[＃3102](http://www.sqlalchemy.org/trac/ticket/3102)

-   **[sql] [bug]**Fixed bug in INSERT..FROM SELECT construct where
    selecting from a UNION would wrap the union in an anonymous (e.g.
    unlabled) subquery.[¶](#change-7d8d4c6b958b8f1189653efea4b7b3d8)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3044](http://www.sqlalchemy.org/trac/ticket/3044)

-   修复了当[`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")和[`Table.delete()`](core_metadata.html#sqlalchemy.schema.Table.delete "sqlalchemy.schema.Table.delete")在空的时候会产生一个空的WHERE子句的问题。**[sql]
    [bug]** [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")或[`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")或其他空白表达。这与[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的一致。[¶](#change-49df72c237a28d2aed4a95b52c723c1e)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3045](http://www.sqlalchemy.org/trac/ticket/3045)

-   **[sql] [bug]**The multi-values version of [`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
    has been repaired to work more usefully with tables that have
    Python- side default values and/or functions, as well as server-side
    defaults.
    该功能现在可以使用使用“位置”参数的方言；就像“executemany”样式调用一样，每个行也会单独调用一个Python可调用对象；服务器端默认列将不再隐式地接收为第一行显式指定的值，而拒绝在没有显式值的情况下调用。

    也可以看看

    [Python-side defaults invoked for each row invidually when using a
    multivalued
    insert](migration_10.html#bug-3288)时，为每行独立调用Python端缺省值

    [¶](#change-122f0ef022ba2c5e0c4793bc923c28e2)

    参考文献：[＃3288](http://www.sqlalchemy.org/trac/ticket/3288)

-   **[sql] [bug]**Fixed bug in [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    method where the [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    associated with a [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    or [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    type object would be doubled in the target table.
    复制过程现在将该约束对象的生产追踪为类型对象的本地对象。[¶](#change-deb48f32e1bed24bf1ca698f249edd8b)

    参考文献：[＃3260](http://www.sqlalchemy.org/trac/ticket/3260)

-   **[sql] [bug]** `ForeignKeyConstraint.columns`集合的行为契约已经一致；这个属性现在是一个类似所有其他约束的[`ColumnCollection`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")，并且在约束与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联的时候初始化。

    也可以看看

    [ForeignKeyConstraint.columns is now a
    ColumnCollection](migration_10.html#change-3243)

    [¶](#change-2c2325d005f45286712184e3593a548f)

    参考文献：[＃3243](http://www.sqlalchemy.org/trac/ticket/3243)

-   **[sql] [bug]**The `Column.key`{ attribute is now used as the source of anonymous bound
    parameter names within expressions, to match the existing use of
    this value as the key when rendered in an INSERT or UPDATE
    statement. 这允许将`Column.key`{用作“替代”字符串来解决难以转换为绑定参数名称的困难列名称。请注意，在任何情况下，paramstyle都可以在[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")上配置，并且今天大多数DBAPI支持命名和位置样式。[¶](#change-31200a6951c38906d011838b19760a18)

    参考文献：[＃3245](http://www.sqlalchemy.org/trac/ticket/3245)

-   **[sql]
    [bug]**修复传递给此事件的[`PoolEvents.reset.dbapi_connection`](core_events.html#sqlalchemy.events.PoolEvents.reset.params.dbapi_connection "sqlalchemy.events.PoolEvents.reset")参数的名称；特别是这会影响该事件的“命名”参数风格的使用。拉金请求提供Jason
    Goldberger。[¶](#change-45c6243938b8d4ee1e742945f0bb54a6)

    参考文献：[请求github：146](https://github.com/zzzeek/sqlalchemy/pull/146)

-   **[sql] [bug]**Reversing a change that was made in 0.9, the
    “singleton” nature of the “constants” [`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null"),
    [`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true"),
    and [`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
    has been reverted.
    这些返回“单例”对象的函数具有这样的效果，即不管词典使用如何，不同的实例都将被视为相同，这尤其会影响SELECT语句的columns子句的呈现。

    也可以看看

    [null(), false() and true() constants are no longer
    singletons](migration_10.html#bug-3170)

    [¶](#change-df1b227cf2b11212ed7273639ee8494a)

    参考文献：[＃3170](http://www.sqlalchemy.org/trac/ticket/3170)

-   **[sql] [bug] [engine]**修复了当您调用[`Connection.connect()`](core_connections.html#sqlalchemy.engine.Connection.connect "sqlalchemy.engine.Connection.connect")时获得的“分支”连接不会共享的错误与父母的无效状态。分支体系结构已经调整了一点，以便分支连接按照所有失效状态和操作顺从父项。[¶](#change-d95f6dd7c7d56fb5b50397f3c1355b6c)

    参考文献：[＃3215](http://www.sqlalchemy.org/trac/ticket/3215)

-   **[sql] [bug] [engine]**修复了当您调用[`Connection.connect()`](core_connections.html#sqlalchemy.engine.Connection.connect "sqlalchemy.engine.Connection.connect")时获得的“分支”连接不会共享的错误与父母的交易状态。分支体系结构已经做了一些调整，以便分支连接按照所有事务状态和操作顺从父进程。[¶](#change-65d68f5b8481db16ce132eedd3b8d459)

    参考文献：[＃3190](http://www.sqlalchemy.org/trac/ticket/3190)

-   **[sql] [bug]**Using [`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
    now implies `inline=True` on [`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert").
    这有助于修复INSERT ... FROM
    SELECT构造无意中编译为支持后端的“隐式返回”的错误，这会在插入零行的INSERT情况下导致破坏（因为隐式返回期望行）
    ，以及在插入多行的INSERT情况下的任意返回数据（例如，只有很多行的第一行）。一个类似的更改也适用于具有多个参数集的INSERT..VALUES；隐含的RETURNING将不再为此语句发出。由于这两个构造都处理可变数量的行，所以[`ResultProxy.inserted_primary_key`](core_connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。以前，有一个文档说明，有人可能更喜欢带有INSERT..FROM
    SELECT的`inline=True`，因为有些数据库不支持返回，因此不能做“隐式”返回，但没有任何理由INSERT
    ... FROM
    SELECT需要在任何情况下隐式返回。如果需要插入数据，则应使用常规显式[`Insert.returning()`](core_dml.html#sqlalchemy.sql.expression.Insert.returning "sqlalchemy.sql.expression.Insert.returning")来返回可变数目的结果行。[¶](#change-18b10ba82954d47ea8c64416cf12bb27)

    参考文献：[＃3169](http://www.sqlalchemy.org/trac/ticket/3169)

-   **[sql] [enhancement]**Custom dialects that implement
    `GenericTypeCompiler` can
    now be constructed such that the visit methods receive an indication
    of the owning expression object, if any.
    任何接受关键字参数的访问方法（例如`**kw`）在大多数情况下都会接收关键字参数`type_expression`，并引用该类型所包含的表达式对象。对于DDL中的列，方言的编译器类可能需要修改它的`get_column_specification()`方法以支持它。如果在参数签名中提供`**kw`，`UserDefinedType.get_col_spec()`方法也会接收`type_expression`。[¶](#change-464e59fa2bf92cf803edfc0088f713da) \>

    参考文献：[＃3074](http://www.sqlalchemy.org/trac/ticket/3074)

### 架构[¶ T0\>](#change-1.0.0b1-schema "Permalink to this headline")

-   **[schema] [feature]**The DDL generation system of
    [`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
    and [`MetaData.drop_all()`](core_metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
    has been enhanced to in most cases automatically handle the case of
    mutually dependent foreign key constraints; the need for the
    [`ForeignKeyConstraint.use_alter`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")
    flag is greatly reduced.
    该系统还适用于先前未给出名称的约束；只有在DROP的情况下，该周期中涉及的至少一个约束所需的名称。

    也可以看看

    [The use\_alter flag on ForeignKeyConstraint is (usually) no longer
    needed](migration_10.html#feature-3282)

    [¶](#change-1029cbed41420ead46a2b77d52f42920)

    参考文献：[＃3282](http://www.sqlalchemy.org/trac/ticket/3282)

-   **[schema] [feature]**Added a new accessor
    [`Table.foreign_key_constraints`{](core_metadata.html#sqlalchemy.schema.Table.foreign_key_constraints "sqlalchemy.schema.Table.foreign_key_constraints")
    to complement the [`Table.foreign_keys`{](core_metadata.html#sqlalchemy.schema.Table.foreign_keys "sqlalchemy.schema.Table.foreign_keys")
    collection, as well as [`ForeignKeyConstraint.referred_table`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.referred_table "sqlalchemy.schema.ForeignKeyConstraint.referred_table").[¶](#change-7288ebf25551a199d61be187d6926a8b)

-   **[schema] [bug]**The [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    construct now supports naming conventions that include the token
    `%(column_0_name)s`; the constraint expression
    is scanned for columns. 此外，不包含`%(constraint_name)s`标记的检查约束的命名约定现在可用于[`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    - 生成的约束，如[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")和[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")；由于[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)的原因，它在0.9.7中停止工作。

    也可以看看

    [Naming CHECK
    Constraints](core_constraints.html#naming-check-constraints)

    [Configuring Naming for Boolean, Enum, and other schema
    types](core_constraints.html#naming-schematypes)配置命名

    [¶](#change-5851c2f9630e7aeed059ec8faeab5fc6)

    参考文献：[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)，[＃3299](http://www.sqlalchemy.org/trac/ticket/3299)

### 的PostgreSQL [¶ T0\>](#change-1.0.0b1-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**使用`postgresql_concurrently`添加了对使用Postgresql索引的`CONCURRENTLY`关键字的支持。请求Iuri de Silvio提出请求。

    也可以看看

    [Indexes with
    CONCURRENTLY](dialects_postgresql.html#postgresql-index-concurrently)

    [¶](#change-9c8871edf9c5e6a62540a127958c0c4e)

    这个改变也被**backported**改为：0.9.9

    参考：[拉请求bitbucket：45](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/45)

-   **[postgresql] [feature]
    [pg8000]**通过pg8000驱动程序为“理智的多行数”添加支持，主要适用于使用ORM进行版本控制时。该功能基于使用的pg8000
    1.9.14或更高版本进行版本检测。拉托洛克洛请求礼貌。[¶](#change-c8679f38da94085f949f3f8fdec71306)

    这个改变也是**backported**改为：0.9.8

    参考文献：[请求github：125](https://github.com/zzzeek/sqlalchemy/pull/125)

-   **[postgresql] [feature]**添加kw参数`postgresql_regconfig`到[`ColumnOperators.match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")运算符，允许指定“reg
    config”参数发送到`to_tsquery()`函数。请求Jonathan
    Vanasco提供。[¶](#change-a11821d7d20015d6d83485a50f48aa6d)

    这个改变也被**backported**改为：0.9.7

    References: [\#3078](http://www.sqlalchemy.org/trac/ticket/3078),
    [pull request
    bitbucket:22](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/22)

-   **[postgresql] [feature]**通过[`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")增加了对Postgresql
    JSONB的支持。请求礼貌Damian
    Dimmich。[¶](#change-65fc53d293aae94000bece0cfec7dc02)

    这个改变也被**backported**改为：0.9.7

    参考文献：[请求github：101](https://github.com/zzzeek/sqlalchemy/pull/101)

-   **[postgresql] [feature]**在使用pg8000
    DBAPI时增加了对AUTOCOMMIT隔离级别的支持。拉托洛克洛请求礼貌。[¶](#change-185ea3fa8da27b13fd310a783ad58be2)

    这个改变也被**backported**改为：0.9.5

    参考文献：[请求github：88](https://github.com/zzzeek/sqlalchemy/pull/88)

-   **[postgresql] [feature]**将新标志[`ARRAY.zero_indexes`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.zero_indexes "sqlalchemy.dialects.postgresql.ARRAY")添加到Postgresql
    [`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型。当设置为`True`时，在传递到数据库之前，值为1将被添加到所有数组索引值，从而允许Python样式的基于零的索引和基于Postgresql
    one的索引之间具有更好的互操作性。请求礼貌Alexey
    Terentev。[¶](#change-ca799da80767ded4fb507183b68fc51e)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃2785](http://www.sqlalchemy.org/trac/ticket/2785)，[拉取请求bitbucket：18](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/18)

-   **[postgresql] [feature]**
    PG8000方言现在支持[`create_engine.encoding`](core_engines.html#sqlalchemy.create_engine.params.encoding "sqlalchemy.create_engine")参数，方法是在连接上设置客户端编码，然后由pg8000拦截。拉托洛克洛请求礼貌。[¶](#change-d52ca2e8075eaaf7fae1903092cfedfe)

    参考：[请求github：132](https://github.com/zzzeek/sqlalchemy/pull/132)

-   **[postgresql]
    [feature]**增加了对PG8000原生JSONB功能的支持。拉托洛克洛请求礼貌。[¶](#change-7e075e5c447c03086a2a0f17646240a1)

    参考：[请求github：132](https://github.com/zzzeek/sqlalchemy/pull/132)

-   **[postgresql] [feature] [pypy]**增加了对pypy上psycopg2cffi
    DBAPI的支持。拉请求礼貌shauns。

    也可以看看

    [`sqlalchemy.dialects.postgresql.psycopg2cffi`](dialects_postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2cffi "sqlalchemy.dialects.postgresql.psycopg2cffi")

    [¶](#change-64734b17d3eb6c3fd68a94871b4d52fb)

    References: [\#3052](http://www.sqlalchemy.org/trac/ticket/3052),
    [pull request
    bitbucket:34](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/34)

-   **[postgresql]
    [feature]**增加了对应用于聚合函数的FILTER关键字的支持，Postgresql
    9.4支持该关键字。拉尔请求IljaEverilä礼貌。

    也可以看看

    [Postgresql FILTER keyword](migration_10.html#feature-gh134)

    [¶](#change-fe67d804d0a940d8be8496fcaa7991d4)

    参考文献：[请求github：134](https://github.com/zzzeek/sqlalchemy/pull/134)

-   **[postgresql]
    [feature]**已经添加了对物化视图和外部表的反映，以及对[`Inspector.get_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names "sqlalchemy.engine.reflection.Inspector.get_view_names")中物化视图的支持以及新方法[`PGInspector.get_foreign_table_names()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_foreign_table_names "sqlalchemy.dialects.postgresql.base.PGInspector.get_foreign_table_names")在Postgresql版本的[`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")上可用。Pull请求Rodrigo
    Menezes礼貌。

    也可以看看

    [Postgresql Dialect reflects Materialized Views, Foreign
    Tables](migration_10.html#feature-2891)

    [¶](#change-ebab99a9425c3e47b7dc731718ef33ff)

    参考文献：[＃2891](http://www.sqlalchemy.org/trac/ticket/2891)，[请求github：128](https://github.com/zzzeek/sqlalchemy/pull/128)

-   **[postgresql] [feature]**通过[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造渲染DDL时，增加了对PG表选项TABLESPACE，ON
    COMMIT，WITH（OUT）OIDS和INHERITS的支持。拉请求礼貌malikdiarra。

    也可以看看

    [PostgreSQL Table
    Options](dialects_postgresql.html#postgresql-table-options)

    [¶](#change-c2d997de0574a24ee1406fba275c153b)

    参考文献：[＃2051](http://www.sqlalchemy.org/trac/ticket/2051)

-   当使用Postgresql的检查器时，添加新方法[`PGInspector.get_enums()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums "sqlalchemy.dialects.postgresql.base.PGInspector.get_enums")将提供ENUM类型的列表。**[postgresql]
    [feature]**请求礼物Ilya
    Pekelny。[¶](#change-5bb1041a6093e95b51a5d7ceebb49aa0)

    参考：[请求github：126](https://github.com/zzzeek/sqlalchemy/pull/126)

-   **[postgresql] [bug]**使用psycopg2时修复了对Postgresql
    UUID类型与ARRAY类型的支持。psycopg2方言现在使用psycopg2.extras.register\_uuid()挂钩，以便始终将UUID值作为UUID()对象传递给DBAPI或从DBAPI传递。[`UUID.as_uuid`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.UUID.params.as_uuid "sqlalchemy.dialects.postgresql.UUID")标志仍然有效，除非使用psycopg2，否则我们需要在禁用时将返回的UUID对象转换回字符串。[¶](#change-435eea7e8818574357a2498c0f1400bf)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃2940](http://www.sqlalchemy.org/trac/ticket/2940)

-   **[postgresql] [bug]**Added support for the `postgresql.JSONB` datatype when using psycopg2 2.5.4
    or greater, which features native conversion of JSONB data so that
    SQLAlchemy’s converters must be disabled; additionally, the newly
    added psycopg2 extension `extras.register_default_jsonb` is used to establish a JSON deserializer passed to the
    dialect via the `json_deserializer` argument.
    还修复了Postgresql集成测试，它实际上并未将JSONB类型与JSON类型相反。请求Mateusz
    Susik提供。[¶](#change-17f696f8363a81871bbc9c3d2ed800b8)

    这个改变也被**backported**改为：0.9.9

    参考文献：[请求github：145](https://github.com/zzzeek/sqlalchemy/pull/145)

-   **[postgresql]
    [bug]**在注册HSTORE类型时，修复了使用“array\_oid”标志的旧版psycopg2版本\<2.4.3，该版本不支持该标志，以及使用native
    json串行器钩子“register\_default\_json”与用户定义的json\_deserializer在psycopg2版本\<2.5上，其中不包含本地json
    ¶

    这个改变也被**backported**改为：0.9.9

-   **[postgresql] [bug]**Fixed bug where Postgresql dialect would fail
    to render an expression in an [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    that did not correspond directly to a table-bound column; typically
    when a [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct was one of the expressions within the index; or could
    misinterpret the list of expressions if one or more of them were
    such an expression.[¶](#change-05ce1a0889e2a9def9137445d02dc6de)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3174](http://www.sqlalchemy.org/trac/ticket/3174)

-   **[postgresql]
    [bug]**重新审视此问题在0.9.5中首次被修补，显然psycopg2的`.closed`访问器并不像我们假设的那样可靠，所以我们添加了一个当检测到is-disconnect场景时，显式检查异常消息“SSL
    SYSCALL错误：错误的文件描述符”和“SSL
    SYSCALL错误：EOF检测到”。我们将继续咨询psycopg2的connection.closed作为第一次检查。[¶](#change-678bda6dc87cf119880054c9592d5a53)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3021](http://www.sqlalchemy.org/trac/ticket/3021)

-   **[postgresql] [bug]**Fixed bug where Postgresql JSON type was not
    able to persist or otherwise render a SQL NULL column value, rather
    than a JSON-encoded `'null'`.
    为了支持这种情况，更改如下：

    -   现在可以指定[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")值，这将始终导致产生该语句的NULL值。
    -   添加了一个新参数[`JSON.none_as_null`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON.params.none_as_null "sqlalchemy.dialects.mysql.JSON")，当True表示Python
        `None`值应该作为SQL
        NULL执行，而不是JSON编码`'null'`

    对于非psycopg2的DBAPI，即pg8000，也会修复NULL的空值。

    [¶](#change-4437affca8615476c90ba2583daa2a88)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3159](http://www.sqlalchemy.org/trac/ticket/3159)

-   **[postgresql] [bug]**
    DBAPI错误的异常包装系统现在可以容纳非标准DBAPI异常，例如psycopg2
    TransactionRollbackError。这些异常现在将使用`sqlalchemy.exc`中最接近的可用子类进行引发，如果是TransactionRollbackError，`sqlalchemy.exc.OperationalError`。[¶](#change-2a6df9779f9af4407c9c4efce9190458)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3075](http://www.sqlalchemy.org/trac/ticket/3075)

-   **[postgresql] [bug]**修正了[`postgresql.array`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")对象中的一个错误，其中与普通Python列表的比较将无法使用正确的数组构造函数。拉请求礼貌Andrew。[¶](#change-947dc4e5d0e46e59a1fec0630c63cfd8)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3141](http://www.sqlalchemy.org/trac/ticket/3141)，[请求github：124](https://github.com/zzzeek/sqlalchemy/pull/124)

-   **[postgresql]
    [bug]**为函数添加了支持的[`FunctionElement.alias()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.alias "sqlalchemy.sql.functions.FunctionElement.alias")方法。
    `func`构造。以前，此方法的行为未定义。当前行为模仿0.9.4之前的行为，即该函数被转换为具有给定别名的单列FROM子句，其中列本身是匿名命名的。[¶](#change-085435079f7139f16f13675776d31727)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3137](http://www.sqlalchemy.org/trac/ticket/3137)

-   **[postgresql] [bug]
    [pg8000]**修正了0.9.5版本中新增的pg8000隔离级别功能导致的错误，其中引擎级别的隔离级别参数会在连接时产生错误[¶
    t2 \>](#change-fd59b588a71617bcbc79e1d3af27e0fb)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3134](http://www.sqlalchemy.org/trac/ticket/3134)

-   **[postgresql] [bug]**当确定异常是否为“断开”错误时，现在查阅psycopg2
    `.closed`访问器；理想情况下，这应该不需要对异常消息进行任何其他检查来检测断开连接，但是我们将保留现有的消息作为后备消息。这应该能够处理新的情况，如“SSL
    EOF”条件。拉德请求礼貌德克米勒。[¶](#change-817ce246e076efdc67696a7e59f8a604)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3021](http://www.sqlalchemy.org/trac/ticket/3021)，[请求github：87](https://github.com/zzzeek/sqlalchemy/pull/87)

-   **[postgresql] [bug]**为PG [`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型添加了`hashable=False`标志，这是允许ORM跳过尝试在混合列/实体列表中请求ORM映射的HSTORE列时“散列”。补丁礼貌GunnlaugurÞórBriem。[¶](#change-841cb0d0b58c849de0668c465b375c91)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3053](http://www.sqlalchemy.org/trac/ticket/3053)

-   **[postgresql]
    [bug]**添加了一个新的“断开连接”消息“连接意外关闭”。这似乎与更新版本的SSL有关。拉提请求Antti
    Haapala礼貌。[¶](#change-391e08a06b2dda8bd1502d285f7fa3ec)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考：[拉取请求bitbucket：13](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/13)

-   **[postgresql] [bug]**The Postgresql [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
    type will emit a DROP TYPE instruction when a plain
    `table.drop()` is called, assuming the object is
    not associated directly with a [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    object.
    为了适应多个表之间共享枚举类型的用例，类型应该直接与[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象关联；在这种情况下，类型只能在元数据级别创建，或者直接创建。一般来说，Postgresql枚举类型的创建/删除规则已被高度重构。

    也可以看看

    [Overhaul of ENUM type create/drop
    rules](migration_10.html#change-3319)

    [¶](#change-00dd6007a5498f39661875f8752be36a)

    参考文献：[＃3319](http://www.sqlalchemy.org/trac/ticket/3319)

-   **[postgresql] [bug]**The `PGDialect.has_table()` method will now query against
    `pg_catalog.pg_table_is_visible(c.oid)`, rather
    than testing for an exact schema match, when the schema name is
    None; this so that the method will also illustrate that temporary
    tables are present.
    请注意，这是一个行为改变，因为Postgresql允许非临时表以默默方式覆盖现有的具有相同名称的临时表，所以这改变了`checkfirst`在该异常情况下的行为。

    也可以看看

    [Postgresql has\_table() now works for temporary
    tables](migration_10.html#change-3264)

    [¶](#change-1fc9593e4484eb96e7d37ce3877329e6)

    参考文献：[＃3264](http://www.sqlalchemy.org/trac/ticket/3264)

-   **[postgresql]
    [enhancement]**在Postgresql方言中添加了一个新类型的[`postgresql.OID`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.OID "sqlalchemy.dialects.postgresql.OID")。虽然“oid”通常是PG中的私有类型，但在现代版本中并未公开，但有一些PG用例，例如可能暴露这些类型的大对象支持，以及某些用户报告的模式反射用例。
    [¶ T0\>](#change-1174b8b08516d0b487d6d8520fcc3b4f)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3002](http://www.sqlalchemy.org/trac/ticket/3002)

### MySQL的[¶ T0\>](#change-1.0.0b1-mysql "Permalink to this headline")

-   **[mysql] [feature]**现在，MySQL方言在所有情况下都使用NULL / NOT
    NULL呈现TIMESTAMP，因此启用`explicit_defaults_for_timestamp`标志的MySQL
    5.6.6将允许TIMESTAMP在`nullable=False`时继续按预期工作。现有的应用程序不受影响，因为SQLAlchemy总是为`nullable=True`的TIMESTAMP列发出NULL。

    也可以看看

    [MySQL TIMESTAMP Type now renders NULL / NOT NULL in all
    cases](migration_10.html#change-3155)

    [TIMESTAMP Columns and
    NULL](dialects_mysql.html#mysql-timestamp-null)

    [¶](#change-888c2e0789c5c34cc840a4b8462d9b9f)

    参考文献：[＃3155](http://www.sqlalchemy.org/trac/ticket/3155)

-   **[mysql] [feature]**在Python
    2下将MySQLdb和Pymysql的“supports\_unicode\_statements”标志更新为True。这是指SQL语句本身，而不是参数，并影响使用非ASCII字符的表和列名称等问题。这些驱动程序似乎都支持Python
    2
    Unicode对象，而在现代版本中没有问题。[¶](#change-4a9ddc227788a62f6b733bcdef159f74)

    参考文献：[＃3121](http://www.sqlalchemy.org/trac/ticket/3121)

-   **[mysql]
    [bug]**增加了对'utf8\_bin'排序检查周围的MySQLdb方言的版本检查，因为这在MySQL服务器\<5.0中失败。¶

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3274](http://www.sqlalchemy.org/trac/ticket/3274)

-   **[mysql] [bug] [mysqlconnector]**Mysqlconnector as of version 2.0,
    probably as a side effect of the python 3 merge, now does not expect
    percent signs (e.g. as used as the modulus operator and others) to
    be doubled, even when using the “pyformat” bound parameter format
    (this change is not documented by Mysqlconnector).
    当检测模运算符是否应该呈现为`%%`或`%`时，方言现在检查py2k和mysqlconnector小于2.0版。[¶](#change-82e5f7ede904a4dfc77f0ed73d7d6de6)

    这个改变也是**backported**改为：0.9.8

-   **[mysql] [bug] [mysqlconnector]** Unicode
    SQL现在传递给MySQLconnector 2.0及更高版本；对于Py2k和MySQL
    \<2.0，字符串被编码。¶

    这个改变也是**backported**改为：0.9.8

-   **[mysql] [bug]**MySQL error 2014 “commands out of sync” appears to
    be raised as a ProgrammingError, not OperationalError, in modern
    MySQL-Python versions; all MySQL error codes that are tested for “is
    disconnect” are now checked within OperationalError and
    ProgrammingError
    regardless.[¶](#change-cc47f2dadf913e8df10f13d8f6369b8a)

    This change is also **backported** to: 0.9.7, 0.8.7

    参考文献：[＃3101](http://www.sqlalchemy.org/trac/ticket/3101)

-   **[mysql] [bug]**Fixed bug where column names added to
    `mysql_length` parameter on an index needed to
    have the same quoting for quoted names in order to be recognized.
    该修复使得引号是可选的，但也提供了旧的行为，以便与使用变通方法的向后兼容。[¶](#change-aeee11434848543451def6bb5409fee7)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3085](http://www.sqlalchemy.org/trac/ticket/3085)

-   **[mysql]
    [bug]**增加了对使用等号在索引中包含KEY\_BLOCK\_SIZE的表来反映表的支持。拉请求礼貌肖恩McGivern。[¶](#change-028aac30fa34b4cac9c150baf9952dc3)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[拉取请求bitbucket：15](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/15)

-   **[mysql]
    [bug]**现在，MySQL方言支持将CAST构造为[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")对象。[¶](#change-d248e6e466f184e254344213a59553d3)

-   **[mysql] [bug]**在MySQL不支持CAST的类型上使用[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")时，会发出警告。
    MySQL仅支持一部分数据类型的CAST。SQLAlchemy很长一段时间在MySQL中省略了不支持类型的CAST。虽然我们现在不想改变它，但我们会发出警告以表明它已发生。当一个CAST与一个根本不支持CAST的较老的MySQL版本（\<4）一起使用时，也会发出一个警告，在这种情况下它也被跳过。¶

    参考文献：[＃3237](http://www.sqlalchemy.org/trac/ticket/3237)

-   **[mysql] [bug]**对[`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")类型进行了大检查，以便不再假定空字符串或具有单个空字符串值的集合实际上一个带有单个空字符串的集合；相反，这是默认处理为空集。为了处理实际上希望将空值`''`作为合法值的[`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")的持久性，添加了一个新的按位操作模式，
    [`mysql.SET.retrieve_as_bitwise`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise "sqlalchemy.dialects.mysql.SET")标志，该标志将使用它们的位标定位来保持并明确检索值。存储和检索本地不转换unicode的驱动程序配置的unicode值也会被修复。

    也可以看看

    [MySQL SET Type Overhauled to support empty sets, unicode, blank
    value handling](migration_10.html#change-3283)

    [¶](#change-220ee8533c248292fd2a189f6855742c)

    参考文献：[＃3283](http://www.sqlalchemy.org/trac/ticket/3283)

-   **[mysql] [bug]**The [`ColumnOperators.match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
    operator is now handled such that the return type is not strictly
    assumed to be boolean; it now returns a [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    subclass called [`MatchType`](core_type_basics.html#sqlalchemy.types.MatchType "sqlalchemy.types.MatchType").
    该类型在Python表达式中使用时仍然会产生布尔行为，但方言可以在结果时覆盖其行为。在MySQL的情况下，虽然MATCH运算符通常用在表达式中的布尔上下文中，但如果实际查询匹配表达式的值，则会返回浮点值；此值与SQLAlchemy的基于C的布尔处理器不兼容，所以MySQL的结果集行为现在遵循[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")类型的行为。还添加了一个新的操作符对象`notmatch_op`，以便更好地允许方言定义匹配操作的否定。

    也可以看看

    [The match() operator now returns an agnostic MatchType compatible
    with MySQL’s floating point return
    value](migration_10.html#change-3263)

    [¶](#change-d684884bc2ec500da77ede3801a695af)

    参考文献：[＃3263](http://www.sqlalchemy.org/trac/ticket/3263)

-   **[mysql] [bug]** MySQL布尔符号“true”，“false”再次工作。0.9
    [＃2682](http://www.sqlalchemy.org/trac/ticket/2682)中的变化不允许MySQL方言在“IS”/“IS
    NOT”的上下文中使用“true”和“false”符号，但MySQL甚至支持这种语法尽管它没有布尔类型。MySQL
    remains “non native boolean”, but the [`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
    and [`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
    symbols again produce the keywords “true” and “false”, so that an
    expression like `column.is_(true())` again works
    on MySQL.

    也可以看看

    [MySQL boolean symbols “true”, “false” work
    again](migration_10.html#bug-3186)

    [¶](#change-9787cfb315047779532af296d86e52c8)

    参考文献：[＃3186](http://www.sqlalchemy.org/trac/ticket/3186)

-   **[mysql]
    [bug]**现在，MySQL方言将禁用[`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error")事件触发它在内部用于检测表是否存在的语句。这是通过使用执行选项`skip_user_error_events`来实现的，该选项为该执行的范围禁用句柄错误事件。通过这种方式，重写异常的用户代码不需要担心偶尔需要捕获SQLAlchemy特定异常的MySQL方言或其他方言。[¶](#change-828372b575d2aa0994e92d6186465a3d)

-   **[mysql]
    [bug]**将MySQL连接器的“raise\_on\_warnings”的默认值更改为False。由于某种原因，这被设置为True。不幸的是，“缓冲”标志必须保持为True，因为MySQL连接器不允许游标被关闭，除非所有结果都被全部获取。[¶](#change-c99bdbe39a0aae424a21593e9240e9f3)

    参考文献：[＃2515](http://www.sqlalchemy.org/trac/ticket/2515)

-   **[mysql] [change]** `gaerdbms`方言不再需要，并且发出弃用警告。Google现在建议直接使用MySQLdb方言。[¶](#change-88c8bf1c005b1ba08a675f1c4fc922b3)

    这个改变也被**backported**改为：0.9.9

    参考文献：[＃3275](http://www.sqlalchemy.org/trac/ticket/3275)

### 源码[¶ T0\>](#change-1.0.0b1-sqlite "Permalink to this headline")

-   **[sqlite]
    [feature]**在SQLite中增加了对部分索引（例如使用WHERE子句）的支持。请求Kai
    Groner提供的请求。

    也可以看看

    [Partial Indexes](dialects_sqlite.html#sqlite-partial-index)

    [¶](#change-3d9fb6341c517aafb29dced236fb59d6)

    这个改变也被**backported**改为：0.9.9

    参考文献：[pull request
    bitbucket：42](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/42)

-   **[sqlite]
    [feature]**为SQLCipher后端添加了新的SQLite后端。该后端使用pysqlcipher
    Python驱动程序提供加密的SQLite数据库，这与pysqlite驱动程序非常相似。

    也可以看看

    [`pysqlcipher`](dialects_sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlcipher "sqlalchemy.dialects.sqlite.pysqlcipher")

    [¶](#change-7e6346bf1aeb5ee43f7e365c475c7b57)

    这个改变也被**backported**改为：0.9.9

-   **[sqlite] [bug]**When selecting from a UNION using an attached
    database file, the pysqlite driver reports column names in
    cursor.description as ‘dbname.tablename.colname’, instead of
    ‘tablename.colname’ as it normally does for a UNION (note that it’s
    supposed to just be ‘colname’ for both, but we work around it).
    此处的列转换逻辑已被调整为检索最右侧的标记，而不是第二个标记，因此它适用于这两种情况。解决方法礼貌Tony
    Roberts。[¶](#change-946017d06b93655ea05ced1c50d7c010)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3211](http://www.sqlalchemy.org/trac/ticket/3211)

-   **[sqlite] [bug]**Fixed a SQLite join rewriting issue where a
    subquery that is embedded as a scalar subquery such as within an IN
    would receive inappropriate substitutions from the enclosing query,
    if the same table were present inside the subquery as were in the
    enclosing query such as in a joined inheritance
    scenario.[¶](#change-dbba9e2ad3a065a1eb84d3b38b6d347d)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3130](http://www.sqlalchemy.org/trac/ticket/3130)

-   **[sqlite] [bug]** UNIQUE和FOREIGN
    KEY约束现在完全反映在SQLite中，包含名称和不包含名称。以前，外键名称被忽略，未命名的唯一约束被忽略。感谢Jon
    Nelson寻求帮助。[¶](#change-792dfcd8b60e9bb55f168dcccc0fd113)

    参考文献：[＃3261](http://www.sqlalchemy.org/trac/ticket/3261)，[＃3244](http://www.sqlalchemy.org/trac/ticket/3244)

-   **[sqlite] [bug]**The SQLite dialect, when using the
    [`sqlite.DATE`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.DATE "sqlalchemy.dialects.sqlite.DATE"),
    [`sqlite.TIME`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.TIME "sqlalchemy.dialects.sqlite.TIME"),
    or [`sqlite.DATETIME`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.DATETIME "sqlalchemy.dialects.sqlite.DATETIME")
    types, and given a `storage_format` that only
    renders numbers, will render the types in DDL as
    `DATE_CHAR`, `TIME_CHAR`,
    and `DATETIME_CHAR`, so that despite the lack of
    alpha characters in the values, the column will still deliver the
    “text affinity”.
    通常这不是必需的，因为默认存储格式中的文本值已经暗示了文本。

    也可以看看

    [Date and Time Types](dialects_sqlite.html#sqlite-datetime)

    [¶](#change-239acc44616f1d843f4adf9a759d3a7b)

    参考文献：[＃3257](http://www.sqlalchemy.org/trac/ticket/3257)

-   **[sqlite] [bug]**
    SQLite现在支持反映来自临时表的唯一约束；以前，这会因类型错误而失败。拉约请求Johannes
    Erdfelt提供。

    也可以看看

    [SQLite/Oracle have distinct methods for temporary table/view name
    reporting](migration_10.html#change-3204) - changes regarding SQLite
    temporary table and view reflection.

    [¶](#change-143526c69a00507711235150baad7656)

    参考文献：[＃3203](http://www.sqlalchemy.org/trac/ticket/3203)，[拉取请求bitbucket：31](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/31)

-   **[sqlite] [bug]**添加了[`Inspector.get_temp_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_table_names "sqlalchemy.engine.reflection.Inspector.get_temp_table_names")和[`Inspector.get_temp_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_view_names "sqlalchemy.engine.reflection.Inspector.get_temp_view_names")；目前，只有SQLite和Oracle方言支持这些方法。The
    return of temporary table and view names has been **removed** from
    SQLite and Oracle’s version of [`Inspector.get_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names")
    and [`Inspector.get_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names "sqlalchemy.engine.reflection.Inspector.get_view_names");
    other database backends cannot support this information (such as
    MySQL), and the scope of operation is different in that the tables
    can be local to a session and typically aren’t supported in remote
    schemas.

    也可以看看

    [SQLite/Oracle have distinct methods for temporary table/view name
    reporting](migration_10.html#change-3204)

    [¶](#change-dc3cc23baa14088445f40787bfb225c9)

    参考文献：[＃3204](http://www.sqlalchemy.org/trac/ticket/3204)

### MSSQL [¶ T0\>](#change-1.0.0b1-mssql "Permalink to this headline")

-   **[mssql] [feature]**为SQL Server 2008启用“多值插入”。拉尔请求Albert
    Cervin礼貌。还扩展了对“IDENTITY
    INSERT”模式的检查，以便在语句的VALUE子句中存在身份钥匙时包含该身份钥匙。[¶](#change-20559f663839ceee7e14634eafedb5be)

    这个改变也被**backported**改为：0.9.7

    参考文献：[请求github：98](https://github.com/zzzeek/sqlalchemy/pull/98)

-   **[mssql] [feature]**SQL Server 2012 now recommends VARCHAR(max),
    NVARCHAR(max), VARBINARY(max) for large text/binary types.
    MSSQL方言现在将基于版本检测以及新的`deprecate_large_types`标志尊重它。

    也可以看看

    [Large Text/Binary Type
    Deprecation](dialects_mssql.html#mssql-large-type-deprecation)

    [¶](#change-f520106ec3455eaa056110c048aa4862)

    参考文献：[＃3039](http://www.sqlalchemy.org/trac/ticket/3039)

-   **[mssql] [changed]**使用pyodbc时，SQL
    Server的基于主机名的连接格式将不再指定默认的“驱动程序名称”，并且如果缺少该驱动程序名称，则会发出警告。SQL
    Server的最佳驱动程序名称经常更改并且是每个平台，因此基于主机名的连接需要指定此名称。基于DSN的连接是首选。

    也可以看看

    [PyODBC driver name is required with hostname-based SQL Server
    connections](migration_10.html#change-3182)是必需的

    [¶](#change-216a4d0059a5b9c4689bd6f999ba2f1e)

    参考文献：[＃3182](http://www.sqlalchemy.org/trac/ticket/3182)

-   **[mssql]
    [bug]**修复了pymssql方言中的版本字符串检测问题，以便与Microsoft SQL
    Azure一起使用，它将单词“SQL Server”更改为“SQL Azure”。[¶ t2
    \>](#change-1ac1ebc454b99a8106f36414704b4f13)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3151](http://www.sqlalchemy.org/trac/ticket/3151)

-   **[mssql] [bug]**Revised the query used to determine the current
    default schema name to use the `database_principal_id()` function in conjunction with the
    `sys.database_principals` view so that we can
    determine the default schema independently of the type of login in
    progress (e.g., SQL Server, Windows,
    etc).[¶](#change-bbd51d56a17c9f56dbfba67a40873a90)

    这个改变也被**backported**改为：0.9.5

    参考文献：[＃3025](http://www.sqlalchemy.org/trac/ticket/3025)

-   **[mssql] [bug]**Added statement encoding to the “SET
    IDENTITY\_INSERT” statements which operate when an explicit INSERT
    is being interjected into an IDENTITY column, to support non-ascii
    table identifiers on drivers such as pyodbc + unix + py2k that don’t
    support unicode
    statements.[¶](#change-1f87a0341490182683860e3d896e5d83)

    This change is also **backported** to: 0.9.7, 0.8.7

-   **[mssql] [bug]**In the SQL Server pyodbc dialect, repaired the
    implementation for the `description_encoding`
    dialect parameter, which when not explicitly set was preventing
    cursor.description from being parsed correctly in the case of result
    sets that contained names in alternate encodings.
    这个参数不应该被继续使用。[¶](#change-8540c30a01328c69626ed15f9d38ae35)

    This change is also **backported** to: 0.9.7, 0.8.7

    参考文献：[＃3091](http://www.sqlalchemy.org/trac/ticket/3091)

### 预言[¶ T0\>](#change-1.0.0b1-oracle "Permalink to this headline")

-   **[oracle] [feature]**通过将`?service_name=<name>`传递给URL，增加了对特定服务名称的cx\_oracle连接的支持，而不是tns名称。请求礼貌SławomirEhlert。[¶](#change-f1f07fe9ae58e5e7549f76959816986a)

    参考文献：[请求github：152](https://github.com/zzzeek/sqlalchemy/pull/152)

-   **[oracle] [feature]**新的Oracle
    DDL特性用于表，索引：COMPRESS，BITMAP。Gabor
    Gombas提供补丁。[¶](#change-d721c0561d8a2b535f97670c2d8ef966)

-   **[oracle] [feature]**添加了对Oracle下的CTE的支持。This includes
    some tweaks to the aliasing syntax, as well as a new CTE feature
    [`CTE.suffix_with()`](core_selectable.html#sqlalchemy.sql.expression.CTE.suffix_with "sqlalchemy.sql.expression.CTE.suffix_with"),
    which is useful for adding in special Oracle-specific directives to
    the CTE.

    也可以看看

    [Improved support for CTEs in Oracle](migration_10.html#change-3220)

    [¶](#change-d9d92d75a7435eeb5a6b5bc6eb1f7f1f)

    参考文献：[＃3220](http://www.sqlalchemy.org/trac/ticket/3220)

-   **[oracle] [feature]**新增了对Oracle表选项ON
    COMMIT的支持。[¶](#change-833d0958c15092ca207886692b5894b6)

-   **[oracle] [bug]**Fixed long-standing bug in Oracle dialect where
    bound parameter names that started with numbers would not be quoted,
    as Oracle doesn’t like numerics in bound parameter
    names.[¶](#change-8cb6529185a476446f028d78bada53c7)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃2138](http://www.sqlalchemy.org/trac/ticket/2138)

-   **[oracle] [bug] [tests]**Fixed bug in oracle dialect test suite
    where in one test, ‘username’ was assumed to be in the database URL,
    even though this might not be the
    case.[¶](#change-a07180efec1ae8c8de5daffb374ea261)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3128](http://www.sqlalchemy.org/trac/ticket/3128)

-   **[oracle] [bug]**An alias name will be properly quoted when
    referred to using the `%(name)s` token inside
    the [`Select.with_hint()`](core_selectable.html#sqlalchemy.sql.expression.Select.with_hint "sqlalchemy.sql.expression.Select.with_hint")
    method.
    以前，Oracle后端没有实现这种引用。[¶](#change-b22f2a6c7705c972bdd48542da13e9e1)

### 杂项[¶ T0\>](#change-1.0.0b1-misc "Permalink to this headline")

-   **[feature]
    [examples]**添加了一个使用最新关系功能说明物化路径的新示例。Jack
    Zhou提供的例子。[¶](#change-34bed682b188b0328e558a3338cd3564)

    这个改变也被**backported**改为：0.9.5

    参考文献：[pull request
    bitbucket：21](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/21)

-   **[feature]
    [ext]**添加了一个新的扩展套件[`sqlalchemy.ext.baked`](orm_extensions_baked.html#module-sqlalchemy.ext.baked "sqlalchemy.ext.baked")。这个简单但不同寻常的系统可以显着节省Python构建和处理orm
    [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，从查询构建到渲染字符串SQL语句。

    也可以看看

    [Baked Queries](orm_extensions_baked.html)

    [¶](#change-fabfc534f4d8cf8fe39e10413fb7d5e6)

    参考文献：[＃3054](http://www.sqlalchemy.org/trac/ticket/3054)

-   **[feature]
    [examples]**一套新的示例，致力于从多个角度详细研究SQLAlchemy
    ORM和Core以及DBAPI的性能。该套件在一个容器内运行，该容器通过控制台输出以及通过RunSnake工具以图形方式提供内置的分析显示。

    也可以看看

    [Performance](orm_examples.html#examples-performance)

    [¶](#change-c3e04c4306f45aebbbd32a56d0f13d47)

-   **[feature] [ext]**The [`sqlalchemy.ext.automap`](orm_extensions_automap.html#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")
    extension will now set `cascade="all, delete-orphan"` automatically on a one-to-many relationship/backref where
    the foreign key is detected as containing one or more non-nullable
    columns.
    在这种情况下，该参数出现在传递给[`automap.generate_relationship()`](orm_extensions_automap.html#sqlalchemy.ext.automap.generate_relationship "sqlalchemy.ext.automap.generate_relationship")的关键字中，并且仍然可以被覆盖。Additionally,
    if the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    specifies `ondelete="CASCADE"` for a
    non-nullable or `ondelete="SET NULL"` for a
    nullable set of columns, the argument
    `passive_deletes=True` is also added to the
    relationship.
    请注意，并非所有后端都支持ondelete的反射，但后端包括Postgresql和MySQL。[¶](#change-748a15a873fc07b67bd7ddfe221fbff3)

    参考文献：[＃3210](http://www.sqlalchemy.org/trac/ticket/3210)

-   **[removed]**
    Drizzle方言已从Core中删除；它现在可以作为[sqlalchemy-drizzle](https://bitbucket.org/zzzeek/sqlalchemy-drizzle)，一种独立的第三方方言。该方言仍然基于SQLAlchemy中存在的MySQL方言。

    也可以看看

    [Drizzle Dialect is now an External
    Dialect](migration_10.html#change-2984)

    [¶](#change-4b74183b867c026c18e2cd7db8eeb462)

-   **[bug] [ext] [py3k]**Fixed bug where the association proxy list
    class would not interpret slices correctly under Py3K.
    拉尔请求礼貌Gilles
    Dartiguelongue。[¶](#change-065233e8c2777e0d68ba556dd655c2f9)

    这个改变也被**backported**改为：0.9.9

    参考文献：[请求github：154](https://github.com/zzzeek/sqlalchemy/pull/154)

-   **[bug] [examples]**Updated the [Versioning with a History
    Table](orm_examples.html#examples-versioned-history) example such
    that mapped columns are re-mapped to match column names as well as
    grouping of columns; in particular, this allows columns that are
    explicitly grouped in a same-column-named joined inheritance
    scenario to be mapped in the same way in the history mappings,
    avoiding warnings added in the 0.9 series regarding this pattern and
    allowing the same view of attribute
    keys.[¶](#change-fa2a2b92fa766fc863eb7235e9fb3d03)

    这个改变也被**backported**改为：0.9.9

-   **[bug] [examples]**Fixed a bug in the
    examples/generic\_assocaitions/discriminator\_on\_association.py
    example, where the subclasses of AddressAssociation were not being
    mapped as “single table inheritance”, leading to problems when
    trying to use the mappings
    further.[¶](#change-615e4d1220e634fb7ce6d05550eb21a7)

    这个改变也被**backported**改为：0.9.9

-   **[bug] [declarative]**Fixed an unlikely race condition observed in
    some exotic end-user setups, where the attempt to check for
    “duplicate class name” in declarative would hit upon a
    not-totally-cleaned-up weak reference related to some other class
    being removed; the check here now ensures the weakref still
    references an object before calling upon it
    further.[¶](#change-42c47d9c9a02c97b7a2be9901e2a9645)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3208](http://www.sqlalchemy.org/trac/ticket/3208)

-   **[bug]
    [ext]**修正了订购清单中的bug，如果reorder\_on\_append标志被设置为True，则在收集替换事件期间将抛出物品的顺序。该修复确保排序列表仅影响与该对象显式关联的列表。[¶](#change-0c1e3c4d921376b5c6e8063fc8ce0569)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3191](http://www.sqlalchemy.org/trac/ticket/3191)

-   修正了[`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")无法实现`update()`字典方法的错误，因此无法捕捉更改。**[bug]
    [ext]**拉请求马特Chisholm。[¶](#change-294bea028af9c9afef0f3f0e1704cdcb)

    这个改变也是**backported**改为：0.9.8

-   **[bug] [ext]**Fixed bug where a custom subclass of
    [`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    would not show up in a “coerce” operation, and would instead return
    a plain [`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict").
    拉请求马特Chisholm。[¶](#change-8d145545ac65b225cab55e7ddd8b87c1)

    这个改变也是**backported**改为：0.9.8

-   **[bug] [pool]**Fixed bug in connection pool logging where the
    “connection checked out” debug logging message would not emit if the
    logging were set up using `logging.setLevel()`,
    rather than using the `echo_pool` flag.
    已经添加了测试来声明这个日志记录。这是在0.9.0中引入的回归。[¶](#change-40ab208d891571a2d6aaa91d50bc86b4)

    这个改变也是**backported**改为：0.9.8

    参考文献：[＃3168](http://www.sqlalchemy.org/trac/ticket/3168)

-   **[bug] [tests]**修正了“python setup.py
    test”没有正确调用distutils的错误，并且在测试套件结束时会发出错误。[T2\>](#change-b4849c03234d67784392c98314d97728)

    这个改变也被**backported**改为：0.9.7

-   **[bug] [declarative]**Fixed bug when the declarative
    `__abstract__` flag was not being distinguished
    for when it was actually the value `False`.
    `__abstract__`标志需要在被测试的级别上进行真实值计算。[¶](#change-b4c1be63379dda62c10d4726c27c8beb)

    这个改变也被**backported**改为：0.9.7

    参考文献：[＃3097](http://www.sqlalchemy.org/trac/ticket/3097)

-   **[bug] [testsuite]**In public test suite, shanged to use of
    `String(40)` from less-supported
    `Text` in
    `StringTest.test_literal_backslashes`.
    Pullreq礼貌Jan. [¶](#change-cfe458e354058e2bba60dd1c3f521791)

    这个改变也被**backported**改为：0.9.5

    参考：[请求github：95](https://github.com/zzzeek/sqlalchemy/pull/95)

-   **[bug] [tests] [py3k]**更正了运行测试时涉及`imp`模块和Python
    3.3或更高版本的一些弃用警告。拉请求马特Chisholm。[¶](#change-2792c57b68ceebf75c4999473088cba4)

    这个改变也被**backported**改为：0.9.5

    References: [\#2830](http://www.sqlalchemy.org/trac/ticket/2830),
    [pull request
    bitbucket:2830](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/2830)

-   **[bug] [declarative]**The `__mapper_args__`
    dictionary is copied from a declarative mixin or abstract class when
    accessed, so that modifications made to this dictionary by
    declarative itself won’t conflict with that of other mappings.
    关于`version_id_col`和`polymorphic_on`参数的字典被修改，将内部的列替换为正式映射到本地类/表的列。[¶
    t4 \>](#change-7190c4c8e7853dc246b3c4c738478edb)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3062](http://www.sqlalchemy.org/trac/ticket/3062)

-   **[bug] [ext]**Fixed bug in mutable extension where
    [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    did not report change events for the `setdefault()` dictionary
    operation.[¶](#change-eae3f266c75c4ae69fc34c7668edf3d1)

    This change is also **backported** to: 0.9.5, 0.8.7

    参考文献：[＃3093](http://www.sqlalchemy.org/trac/ticket/3093)，[＃3051](http://www.sqlalchemy.org/trac/ticket/3051)

-   **[bug] [ext]**Fixed bug where [`MutableDict.setdefault()`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict.setdefault "sqlalchemy.ext.mutable.MutableDict.setdefault")
    didn’t return the existing or new value (this bug was not released
    in any 0.8 version).
    请求礼貌托马斯Hervé。[¶](#change-97ce2c718bb55b40569d4c50e584b2fc)

    This change is also **backported** to: 0.9.5, 0.8.7

    References: [\#3093](http://www.sqlalchemy.org/trac/ticket/3093),
    [\#3051](http://www.sqlalchemy.org/trac/ticket/3051), [pull request
    bitbucket:24](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/24)


